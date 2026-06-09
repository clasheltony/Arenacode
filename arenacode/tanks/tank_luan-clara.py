from core.tank import Tank
from core.action import Action

class LuanClara(Tank):
   
    def __init__(self):
        super().__init__(nome="Luan Clara", cor=(0, 0, 0))

    def programar(self):
        
        self.configurar_gatilhos(vida=20, municao=0, alerta=2.0)

        self.patrulhar([
            Action.MOVER_SEGURO(100),
            Action.VARREDURA_RADAR(360),
            Action.GIRAR_ESQUERDA(130)
        ])
        
        self.inimigo_encontrado([
            Action.MANTER_DISTANCIA(80),
            Action.MIRAR,
            Action.ATIRAR_FORTE,
            Action.ATIRAR_FORTE,
            Action.ATIRAR_CERTEIRO
            
        ])
        
        self.recebendo_ataque([                
            Action.MIRAR,
            Action.ATIRAR_CERTEIRO,
            Action.ATIRAR_FORTE,
        ])
        
        self.fugir([
            Action.MIRAR,
            Action.ATIRAR_CERTEIRO,
            Action.ATIRAR_FORTE,
            Action.ATIRAR_FORTE
            
            
            
        ])