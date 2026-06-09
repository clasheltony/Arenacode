import pygame
import math

class Arena:
    def __init__(self, largura, altura, tanques):
        self.largura = largura
        self.altura = altura
        self.tanques = tanques

    def atualizar(self):
        for t in self.tanques:
            inimigos = [i for i in self.tanques if i != t]

            estado = {
                "inimigos": inimigos,
                "largura": self.largura,
                "altura": self.altura
            }

            t.agir(estado)
            t.atualizar_tiros(self.largura, self.altura)

            t.x = max(0, min(self.largura, t.x))
            t.y = max(0, min(self.altura, t.y))

        self.verificar_colisoes()

    def verificar_colisoes(self):
        for t in self.tanques:
            for tiro in t.tiros[:]:
                for inimigo in self.tanques:
                    if inimigo != t:
                        dx = tiro["x"] - inimigo.x
                        dy = tiro["y"] - inimigo.y
                        dist = math.hypot(dx, dy)

                        if dist < 15:
                            inimigo.vida -= 10
                            t.tiros.remove(tiro)

    def desenhar(self, tela):
        for t in self.tanques:
            # tanque
            pygame.draw.circle(tela, t.cor, (int(t.x), int(t.y)), 15)

            # barra de vida
            pygame.draw.rect(tela, (255,0,0), (t.x-20, t.y-30, 40, 5))
            pygame.draw.rect(tela, (0,255,0), (t.x-20, t.y-30, 40*(t.vida/100), 5))

            # tiros
            for tiro in t.tiros[:]:
                pygame.draw.circle(tela, (255,255,0), (int(tiro["x"]), int(tiro["y"])), 6)