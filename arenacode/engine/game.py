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

        self.scores = {
            t.nome: {
                "vitoria": 0,
                "dano_causado": 0,
                "acertos": 0,
                "erros": 0,
                "destruicoes": 0,
                "destruido": 0,
                "sobrevivencia": 0,
                "total": 0
            } for t in self.tanques
        }
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
        
        if tipo in [Action.ATIRAR, Action.ATIRAR_FRACA, Action.ATIRAR_MEDIA, Action.ATIRAR_FORTE]:
            # Definir parâmetros baseados no tipo de tiro
            custo = 50
            dano = 6
            velocidade = 11.0
            
            if tipo == Action.ATIRAR_FRACA:
                custo = 10
                dano = 3
                velocidade = 7.0
            elif tipo == Action.ATIRAR_FORTE:
                custo = 80
                dano = 12
                velocidade = 16.0
                
            if tanque._consumir_municao(custo):
                rad = math.radians(tanque.angulo)
                bx = tanque.posicao[0] + math.cos(rad) * 19
                by = tanque.posicao[1] - math.sin(rad) * 19
                self.balas.append(Bullet(bx, by, tanque.angulo, tanque.nome, velocidade, dano))
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
            colidiu, bateu_parede = self.collision.mover_tanque_com_colisao(tanque, dx, dy, self.tanques)
            movimento_real = math.hypot(tanque.posicao[0] - pos_antes[0], tanque.posicao[1] - pos_antes[1])
            
            if bateu_parede:
                # Regra: Girar 90 e Ir pra frente
                tanque._sequencia_recuperacao = [
                    Action.GIRAR_DIREITA(90),
                    Action.MOVER_FRENTE(60)
                ]
                tanque._indice_acao = 0
                tanque._progresso_acao = 0.0
                return

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
            colidiu, bateu_parede = self.collision.mover_tanque_com_colisao(tanque, dx, dy, self.tanques)
            movimento_real = math.hypot(tanque.posicao[0] - pos_antes[0], tanque.posicao[1] - pos_antes[1])
            
            if bateu_parede:
                tanque._sequencia_recuperacao = [
                    Action.GIRAR_DIREITA(90),
                    Action.MOVER_FRENTE(60)
                ]
                tanque._indice_acao = 0
                tanque._progresso_acao = 0.0
                return

            if colidiu or (passo > 0 and movimento_real < passo * 0.3):
                tanque._frames_parado += 1
                if tanque._frames_parado >= 10:
                    tanque._frames_parado = 0
                    tanque._avancar_acao()
            else:
                tanque._frames_parado = 0
                tanque._progresso_acao += movimento_real
                if acao.valor is not None and tanque._progresso_acao >= acao.valor:
                    tanque._avancar_acao()
                
        elif tipo == Action.GIRAR_ESQUERDA:
            passo = 3.0 * (dt * 60)
            if acao.valor is not None:
                faltante = acao.valor - tanque._progresso_acao
                passo = min(passo, faltante)
            tanque._set_angulo(tanque.angulo + passo)
            tanque._progresso_acao += passo
            if acao.valor is not None and tanque._progresso_acao >= acao.valor - 1:
                tanque._avancar_acao()
                
        elif tipo == Action.GIRAR_DIREITA:
            passo = 3.0 * (dt * 60)
            if acao.valor is not None:
                faltante = acao.valor - tanque._progresso_acao
                passo = min(passo, faltante)
            tanque._set_angulo(tanque.angulo - passo)
            tanque._progresso_acao += passo
            if acao.valor is not None and tanque._progresso_acao >= acao.valor - 1:
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
            colidiu, bateu_parede = self.collision.mover_tanque_com_colisao(tanque, dx, dy, self.tanques)
            movimento_real = math.hypot(tanque.posicao[0] - pos_antes[0], tanque.posicao[1] - pos_antes[1])
            
            if bateu_parede:
                tanque._sequencia_recuperacao = [
                    Action.GIRAR_DIREITA(90),
                    Action.MOVER_FRENTE(60)
                ]
                tanque._indice_acao = 0
                tanque._progresso_acao = 0.0
                return

            # Se colidiu ou progresso muito lento, pula ação
            if colidiu or (passo > 0 and movimento_real < passo * 0.5):
                tanque._avancar_acao()
            else:
                if acao.valor is not None:
                    tanque._progresso_acao += movimento_real
                    if tanque._progresso_acao >= acao.valor:
                        tanque._avancar_acao()

        elif tipo == Action.ATIRAR_CERTEIRO:
            alvo = self._encontrar_inimigo_mais_proximo(tanque)
            if alvo:
                if abs(alvo['angulo_relativo']) <= 5:
                    if tanque._consumir_municao(25):
                        rad = math.radians(tanque.angulo)
                        bx = tanque.posicao[0] + math.cos(rad) * 19
                        by = tanque.posicao[1] - math.sin(rad) * 19
                        self.balas.append(Bullet(bx, by, tanque.angulo, tanque.nome, 11.0, 6))
            tanque._avancar_acao() # Sempre avança para não travar a patrulha

        elif tipo == Action.MOVER_SEGURO:
            if sensores.parede_frente < 50:
                tanque._avancar_acao() # Perigo! Para o movimento
            else:
                # Lógica idêntica ao MOVER_FRENTE
                rad = math.radians(tanque.angulo)
                passo = tanque.velocidade * (dt * 60)
                if acao.valor is not None:
                    faltante = acao.valor - tanque._progresso_acao
                    passo = min(passo, faltante)
                dx = math.cos(rad) * passo
                dy = -math.sin(rad) * passo
                pos_antes = tanque.posicao
                colidiu, bateu_parede = self.collision.mover_tanque_com_colisao(tanque, dx, dy, self.tanques)
                movimento_real = math.hypot(tanque.posicao[0] - pos_antes[0], tanque.posicao[1] - pos_antes[1])
                
                if bateu_parede:
                    tanque._sequencia_recuperacao = [Action.GIRAR_DIREITA(90), Action.MOVER_FRENTE(60)]
                    tanque._indice_acao = 0
                    tanque._progresso_acao = 0.0
                    return

                tanque._progresso_acao += movimento_real
                if acao.valor is not None and tanque._progresso_acao >= acao.valor:
                    tanque._avancar_acao()
                elif colidiu:
                    tanque._avancar_acao()

        elif tipo == Action.VARREDURA_RADAR:
            if sensores.inimigos_proximos:
                tanque._avancar_acao() # Encontrou!
            else:
                passo = 3.0 * (dt * 60)
                if acao.valor is not None:
                    faltante = acao.valor - tanque._progresso_acao
                    passo = min(passo, faltante)
                tanque._set_angulo(tanque.angulo - passo) # Gira para a direita na varredura
                tanque._progresso_acao += passo
                if acao.valor is not None and tanque._progresso_acao >= acao.valor - 1:
                    tanque._avancar_acao()

        elif tipo == Action.GIRAR_ALEATORIO:
            if acao.valor is None:
                acao.valor = random.uniform(45, 180)
            
            passo = 4.0 * (dt * 60)
            faltante = acao.valor - tanque._progresso_acao
            passo = min(passo, faltante)
            tanque._set_angulo(tanque.angulo + passo)
            tanque._progresso_acao += passo
            if tanque._progresso_acao >= acao.valor - 1:
                acao.valor = None # Reseta para o próximo uso
                tanque._avancar_acao()

        elif tipo == Action.MANTER_DISTANCIA:
            alvo = self._encontrar_inimigo_mais_proximo(tanque)
            if alvo:
                dist_atual = alvo['distancia']
                dist_alvo = acao.valor if acao.valor else 250
                erro = dist_atual - dist_alvo
                
                if abs(erro) < 20:
                    tanque._avancar_acao() # Distância atingida
                else:
                    rad = math.radians(tanque.angulo)
                    # Se erro > 0, precisa aproximar (mover frente)
                    # Se erro < 0, precisa afastar (mover tras)
                    sentido = 1 if erro > 0 else -1
                    passo = (tanque.velocidade * 0.8) * (dt * 60) * sentido
                    
                    dx = math.cos(rad) * passo
                    dy = -math.sin(rad) * passo
                    self.collision.mover_tanque_com_colisao(tanque, dx, dy, self.tanques)
            else:
                tanque._avancar_acao()

        elif tipo == Action.ESQUIVA_SMART:
            # Procura balas vindo na direção (ângulo relativo frontal)
            perigo = False
            for b in sensores.balas_proximas:
                if abs(b['angulo_relativo']) < 30: # Bala vindo de frente
                    perigo = True
                    break
            
            if perigo:
                # Manobra de esquiva: Gira 90 e move um pouco
                tanque._sequencia_recuperacao = [
                    Action.GIRAR_DIREITA(90),
                    Action.MOVER_FRENTE(50)
                ]
                tanque._indice_acao = 0
                tanque._progresso_acao = 0.0
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
            for t_nome, s in self.scores.items():
                # Durante a batalha, o total é o parcial de acertos/erros/dano
                s["total"] = (s["dano_causado"] * 2) + (s["acertos"] * 10) + (s["erros"] * -2) + (s.get("destruicoes", 0) * 50)
                # Penalidade de morte instantânea no HUD
                tanque_obj = next((t for t in self.tanques if t.nome == t_nome), None)
                if tanque_obj and not tanque_obj._esta_vivo():
                    s["total"] -= 50

            self.renderer.desenhar_frame(self.tanques, self.balas, self.tempo_batalha, self.scores)
            
            if vivos <= 1:
                time.sleep(1)
                break

        # Finalizar Pontuação
        vencedor_unico = None
        if vivos == 1:
            for t in self.tanques:
                if t._esta_vivo():
                    vencedor_unico = t
                    break
        
        for tanque in self.tanques:
            s = self.scores[tanque.nome]
            
            # Sobrevivência ou Vitória
            if tanque._esta_vivo():
                if vencedor_unico == tanque and len(self.tanques) > 1:
                    # Só ganha vitória se destruiu TODOS os outros (vivos == 1)
                    s["vitoria"] = 100
                else:
                    s["sobrevivencia"] = 25
            else:
                s["destruido"] = -50
            
            # Cálculo do Total
            # Vitória (+100) ou Sobrevivência (+25) ou Destruído (-50)
            # Dano (+2 por 1 de dano)
            # Acertos (+10)
            # Erros (-2)
            s["total"] = (
                s["vitoria"] + 
                s["sobrevivencia"] + 
                s["destruido"] + 
                (s["dano_causado"] * 2) + 
                (s["acertos"] * 10) + 
                (s["erros"] * -2) +
                (s.get("destruicoes", 0) * 50)
            )

        return self.scores
