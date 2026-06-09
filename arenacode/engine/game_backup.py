import time
import math
import random
import traceback
import pygame
from typing import List, Dict

from core.tank import Tank
from core.action import Action, ConfiguredAction
from core.sensor import Sensor
from core.bullet import Bullet
from engine.arena import Arena
from engine.collision import CollisionSystem, angulo_relativo, distancia
from engine.renderer import Renderer

class GameEngine:
    def __init__(self, tanques_classes: List[type]):
        self.arena = Arena()
        self.collision = CollisionSystem(self.arena)
        self.renderer = Renderer(self.arena)
        self.balas: List[Bullet] = []
        
        self.tanques: List[Tank] = []
        
        for i, TankClass in enumerate(tanques_classes):
            try:
                tanque = TankClass()
                
                # Gera posição aleatória com margen, evitando áreas do timer (topo) e HUD (baixo)
                tentativas = 0
                while tentativas < 50:
                    x = random.uniform(80, self.arena.largura - 80)
                    y = random.uniform(60, self.arena.altura - 80)
                    
                    # Garante distância mínima de 150px para batalhas em massa
                    dist_ok = True
                    for outro in self.tanques:
                        if math.hypot(x - outro.posicao[0], y - outro.posicao[1]) < 150:
                            dist_ok = False
                            break
                    
                    if dist_ok:
                        break
                    tentativas += 1
                
                # Garante nome único para o placar
                nome_base = tanque.nome
                contador = 1
                while any(t.nome == tanque.nome for t in self.tanques):
                    tanque._set_nome(f"{nome_base} {contador}")
                    contador += 1
                
                tanque._set_posicao(x, y)
                tanque._set_angulo(random.uniform(0, 360))
                
                try:
                    tanque.programar()
                except Exception as e:
                    print(f"[ERRO] Tanque {tanque.nome} falhou no programar(): {e}")
                
                self.tanques.append(tanque)
            except Exception as e:
                print(f"Erro ao instanciar tanque {TankClass.__name__}: {e}")

        self.scores = {t.nome: 0 for t in self.tanques}
        self.tempo_batalha = 60.0
        
    def _gerar_sensores(self, tanque: Tank) -> Sensor:
        inimigos_proximos = []
        for outro in self.tanques:
            if outro is not tanque and outro._esta_vivo():
                dist = distancia(tanque.posicao, outro.posicao)
                if dist < 400:
                    ang_rel = angulo_relativo(tanque.posicao, outro.posicao, tanque.angulo)
                    # Cone de visão frontal: ±60° da direção do tanque
                    if abs(ang_rel) <= 60:
                        inimigos_proximos.append({
                            'distancia': dist,
                            'angulo_relativo': ang_rel,
                            'vida': outro.vida
                        })
                    
        inimigos_proximos.sort(key=lambda x: x['distancia'])

        parede_frente = self.collision.get_distancia_parede_frente(tanque.posicao[0], tanque.posicao[1], tanque.angulo)
        parede_direita = self.collision.get_distancia_parede_frente(tanque.posicao[0], tanque.posicao[1], tanque.angulo - 90)
        parede_esquerda = self.collision.get_distancia_parede_frente(tanque.posicao[0], tanque.posicao[1], tanque.angulo + 90)
        
        balas_prox = []
        for b in self.balas:
            if b.dono != tanque.nome:
                dist = distancia(tanque.posicao, b.posicao)
                if dist < 200:
                    ang_rel = angulo_relativo(tanque.posicao, b.posicao, tanque.angulo)
                    balas_prox.append({'distancia': dist, 'angulo_relativo': ang_rel})

        return Sensor(
            inimigos_proximos=inimigos_proximos,
            parede_frente=parede_frente,
            parede_direita=parede_direita,
            parede_esquerda=parede_esquerda,
            propria_vida=tanque.vida,
            propria_municao=tanque.municao,
            posicao_atual=tanque.posicao,
            balas_proximas=balas_prox
        )

    def _executar_acao(self, tanque: Tank, dt: float, sensores: Sensor):
        """Executa a ação atual do tanque (uma por vez, sequencial)."""
        acao = tanque._acao_atual
        if acao is None:
            return
        
        tipo = acao.action_type
        
        if tipo == Action.ATIRAR:
            if tanque._consumir_municao():
                rad = math.radians(tanque.angulo)
                bx = tanque.posicao[0] + math.cos(rad) * 19
                by = tanque.posicao[1] - math.sin(rad) * 19
                self.balas.append(Bullet(bx, by, tanque.angulo, tanque.nome))
            tanque._avancar_acao()
            
        elif tipo == Action.MOVER_FRENTE:
            rad = math.radians(tanque.angulo)
            passo = tanque.velocidade * (dt * 60)
            if acao.valor is not None:
                faltante = acao.valor - tanque._progresso_acao
                passo = min(passo, faltante)
            dx = math.cos(rad) * passo
            dy = -math.sin(rad) * passo
            pos_antes = tanque.posicao
            colidiu = self.collision.mover_tanque_com_colisao(tanque, dx, dy, self.tanques)
            movimento_real = math.hypot(tanque.posicao[0] - pos_antes[0], tanque.posicao[1] - pos_antes[1])
            
            # Verificação mais tolerante: só avança se quase não moveu por vários frames
            if colidiu or (passo > 0 and movimento_real < passo * 0.3):
                tanque._frames_parado += 1
                if tanque._frames_parado >= 10:  # 10 frames (~160ms) antes de avançar
                    tanque._frames_parado = 0
                    tanque._avancar_acao()
            else:
                tanque._frames_parado = 0
                tanque._progresso_acao += movimento_real
                if acao.valor is not None and tanque._progresso_acao >= acao.valor:
                    tanque._avancar_acao()
                
        elif tipo == Action.MOVER_TRAS:
            rad = math.radians(tanque.angulo)
            passo = (tanque.velocidade / 2) * (dt * 60)
            if acao.valor is not None:
                faltante = acao.valor - tanque._progresso_acao
                passo = min(passo, faltante)
            dx = -math.cos(rad) * passo
            dy = math.sin(rad) * passo
            pos_antes = tanque.posicao
            colidiu = self.collision.mover_tanque_com_colisao(tanque, dx, dy, self.tanques)
            movimento_real = math.hypot(tanque.posicao[0] - pos_antes[0], tanque.posicao[1] - pos_antes[1])
            
