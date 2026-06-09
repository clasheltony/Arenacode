import math
from typing import List, Tuple
from core.tank import Tank
from core.bullet import Bullet
from engine.arena import Arena

def distancia(p1: Tuple[float, float], p2: Tuple[float, float]) -> float:
    return math.hypot(p2[0] - p1[0], p2[1] - p1[1])

def angulo_relativo(p1: Tuple[float, float], p2: Tuple[float, float], angulo_base: float) -> float:
    dx = p2[0] - p1[0]
    dy = p1[1] - p2[1]
    ang = math.degrees(math.atan2(dy, dx))
    if ang < 0:
        ang += 360
    
    relativo = ang - angulo_base
    if relativo < -180: relativo += 360
    if relativo > 180: relativo -= 360
    return relativo

class CollisionSystem:
    def __init__(self, arena: Arena):
        self.arena = arena
        self.raio_tanque = 16.0
        self.borda = 10
        self.menu_altura = 50
        self.timer_altura = 50
        
    def get_distancia_parede_frente(self, x: float, y: float, angulo: float) -> float:
        rad = math.radians(angulo)
        
        step_x = math.cos(rad) * 5
        step_y = -math.sin(rad) * 5
        
        dist = 0
        curr_x, curr_y = x, y
        
        max_x = self.arena.largura - self.borda
        max_y = self.arena.altura - self.borda - self.menu_altura
        
        while self.borda <= curr_x <= max_x and self.timer_altura <= curr_y <= max_y:
            curr_x += step_x
            curr_y += step_y
            dist += 5
            if dist > 500:
                break
        
        return dist
        
    def mover_tanque_com_colisao(self, tanque: Tank, dx: float, dy: float, outros_tanques: List[Tank]) -> Tuple[bool, bool]:
        colidiu = False
        bateu_parede = False
        pos_x, pos_y = tanque.posicao
        novo_x = pos_x + dx
        novo_y = pos_y + dy
        
        min_x = self.borda + self.raio_tanque
        max_x = self.arena.largura - self.borda - self.raio_tanque
        min_y = self.timer_altura + self.raio_tanque
        max_y = self.arena.altura - self.menu_altura - self.raio_tanque
        
        if novo_x < min_x or novo_x > max_x:
            colidiu = True
            bateu_parede = True
        if novo_y < min_y or novo_y > max_y:
            colidiu = True
            bateu_parede = True
        
        novo_x = max(min_x, min(max_x, novo_x))
        novo_y = max(min_y, min(max_y, novo_y))
        
        for outro in outros_tanques:
            if outro is not tanque and outro._esta_vivo():
                dist = math.hypot(novo_x - outro.posicao[0], novo_y - outro.posicao[1])
                min_dist = self.raio_tanque * 2
                if dist < min_dist:
                    colidiu = True
                    bateu_parede = True
                    if dist == 0: dist = 0.001
                    overlap = min_dist - dist
                    nx = (novo_x - outro.posicao[0]) / dist
                    ny = (novo_y - outro.posicao[1]) / dist
                    novo_x += nx * overlap
                    novo_y += ny * overlap

        novo_x = max(min_x, min(max_x, novo_x))
        novo_y = max(min_y, min(max_y, novo_y))

        tanque._set_posicao(novo_x, novo_y)
        return colidiu, bateu_parede

    def verificar_colisao_balas(self, balas: List[Bullet], tanques: List[Tank], scores: dict) -> List[Bullet]:
        balas_ativas = []
        
        min_x = self.borda
        max_x = self.arena.largura - self.borda
        min_y = self.timer_altura
        max_y = self.arena.altura - self.borda
        
        for bala in balas:
            destruir = False
            
            # 1. Saiu da tela (Erro)
            if not (min_x <= bala.x <= max_x and min_y <= bala.y <= max_y):
                if bala.dono in scores:
                    scores[bala.dono]["erros"] += 1
                destruir = True
            
            # 2. Obstáculos (Erro/Parede)
            if not destruir and self.arena.obstaculos:
                for ox, oy, ow, oh in self.arena.obstaculos:
                    if ox <= bala.x <= ox + ow and oy <= bala.y <= oy + oh:
                        if bala.dono in scores:
                            scores[bala.dono]["erros"] += 1
                        destruir = True
                        break
            
            # 3. Tanques (Acerto)
            if not destruir:
                for tanque in tanques:
                    if tanque._esta_vivo() and tanque.nome != bala.dono:
                        if distancia(bala.posicao, tanque.posicao) < (self.raio_tanque + bala.raio):
                            if bala.dono in scores:
                                s = scores[bala.dono]
                                s["acertos"] += 1
                                s["dano_causado"] += bala.dano
                            tanque._receber_dano(bala.dano)
                            
                            # Se o tanque foi destruído por esta bala
                            if not tanque._esta_vivo():
                                if bala.dono in scores:
                                    # Bônus por destruição: +50 pontos
                                    if "destruicoes" not in scores[bala.dono]:
                                        scores[bala.dono]["destruicoes"] = 0
                                    scores[bala.dono]["destruicoes"] += 1
                                    scores[bala.dono]["total"] += 50
                            
                            # Recuperar munição (1 a cada 5 acertos)
                            atirador = next((t for t in tanques if t.nome == bala.dono), None)
                            if atirador:
                                atirador._registrar_acerto()
                                
                            destruir = True
                            break
            
            if not destruir:
                balas_ativas.append(bala)
        
        return balas_ativas