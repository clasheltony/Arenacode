import pygame
import math
import random
from typing import List
from core.tank import Tank
from core.bullet import Bullet
from engine.arena import Arena

class Renderer:
    def __init__(self, arena: Arena):
        pygame.init()
        self.arena = arena
        self.tela = pygame.display.set_mode((arena.largura, arena.altura))
        pygame.display.set_caption("ArenaCode - Batalha de Tanques")
        
        self.fonte = pygame.font.SysFont("bebasneueregular", 18)
        self.fonte_placar = pygame.font.SysFont("bebasneueregular", 26)
        self.fonte_estado = pygame.font.SysFont("bebasneueregular", 14)
        self.fonte_pequena = pygame.font.SysFont("bebasneueregular", 12)
        import os
        fonte_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Digital Display.ttf")
        self.fonte_timer = pygame.font.Font(fonte_path, 38)
        self.relogio = pygame.time.Clock()
        
        self.particulas = []
        self.explosoes = []
        self.rastros_balas = {}
        
        self._nomes_estado = {
            "patrulhando": "PATRULHANDO",
            "atacando": "ATACANDO",
            "sob_ataque": "SOB ATAQUE",
            "fugindo": "FUGINDO",
        }
        self._cores_estado = {
            "patrulhando": (100, 200, 255),
            "atacando": (255, 80, 80),
            "sob_ataque": (255, 200, 50),
            "fugindo": (255, 150, 255),
        }
        
        self._cores = {
            "fundo": (25, 27, 35),
            "grade": (40, 45, 55),
            "borda": (80, 90, 100),
            "zona_perigosa": (60, 40, 40),
            "parede": (70, 120, 140),
        }

    def desenhar_frame(self, tanques: List[Tank], balas: List[Bullet], tempo_restante: float, scores: dict[str, int]):
        self._desenhar_arena()
        self._desenhar_zonas()
        
        for tanque in tanques:
            if tanque._esta_vivo():
                if tanque.vida < 30:
                    for _ in range(1):
                        self.particulas.append({
                            'x': tanque.posicao[0], 'y': tanque.posicao[1],
                            'vx': random.uniform(-0.8, 0.8), 'vy': random.uniform(-0.8, 0.8),
                            'vida': random.uniform(0.4, 0.7),
                            'cor': (120, 70, 50),
                            'tipo': 'fumaca'
                        })
                self._desenhar_tanque(tanque)
        
        for bala in balas:
            if bala.dono not in self.rastros_balas:
                self.rastros_balas[bala.dono] = []
            self.rastros_balas[bala.dono].append((bala.x, bala.y))
            if len(self.rastros_balas[bala.dono]) > 6:
                self.rastros_balas[bala.dono].pop(0)
            self._desenhar_bala(bala)
        
        self._atualizar_particulas()
        self._atualizar_explosoes()
        self._desenhar_hud(tanques, tempo_restante, scores)
        
        pygame.display.flip()

    def _desenhar_arena(self):
        self.tela.fill(self._cores["fundo"])
        
        border = 8
        pygame.draw.rect(self.tela, self._cores["borda"], (0, 0, self.arena.largura, self.arena.altura), border)
        
        for x in range(40, self.arena.largura - 40, 40):
            pygame.draw.line(self.tela, self._cores["grade"], (x, border), (x, self.arena.altura - border), 1)
        for y in range(40, self.arena.altura - 40, 40):
            pygame.draw.line(self.tela, self._cores["grade"], (border, y), (self.arena.largura - border, y), 1)

    def _desenhar_zonas(self):
        centro_x, centro_y = self.arena.largura // 2, self.arena.altura // 2
        raio = 100
        
        for i in range(3, 0, -1):
            raio_atual = raio * i // 3
            pygame.draw.circle(self.tela, (50 + i * 10, 35, 35), (centro_x, centro_y), raio_atual, 1)

    def _desenhar_tanque(self, tanque: Tank):
        x, y = int(tanque.posicao[0]), int(tanque.posicao[1])
        cor = tanque.cor
        ang = tanque.angulo
        rad = math.radians(ang)
        
        def rot(px, py):
            rx = px * math.cos(rad) + py * math.sin(rad)
            ry = -px * math.sin(rad) + py * math.cos(rad)
            return (x + rx, y + ry)
        
        esteiras_pts = [
            [rot(-15, -14), rot(15, -14), rot(15, -8), rot(-15, -8)],
            [rot(-15, 8), rot(15, 8), rot(15, 14), rot(-15, 14)],
        ]
        for pts in esteiras_pts:
            pygame.draw.polygon(self.tela, (55, 60, 70), pts)
        
        corpo_pts = [
            rot(-12, -12), rot(12, -12), rot(12, 12), rot(-12, 12)
        ]
        pygame.draw.polygon(self.tela, cor, corpo_pts)
        pygame.draw.polygon(self.tela, self._clarear(cor, 25), corpo_pts, 2)
        
        pygame.draw.circle(self.tela, self._escurer(cor, 25), (x, y), 5)
        pygame.draw.circle(self.tela, self._clarear(cor, 35), (x, y), 3)
        
        canhao_inicio = rot(7, 0)
        canhao_fim = rot(22, 0)
        pygame.draw.line(self.tela, self._escurer(cor, 35), canhao_inicio, canhao_fim, 5)
        pygame.draw.line(self.tela, (175, 175, 185), canhao_inicio, canhao_fim, 2)
        
        pygame.draw.circle(self.tela, (195, 195, 205), canhao_fim, 3)
        
        texto_nome = self.fonte.render(tanque.nome[:10], True, (215, 215, 215))
        self.tela.blit(texto_nome, (x - texto_nome.get_width() // 2, y - 32))
        
        estado = getattr(tanque, '_estado_atual', 'patrulhando')
        nome_estado = self._nomes_estado.get(estado, estado)
        cor_estado = self._cores_estado.get(estado, (200, 200, 200))
        texto_estado = self.fonte_pequena.render(nome_estado, True, cor_estado)
        self.tela.blit(texto_estado, (x - texto_estado.get_width() // 2, y + 22))

    def _desenhar_bala(self, bala: Bullet):
        rastros = self.rastros_balas.get(bala.dono, [])
        for idx, (rx, ry) in enumerate(rastros[:-1]):
            pygame.draw.circle(self.tela, (200, 200, 80), (int(rx), int(ry)), 2)
        
        pygame.draw.circle(self.tela, (255, 255, 190), (int(bala.x), int(bala.y)), bala.raio + 2)
        pygame.draw.circle(self.tela, (255, 255, 0), (int(bala.x), int(bala.y)), bala.raio)
        pygame.draw.circle(self.tela, (255, 255, 255), (int(bala.x), int(bala.y)), 1)

    def _desenhar_hud(self, tanques: List[Tank], tempo_restante: float, scores: dict):
        # Timer no topo (estilo digital)
        tempo_str = f"{int(tempo_restante):02d}"
        texto_tempo = self.fonte_timer.render(tempo_str, True, (0, 255, 0) if tempo_restante > 10 else (255, 50, 0))
        
        # Fundo do timer
        timer_x = self.arena.largura // 2 - texto_tempo.get_width() // 2
        timer_y = 10
        pygame.draw.rect(self.tela, (10, 12, 18), (timer_x - 10, timer_y - 5, texto_tempo.get_width() + 20, texto_tempo.get_height() + 10))
        pygame.draw.rect(self.tela, (50, 60, 70), (timer_x - 10, timer_y - 5, texto_tempo.get_width() + 20, texto_tempo.get_height() + 10), 1)
        
        self.tela.blit(texto_tempo, (timer_x, timer_y))
        
        # Barra inferior com info dos tanques
        barra_y = self.arena.altura - 45
        
        pygame.draw.rect(self.tela, (18, 20, 28), (0, barra_y, self.arena.largura, 45))
        pygame.draw.line(self.tela, (85, 95, 110), (0, barra_y), (self.arena.largura, barra_y), 2)
        
        x_info = 25
        espacamento = 280
        
        for i, tanque in enumerate(tanques):
            x_pos = x_info + i * espacamento
            
            # Nome do tanque
            nome_cor = tanque.cor if tanque._esta_vivo() else (90, 90, 90)
            nome_tank = self.fonte.render(tanque.nome[:10], True, nome_cor)
            self.tela.blit(nome_tank, (x_pos, barra_y + 3))
            
            # Pontos
            s_data = scores.get(tanque.nome, {})
            # Se for dicionário (novo sistema), pega o total. Se for int (antigo), usa direto.
            pts = s_data.get("total", 0) if isinstance(s_data, dict) else s_data
            pts_txt = self.fonte.render(f"{pts} pts", True, (180, 180, 180))
            self.tela.blit(pts_txt, (x_pos + 85, barra_y + 3))
            
            # Barras de vida e energia
            vida_x = x_pos + 145
            vida_y = barra_y + 6
            # Vida
            pygame.draw.rect(self.tela, (35, 18, 18), (vida_x, vida_y, 70, 7))
            if tanque._esta_vivo():
                vida_pct = max(0, tanque.vida / 100.0)
                cor_vida = (50, 200, 50) if vida_pct > 0.3 else (200, 50, 50)
                pygame.draw.rect(self.tela, cor_vida, (vida_x, vida_y, int(70 * vida_pct), 7))
                
                # Energia (Barra Azul)
                eng_y = barra_y + 16
                pygame.draw.rect(self.tela, (15, 15, 30), (vida_x, eng_y, 70, 5))
                eng_pct = max(0, tanque.energia / 100.0)
                pygame.draw.rect(self.tela, (80, 160, 255), (vida_x, eng_y, int(70 * eng_pct), 5))
            else:
                texto_morto = self.fonte_pequena.render("DEST", True, (140, 50, 50))
                self.tela.blit(texto_morto, (vida_x, vida_y - 1))
            
            # Munição
            mun = self.fonte.render(f"M:{tanque.municao}", True, (150, 150, 150))
            self.tela.blit(mun, (x_pos + 225, barra_y + 8))

    def _atualizar_particulas(self):
        novas = []
        for p in self.particulas:
            p['x'] += p['vx']
            p['y'] += p['vy']
            p['vida'] -= 0.025
            
            if p['vida'] > 0:
                if p['tipo'] == 'fumaca':
                    raio = int(6 * p['vida'])
                    pygame.draw.circle(self.tela, p['cor'], (int(p['x']), int(p['y'])), max(1, raio))
                novas.append(p)
        self.particulas = novas

    def _atualizar_explosoes(self):
        novas = []
        for e in self.explosoes:
            e['timer'] -= 1
            if e['timer'] > 0:
                raio = e['raio'] * (1 - e['timer'] / 15)
                for _ in range(2):
                    ang = random.uniform(0, 6.28)
                    dist = random.uniform(3, raio)
                    px = e['x'] + math.cos(ang) * dist
                    py = e['y'] + math.sin(ang) * dist
                    pygame.draw.circle(self.tela, (255, 150, 50), (int(px), int(py)), 2)
                novas.append(e)
        self.explosoes = novas

    def criar_explosao(self, x, y):
        self.explosoes.append({'x': x, 'y': y, 'timer': 12, 'raio': 20})

    def _clarear(self, cor, amount):
        return tuple(min(255, c + amount) for c in cor)

    def _escurer(self, cor, amount):
        return tuple(max(0, c - amount) for c in cor)

    def atualizar_fps(self):
        return self.relogio.tick(60) / 1000.0

    def fechar(self):
        pygame.quit()