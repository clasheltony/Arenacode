from core.tank import Tank
from core.action import Action

class Kenim (Tank):
    def __init__(self):
        super().__init__(nome="Kenim", cor=(200, 50, 200))

    def programar(self):
        # Patrulhar: anda 200px, gira 90° para a direita (quadrado oposto ao Caçador)
        self.patrulhar([
            Action.MOVER_SEGURO(50),
            Action.VARREDURA_RADAR(180),
            Action.GIRAR_ALEATORIO,
            Action.MOVER_FRENTE(200)
           
        ])
        
        # Inimigo encontrado: atira, gira 15° para ajustar mira, atira de novo
        self.inimigo_encontrado([

            Action.MIRAR,
            Action.ATIRAR_MEDIA,
            Action.MANTER_DISTANCIA(125),
        ])
        
        # Recebendo ataque: avança e gira (contorna o inimigo)
        self.recebendo_ataque([
            
            Action.ESQUIVA_SMART,      
            Action.MIRAR,              
            Action.ATIRAR_CERTEIRO,
        ])
        
        self.fugir([
            Action.MOVER_TRAS(80),
            Action.GIRAR_ALEATORIO,
            Action.MOVER_SEGURO(150),
            Action.MIRAR,
            Action.ATIRAR_CERTEIRO

        ])
