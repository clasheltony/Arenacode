from core.tank import Tank
from core.action import Action
from random import randint

class Karlos_Cezinha(Tank):
    def __init__(self):
        super().__init__(nome="ANGEL K/C", cor=(255, 255, 255))

    def programar(self):
        
        
        self.patrulhar([
            Action.MOVER_FRENTE(100),
            Action.VARREDURA_RADAR(180)
            
        ])
        
        
        self.inimigo_encontrado([
            Action.MIRAR,
            Action.ATIRAR_CERTEIRO,
            Action.ATIRAR_CERTEIRO,
            Action.ATIRAR_CERTEIRO


        ])
        
        
        self.recebendo_ataque([
            Action.MIRAR,
            Action.ATIRAR_CERTEIRO,
            Action.ATIRAR_MEDIA

        ])
        
        self.fugir([
            Action.MOVER_FRENTE(100),
            Action.VARREDURA_RADAR(180),
            Action.MIRAR,
            Action.ATIRAR_CERTEIRO,
            Action.ATIRAR_CERTEIRO
        ])
        