from core.tank import Tank
from core.action import Action

class Tank_Vl(Tank):
    def __init__(self):
        super().__init__(nome="Tank VL", cor=(15, 15, 15))

    def programar(self):
        
        self.configurar_gatilhos(vida=20, municao=0, alerta=2.5)
        self.patrulhar([
    
           Action.MOVER_SEGURO(60),
           Action.MOVER_FRENTE(40),
           Action.VARREDURA_RADAR(190)

        ])
        
        
        self.inimigo_encontrado([
            Action.MIRAR,
            Action.ATIRAR_CERTEIRO,
            Action.ATIRAR_FRACA
        ])
        
        
        self.recebendo_ataque([
            Action.MIRAR,
            Action.ATIRAR_CERTEIRO,
            Action.ATIRAR_FORTE
            
        ])
        
       
        self.fugir([
            Action.MIRAR,
            Action.ATIRAR_CERTEIRO
        ])

