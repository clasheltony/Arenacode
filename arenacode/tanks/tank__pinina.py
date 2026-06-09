from core.tank import Tank
from core.action import Action

class Pinina(Tank):
    def __init__(self):
        super().__init__(nome="Pinina", cor=(200, 200, 30))

    def programar(self):

        self.configurar_gatilhos( vida=10, municao=1, alerta=1)
        # Patrulhar: anda 150px, gira 90 para a esquerda (patrulha em quadrado)
        self.patrulhar([
            Action.MOVER_FRENTE (50),
            Action.VARREDURA_RADAR (180),
            Action.MOVER_FRENTE(50),
            Action.MOVER_SEGURO(50)
        ])
        
        # Inimigo encontrado: persegue 50px, mira no inimigo e atira (loop)
        self.inimigo_encontrado([
           Action.MIRAR,       
            Action.ATIRAR_MEDIA   
        ])
        
        # Recebendo ataque: gira 90 e foge 100px
        self.recebendo_ataque([ 
            Action.MIRAR,         
            Action.ATIRAR_FRACA
        ])
        
        # Fugir: daocio 80px e gira 90 (foge em zigue-zague)
        self.fugir([
          Action.MOVER_TRAS(40),
            Action.GIRAR_ALEATORIO,
            Action.MIRAR,
            Action.ATIRAR_FRACA
        ])