class ActionType:
    """Representa um tipo de ação do tanque. Pode ser chamado com valor: Action.MOVER_FRENTE(100)"""
    
    def __init__(self, nome: str, valor_padrao: float = None):
        self.nome = nome
        self.valor_padrao = valor_padrao
    
    def __call__(self, valor: float = None) -> 'ConfiguredAction':
        """Cria ação com valor. Ex: Action.MOVER_FRENTE(100) -> mover 100 pixels"""
        if valor is None:
            valor = self.valor_padrao
        return ConfiguredAction(self, valor)
    
    def __repr__(self):
        return f"Action.{self.nome}"
    
    def __eq__(self, other):
        if isinstance(other, ActionType):
            return self.nome == other.nome
        return NotImplemented
    
    def __hash__(self):
        return hash(self.nome)


class ConfiguredAction:
    """Uma ação com valor definido (pixels ou graus). Criada ao chamar Action.MOVER_FRENTE(100)."""
    
    def __init__(self, action_type: ActionType, valor: float = None):
        self.action_type = action_type
        self.valor = valor
    
    def __repr__(self):
        if self.valor is not None:
            return f"{self.action_type}({self.valor})"
        return f"{self.action_type}"


class Action:
    """
    Ações disponíveis para programar o tanque.
    
    Com valor:
        Action.MOVER_FRENTE(100)   -> move 100 pixels para frente
        Action.GIRAR_DIREITA(90)   -> gira 90 graus para a direita
        Action.PERSEGUIR(50)       -> persegue o inimigo por 50 pixels
    
    Sem valor (usa padrão):
        Action.MOVER_FRENTE        -> move 50 pixels (padrão)
        Action.GIRAR_DIREITA       -> gira 45 graus (padrão)
        Action.ATIRAR              -> dispara uma vez
        Action.MIRAR               -> gira até encarar o inimigo
    """
    MOVER_FRENTE = ActionType("MOVER_FRENTE", 50)
    MOVER_TRAS = ActionType("MOVER_TRAS", 50)
    GIRAR_DIREITA = ActionType("GIRAR_DIREITA", 45)
    GIRAR_ESQUERDA = ActionType("GIRAR_ESQUERDA", 45)
    ATIRAR = ActionType("ATIRAR", None) # Mapeado para ATIRAR_MEDIA
    ATIRAR_FRACA = ActionType("ATIRAR_FRACA", None)
    ATIRAR_MEDIA = ActionType("ATIRAR_MEDIA", None)
    ATIRAR_FORTE = ActionType("ATIRAR_FORTE", None)
    ATIRAR_CERTEIRO = ActionType("ATIRAR_CERTEIRO", None)
    PARADO = ActionType("PARADO", None)
    PERSEGUIR = ActionType("PERSEGUIR", 50)
    MIRAR = ActionType("MIRAR", None)
    MOVER_SEGURO = ActionType("MOVER_SEGURO", 50)
    ESQUIVA_SMART = ActionType("ESQUIVA_SMART", None)
    VARREDURA_RADAR = ActionType("VARREDURA_RADAR", 360)
    MANTER_DISTANCIA = ActionType("MANTER_DISTANCIA", 250)
    GIRAR_ALEATORIO = ActionType("GIRAR_ALEATORIO", None)
