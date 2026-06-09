from tanque_base import TanqueBase
import math

class TanqueAluno1(TanqueBase):

    def agir(self, estado):
        inimigo = estado["inimigos"][0]

        dx = inimigo.x - self.x
        dy = inimigo.y - self.y

        angulo_desejado = math.atan2(dy, dx)

        # normaliza diferença de ângulo
        diff = angulo_desejado - self.angulo

        # mantém entre -pi e pi
        if diff > math.pi:
            diff -= 2 * math.pi
        if diff < -math.pi:
            diff += 2 * math.pi

        # gira na direção correta
        if diff > 0:
            self.girar(1)
        else:
            self.girar(-1)

        # 💥 AGORA ATIRA SEMPRE (com cooldown)
        self.atirar()

        self.mover_frente()