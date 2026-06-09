from core.tank import Tank
from core.action import Action

class sigma(Tank):
    def __init__(self):
        super().__init__(nome="SIGMA", cor=(75, 0, 130))

    def programar(self):

        self.configurar_gatilhos( vida=10, municao=1, alerta=1)
        # Patrulhar: anda 150px, girar 90° e seguir 150px em linha reta (patrulha em quadrado)
        self.patrulhar([
            Action.VARREDURA_RADAR(150),
            Action.GIRAR_ALEATORIO, # Girar 45° e seguir 150px em linha reta 

            
        ])
        
        # Inimigo encontrado: usa mira perfeita e mantém distancia
        self.inimigo_encontrado([
            Action.MANTER_DISTANCIA(100),
            Action.MIRAR,    # perseguir o inimigo e atirar várias vezes
            Action.ATIRAR_FORTE,

        ])
        
        # Recebendo ataque: usa esquiva automática
        self.recebendo_ataque([
            Action.ESQUIVA_SMART,
            Action.MIRAR,  # atirar
            Action.ATIRAR_CERTEIRO, # perseguir o inimigo e atirar várias vezes
        ])
        
        # Fugir: movimento errático para sobreviver
        self.fugir ([
            Action.MOVER_TRAS(60),
            Action.GIRAR_ALEATORIO, #Girar 90° e seguir 100px em linha reta 
            Action.MOVER_SEGURO,
            Action.MIRAR,
            Action.ATIRAR_CERTEIRO,
        ])