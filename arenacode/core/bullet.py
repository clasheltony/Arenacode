import math
from typing import Tuple

class Bullet:
    """
    Representa um projétil disparado por um tanque.
    Gerenciado exclusivamente pela engine.
    """
    def __init__(self, x: float, y: float, angulo: float, dono: str, velocidade: float = 8.0, dano: int = 10):
        self.x = x
        self.y = y
        self.angulo = angulo
        self.velocidade = velocidade
        self.dono = dono  # Nome do tanque que atirou (para não dar dano a si mesmo e dar pontuação)
        self.dano = dano
        self.ativa = True
        self.raio = 3

    def atualizar(self, dt: float):
        """Move a bala de acordo com seu ângulo e velocidade."""
        # pygame y axis is inverted: up is negative y
        # math.sin and cos work with standard cartesian, so we subtract sin for Y.
        rad = math.radians(self.angulo)
        # Assumindo dt em segundos. Multiplicamos por 60 para simular a velocidade por frame base 60 FPS.
        fator = dt * 60
        self.x += math.cos(rad) * self.velocidade * fator
        self.y -= math.sin(rad) * self.velocidade * fator

    @property
    def posicao(self) -> Tuple[float, float]:
        return (self.x, self.y)
