from core.tank import Tank
from core.action import Action

#Criação da classe Tanque
class Tanque_Tony (Tank):
    def __init__(self):
        super().__init__(nome = "Tony Ferreira", cor = (0, 0 ,255))
        
    def programar(self):
        self.configurar_gatilhos(vida=10, municao= 3, alerta= 1)

        self.patrulhar([
            Action.VARREDURA_RADAR(360),
            Action.MOVER_FRENTE(150)
            


        ])
        self.inimigo_encontrado([
            
            Action.MIRAR,
            Action.ATIRAR_CERTEIRO,
            Action.MANTER_DISTANCIA(100),
            Action.ATIRAR_FRACA
        
        ])
        self.recebendo_ataque([
            
            
            Action.MIRAR,
            Action.PERSEGUIR(50),
            Action.ATIRAR_CERTEIRO,
            Action.ATIRAR_FORTE,
            Action.MANTER_DISTANCIA(50)
            
        ])
        self.fugir([
            Action.GIRAR_ALEATORIO,
            Action.ESQUIVA_SMART,
            Action.MANTER_DISTANCIA(200),
            Action.ATIRAR_CERTEIRO,
            
        ])

    