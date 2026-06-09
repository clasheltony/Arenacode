from core.tank import Tank
from core.action import Action

class Tank_0(Tank):
    """
    Tanque de exemplo que utiliza as Ações Inteligentes (Smart Actions).
    Ele demonstra como programar comportamentos complexos com pouco código.
    """
    def __init__(self):
        super().__init__(nome="Tank_0", cor=(70, 140, 200))

    def programar(self):
        # Configura os gatilhos (Triggers)
        # Se vida < 30 ou munição < 5, entra em modo Fugir
        # Se levar dano, fica em alerta por 2 segundos
        self.configurar_gatilhos(vida=20, municao=0, alerta=2.0)

        # 1. PATRULHAR: Usa movimento seguro e radar de varredura
        self.patrulhar([
        Action.MOVER_FRENTE(150),
        Action.VARREDURA_RADAR(250),
        Action.MOVER_TRAS(80),
        Action.GIRAR_DIREITA(90),
        Action.GIRAR_ESQUERDA(180)
        ])
        
        # 2. INIMIGO ENCONTRADO: Usa mira perfeita e mantém distância
        self.inimigo_encontrado([
        Action.MIRAR,
        Action.ATIRAR_CERTEIRO,
        Action.MANTER_DISTANCIA(85),
        Action.MIRAR,
        Action.ATIRAR_FORTE
        ])
        
        # 3. RECEBENDO ATAQUE: Usa esquiva automática
        self.recebendo_ataque([
            Action.ESQUIVA_SMART,
            Action.VARREDURA_RADAR(100),
            Action.MANTER_DISTANCIA(50),
            Action.MIRAR,
            Action.ATIRAR_MEDIA,
            Action.ESQUIVA_SMART,
            Action.ATIRAR_CERTEIRO
        ])
        
        # 4. FUGIR: Movimento errático para sobreviver
        self.fugir([
            Action.MIRAR,
            Action.ATIRAR_CERTEIRO,
            Action.ESQUIVA_SMART,
            Action.MANTER_DISTANCIA(200)
        ])

    
