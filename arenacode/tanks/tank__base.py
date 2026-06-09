from core.tank import Tank
from core.action import Action

class LINK(Tank):
    def __init__(self):
        super().__init__(nome="LINK", cor=(0, 255, 0))

    def programar(self):

        self.configurar_gatilhos( vida=10, municao=1, alerta=1)
        # Patrulhar: anda 150px, gira 90 para a esquerda (patrulha em quadrado)
        self.patrulhar([
            Action.MOVER_FRENTE(60),
            Action.GIRAR_DIREITA(90),
            Action.GIRAR_DIREITA(60),
            Action.MOVER_FRENTE(100) 
            
        ])
        
        # Inimigo encontrado: persegue 50px, mira no inimigo e atira (loop)
        self.inimigo_encontrado([
            Action.MIRAR,
            Action.ATIRAR_FRACA,
            Action.ATIRAR_FRACA
        ])
        
        # Recebendo ataque: gira 90 e foge 100px
        self.recebendo_ataque([
            Action.MIRAR,
            Action.ATIRAR_FRACA,
            Action.ATIRAR_FRACA
            
        ])
        
        # Fugir: daocio 80px e gira 90 (foge em zigue-zague)
        self.fugir([
            Action.GIRAR_ESQUERDA(90),
            Action.MIRAR,
            Action.ATIRAR_FORTE
        ])