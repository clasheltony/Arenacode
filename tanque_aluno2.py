from tanque_base import TanqueBase
import math

class TanqueAluno2(TanqueBase):

    def agir(self, estado):
        inimigo = estado["inimigos"][0]

        dx = self.x - inimigo.x
        dy = self.y - inimigo.y

        self.angulo = math.atan2(dy, dx)

        # se estiver perto da borda, muda direção
        if self.x < 50 or self.x > estado["largura"] - 50:
            self.angulo += math.pi / 2

        if self.y < 50 or self.y > estado["altura"] - 50:
            self.angulo += math.pi / 2

        self.mover_frente()