from core.tank import Tank
from core.action import Action

#Criação da classe Tanque
class Tanque_andrey (Tank):
    def __init__(self):
        super().__init__(nome = "x<A>x", cor = (0, 78 ,255))
    def programar(self):
        
        self.configurar_gatilhos(vida=10, municao=6, alerta=4)
       
        self.patrulhar([
            Action.MOVER_SEGURO(60),
            Action.VARREDURA_RADAR(200),
            Action.GIRAR_ALEATORIO
           
            
        ])

        self.inimigo_encontrado([
            #Action.PERSEGUIR(100),
            Action.MIRAR,
            Action.ATIRAR_FORTE,
            Action.MANTER_DISTANCIA(100),
            Action.PERSEGUIR(50),
            Action.VARREDURA_RADAR(180)

        
        ])
        self.recebendo_ataque([
            
            Action.ESQUIVA_SMART,
            
            Action.MIRAR,
            Action.ATIRAR_CERTEIRO,
            
            
            
        ])
        self.fugir([
             Action.PERSEGUIR(80),
            Action.MOVER_TRAS(90),
           
            Action.MOVER_SEGURO(150),
            Action.MIRAR,
            Action.ATIRAR_CERTEIRO,
 
            
        ])

    