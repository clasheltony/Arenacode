from core.tank import Tank
from core.action import Action

class sameque(Tank):
    def __init__(self):
        super().__init__(nome="sameque", cor=(50, 50, 255))

    def programar(self):
        # Patrulhar: anda 150px, gira 90 para a esquerda (patrulha em quadrado)
        self.patrulhar([
            Action.MOVER_FRENTE(200),
            Action.GIRAR_ALEATORIO (90),
            Action.VARREDURA_RADAR(360)
            
        ])
        
        # Inimigo encontrado: persegue 50px, mira no inimigo e atira (loop)
        self.inimigo_encontrado([
            Action.PERSEGUIR(150),
            Action.MIRAR,
            Action.ATIRAR_MEDIA,
            Action.ATIRAR_FRACA
            
        ])
        
        # Recebendo ataque: gira 90 e foge 100px
        self.recebendo_ataque([
            Action.GIRAR_DIREITA(90),
            Action.MOVER_FRENTE(100),
            Action.MIRAR,
            Action.ATIRAR_MEDIA
        ])
        
        # Fugir: daocio 80px e gira 90 (foge em zigue-zague)
        self.fugir([
            Action.MOVER_TRAS(50),
            Action.GIRAR_ESQUERDA(90),
            Action.MIRAR,
            Action.ATIRAR_FRACA,
        ])
        
        # Inimigo encontrado: persegue 50px, mira no inimigo e atira (loop)
        self.inimigo_encontrado([
            Action.PERSEGUIR(50),
            Action.MIRAR,
            Action.ATIRAR_FORTE
        ])
        
        # Recebendo ataque: gira 90° e foge 100px
        self.recebendo_ataque([
            Action.MOVER_FRENTE(100),
            Action.GIRAR_DIREITA(90),
            Action.MOVER_FRENTE(100)
        ])
        
        # Fugir: dá ré 80px e gira 90° (foge em zigue-zague)
        self.fugir([
            Action.MOVER_TRAS(50),
            Action.GIRAR_ESQUERDA(90),
            Action.MIRAR,
            Action.ATIRAR,


        ])
