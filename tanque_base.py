import math

class TanqueBase:
    def __init__(self, x, y, cor):
        self.x = x
        self.y = y
        self.angulo = 0
        self.velocidade = 2
        self.cor = cor
        self.vida = 100
        self.tiros = []
        self.cooldown = 0

    def mover_frente(self):
        self.x += math.cos(self.angulo) * self.velocidade
        self.y += math.sin(self.angulo) * self.velocidade

    def girar(self, direcao):
        self.angulo += direcao * 0.1

    def atirar(self):
        if self.cooldown == 0:
            tiro = {
                "x": self.x + math.cos(self.angulo) * 20,
                "y": self.y + math.sin(self.angulo) * 20,
                "angulo": self.angulo
            }
            self.tiros.append(tiro)
            self.cooldown = 30
            print("Atirou!!!")

    def atualizar_tiros(self, largura, altura):
        novos = []
        for t in self.tiros:
            t["x"] += math.cos(t["angulo"]) * 3
            t["y"] += math.sin(t["angulo"]) * 3

            if 0 < t["x"] < largura and 0 < t["y"] < altura:
                novos.append(t)

        self.tiros = novos

        if self.cooldown > 0:
            self.cooldown -= 1

    def agir(self, estado):
        pass