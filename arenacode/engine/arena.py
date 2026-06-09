class Arena:
    LARGURA = 900
    ALTURA = 700

    def __init__(self):
        self.largura = self.LARGURA
        self.altura = self.ALTURA
        self.obstaculos = []

    def get_posicoes_iniciais(self):
        return [
            (80.0, 80.0),
            (self.largura - 80.0, self.altura - 80.0),
            (80.0, self.altura - 80.0),
            (self.largura - 80.0, 80.0)
        ]