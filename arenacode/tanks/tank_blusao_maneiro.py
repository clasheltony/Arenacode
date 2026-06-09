from core.tank import Tank
from core.action import Action

class blusao_maneiro(Tank):
    def __init__(self):
        super().__init__(nome="blusao_maneiro", cor=(255, 0, 255))
    
    def programar(self):
    
        self.configurar_gatilhos(vida=30, municao=1, alerta=4)

        self.patrulhar([
            Action.MOVER_SEGURO (180),
            Action.VARREDURA_RADAR (100),
            Action.GIRAR_ALEATORIO
        ])

        self.inimigo_encontrado([
            Action.PERSEGUIR(30),
            Action.ATIRAR_CERTEIRO,
            Action.MOVER_TRAS(40),
            Action.ATIRAR_CERTEIRO
        ])

        self.recebendo_ataque([
            Action.PERSEGUIR(30),
            Action.ESQUIVA_SMART,
            Action.MIRAR,
            Action.ATIRAR_MEDIA
            
        ])

        self.fugir([
            Action.ESQUIVA_SMART,
            Action.MANTER_DISTANCIA(50),
            Action.GIRAR_ALEATORIO,
            Action.MANTER_DISTANCIA(60)
        ])