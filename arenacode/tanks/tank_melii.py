from core.tank import Tank
from core.action import Action

class Melissa(Tank):
    def __init__(self):
        super().__init__(nome="Meli", cor=(123, 60, 100))

    def programar(self):
        self.configurar_gatilhos(vida=30, municao= 4, alerta= 2.0)
        # Patrulhar: anda 150px, gira 90 para a esquerda (patrulha em quadrado)
        self.patrulhar([
        Action.VARREDURA_RADAR(180),
        Action.MOVER_SEGURO(50),
        Action.GIRAR_ALEATORIO(90)
        ])
        
        # Inimigo encontrado: persegue 50px, mira no inimigo e atira (loop)
        self.inimigo_encontrado([
            Action.MIRAR,
            Action.ATIRAR_FORTE,
            Action.MANTER_DISTANCIA
        ])
        
        # Recebendo ataque: gira 90 e foge 100px
        self.recebendo_ataque([
            
            Action.MIRAR,
            Action.ATIRAR_FRACA,
          
        ])
        
        # Fugir: daocio 80px e gira 90 (foge em zigue-zague)
        self.fugir([
            Action.MOVER_TRAS(50),
            Action.GIRAR_DIREITA(45),
            Action.MIRAR,
            Action.ATIRAR_FORTE,
            
        ])
        
      
