from core.tank import Tank
from core.action import Action

class Yslla (Tank):
    def __init__(self):
        super().__init__(nome="Yslla", cor=(200, 200, 30))

    def programar(self):
        #patrulhar
        self.configurar_gatilhos( vida=10, municao=1, alerta=1)
        self.patrulhar([
            Action.VARREDURA_RADAR,
            Action.MOVER_SEGURO(150),
            Action.MOVER_FRENTE(90)
        
        ])
        
        # Inimigo encontrado perceguir
        self.inimigo_encontrado([
            Action.MIRAR,
            Action.ATIRAR_CERTEIRO,
            Action.MANTER_DISTANCIA(130)
        ])
        
        # Recebendo ataque: gira 90 e foge 100px
        self.recebendo_ataque([
            Action.ESQUIVA_SMART,
            Action.MIRAR,
            Action.ATIRAR_CERTEIRO,
        ])
        
        # Fugir: daocio 80px e gira 90 (foge em zigue-zague)
        self.fugir([
            Action.MOVER_TRAS(80),
            Action.GIRAR_ALEATORIO,
            Action.MOVER_SEGURO(150),
            Action.MIRAR,
            Action.ATIRAR_CERTEIRO
        ])