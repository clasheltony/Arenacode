from core.tank import Tank
from core.action import Action

class Estrategista(Tank):
    """
    Tanque de exemplo que utiliza as Ações Inteligentes (Smart Actions).
    Ele demonstra como programar comportamentos complexos com pouco código.
    """
    def __init__(self):
        super().__init__(nome="Estrategista", cor=(50, 200, 150))

    def programar(self):
        # Configura os gatilhos (Triggers)
        # Se vida < 30 ou munição < 5, entra em modo Fugir
        # Se levar dano, fica em alerta por 2 segundos
        self.configurar_gatilhos(vida=20, municao=0, alerta=2.0)

        # 1. PATRULHAR: Usa movimento seguro e radar de varredura
        self.patrulhar([
            Action.MOVER_SEGURO(200),  # Anda 200px, mas para se houver parede
            Action.VARREDURA_RADAR(180), # Gira 180 procurando inimigos, para se achar
            Action.GIRAR_ALEATORIO     # Gira um valor randômico para ser imprevisível
        ])
        
        # 2. INIMIGO ENCONTRADO: Usa mira perfeita e mantém distância
        self.inimigo_encontrado([
            Action.MIRAR,              # Alinha com o inimigo
            Action.ATIRAR_CERTEIRO,    # Só atira se a mira estiver ±5 graus
            Action.MANTER_DISTANCIA(200) # Tenta ficar a 200px do alvo (Kite)
        ])
        
        # 3. RECEBENDO ATAQUE: Usa esquiva automática
        self.recebendo_ataque([
            Action.ESQUIVA_SMART,      # Desvia se houver balas vindo
            Action.MIRAR,              # Tenta revidar
            Action.ATIRAR_CERTEIRO
        ])
        
        # 4. FUGIR: Movimento errático para sobreviver
        self.fugir([
            Action.MOVER_TRAS(80),
            Action.GIRAR_ALEATORIO,
            Action.MOVER_SEGURO(150),
            Action.MIRAR,
            Action.ATIRAR_CERTEIRO
            
            
        ])