if colidiu or (passo > 0 and movimento_real < passo * 0.3):
                tanque._frames_parado += 1
                if tanque._frames_parado >= 10:
                    tanque._frames_parado = 0
                    tanque._avancar_acao()
            else:
                tanque._frames_parado = 0
                tanque._progresso_acao += movimento_real
                if acao.valor is not None and tank_progresso_acao >= acao.valor:
                    tanque._avancar_acao()
                
        elif tipo == Action.GIRAR_ESQUERDA:
            passo = 3.0 * (dt * 60)
            if acao.valor is not None:
                faltante = acao.valor - tank_progresso_acao
                passo = min(passo, faltante)
            tank_set_angulo(tanque.angulo + passo)
            tanque._progresso_acao += passo
            if acao.valor is not None and tank_progresso_acao >= acao.valor - 1:
                tanque._avancar_acao()
                
        elif tipo == Action.GIRAR_DIREITA:
            passo = 3.0 * (dt * 60)
            if acao.valor is not None:
                faltante = acao.valor - tank_progresso_acao
                passo = min(passo, faltante)
            tank_set_angulo(tanque.angulo - passo)
            tank_progresso_acao += passo
            if acao.valor is not None and tank_progresso_acao >= acao.valor - 1:
                tanque._avancar_acao()
         
        elif tipo == Action.MIRAR:
            # Gira até encarar o inimigo mais próximo (busca em 360°)
            alvo = self._encontrar_inimigo_mais_proximo(tanque)
            if alvo is None:
                tanque._avancar_acao()  # Sem inimigo vivo, pula
                return
            ang_rel = alvo['angulo_relativo']
            if abs(ang_rel) < 3:
                tanque._avancar_acao()  # Já está mirando, avança
            else:
                passo = min(abs(ang_rel), 3.0 * (dt * 60))
                if ang_rel > 0:
                    tanque._set_angulo(tanque.angulo + passo)
                else:
                    tanque._set_angulo(tanque.angulo - passo)
        
        elif tipo == Action.PERSEGUIR:
            # Gira em direção ao inimigo E avança ao mesmo tempo (busca em 360°)
            alvo = self._encontrar_inimigo_mais_proximo(tanque)
            if alvo is None:
                tanque._avancar_acao()  # Sem inimigo vivo, pula
                return
            
            # 1. Girar em direção ao inimigo
            ang_rel = alvo['angulo_relativo']
            if abs(ang_rel) > 2:
                passo_giro = min(abs(ang_rel), 4.0 * (dt * 60))
                if ang_rel > 0:
                    tanque._set_angulo(tanque.angulo + passo_giro)
                else:
                    tanque._set_angulo(tanque.angulo - passo_giro)
            
            # 2. Avançar em direção ao inimigo
            rad = math.radians(tanque.angulo)
            passo = tanque.velocidade * (dt * 60)
            dx = math.cos(rad) * passo
            dy = -math.sin(rad) * passo
            pos_antes = tanque.posicao
            colidiu = self.collision.mover_tanque_com_colisao(tanque, dx, dy, self.tanques)
            movimento_real = math.hypot(tanque.posicao[0] - pos_antes[0], tanque.posicao[1] - pos_antes[1])
            
            # Se colidiu ou progresso muito lento, pula ação
            if colidiu or (passo > 0 and movimento_real < passo * 0.5):
                tanque._avancar_acao()
            else:
                if acao.valor is not None:
                    tanque._progresso_acao += movimento_real
                    if tanque._progresso_acao >= acao.valor:
                        tanque._avancar_acao()
    
    def _encontrar_inimigo_mais_proximo(self, tanque: Tank):
        """Busca o inimigo vivo mais próximo em 360° (para PERSEGUIR/MIRAR)."""
        mais_proximo = None
        menor_dist = float('inf')
        for outro in self.tanques:
            if outro is not tanque and outro._esta_vivo():
                dist = distancia(tanque.posicao, outro.posicao)
                if dist < menor_dist:
                    menor_dist = dist
                    ang_rel = angulo_relativo(tanque.posicao, outro.posicao, tanque.angulo)
                    mais_proximo = {'distancia': dist, 'angulo_relativo': ang_rel}
        return mais_proximo

    def executar_batalha(self) -> Dict[str, int]:
        """Retorna os scores da batalha."""
        rodando = True
        
        while rodando and self.tempo_batalha > 0:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    rodando = False

            dt = self.renderer.atualizar_fps()
            self.tempo_batalha -= dt

            # 1. Decisão e Execução dos Tanques
            for tanque in self.tanques:
                if not tanque._esta_vivo():
                    continue
                    
                tanque._atualizar(dt)
                sensores = self._gerar_sensores(tanque)
                
                try:
                    tanque.decidir(sensores)
                except Exception as e:
                    print(f"[ERRO] Tanque {tanque.nome} quebrou no decidir(): {e}")
                
                self._executar_acao(tanque, dt, sensores)

            # 2. Atualizar Balas
            for bala in self.balas:
                bala.atualizar(dt)
            
            # 3. Colisões
            self.balas = self.collision.verificar_colisao_balas(self.balas, self.tanques, self.scores)
            
            # Checa kills
            vivos = 0
            for tanque in self.tanques:
                if tanque.vida > 0:
                    vivos += 1
            
            # 4. Renderização
            self.renderer.desenhar_frame(self.tanques, self.balas, self.tempo_batalha, self.scores)
            
            if vivos <= 1:
                time.sleep(1)
                break

        return self.scores
