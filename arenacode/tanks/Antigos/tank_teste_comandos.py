from core.tank import Tank
from core.action import Action

class Comandante(Tank):
    def __init__(self):
        super().__init__(nome="Comandante", cor=(200, 50, 200))

    def programar(self):
        # Patrulhar: anda 200px, gira 90° para a direita (quadrado oposto ao Caçador)
        self.patrulhar([
            Action.MOVER_FRENTE(90),
            Action.GIRAR_DIREITA(90),
            Action.MOVER_FRENTE(90),
            Action.GIRAR_DIREITA(90)
        ])
        
        # Inimigo encontrado: atira, gira 15° para ajustar mira, atira de novo
        self.inimigo_encontrado([
            Action.MIRAR,
            Action.PERSEGUIR(120),
            Action.ATIRAR_MEDIA,
            Action.ATIRAR_FRACA,
            Action.MOVER_FRENTE(40)
        ])
        
        # Recebendo ataque: avança e gira (contorna o inimigo)
        self.recebendo_ataque([
            Action.PERSEGUIR(50) ,
            Action.MIRAR,
            Action.ATIRAR,
            Action.GIRAR_DIREITA(90),
            Action.MOVER_FRENTE(100)

        ])
        
        # Fugir: dá ré e gira 120° (faz curvas largas fugindo)
        self.fugir([
            Action.GIRAR_ESQUERDA(90),
            Action.MOVER_FRENTE(180),
            Action.MIRAR,
            Action.ATIRAR
        ])
