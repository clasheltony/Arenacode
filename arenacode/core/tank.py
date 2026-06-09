from abc import ABC, abstractmethod
from typing import Tuple, List, Optional
from .action import Action, ActionType, ConfiguredAction
from .sensor import Sensor
from .bullet import Bullet

class Tank(ABC):
    """
    Classe base abstrata para todos os tanques do jogo.
    Os alunos devem herdar desta classe e implementar o método programar().
    
    No método programar(), o aluno define até 5 ações para cada estado:
        - patrulhar:          Ações enquanto não há inimigos nem ataques.
        - inimigo_encontrado: Ações quando detecta um inimigo.
        - recebendo_ataque:   Ações quando sofre dano.
        - fugir:              Ações quando a vida está baixa ou munição acabando.
    
    Cada ação pode ter um valor:
        Action.MOVER_FRENTE(100)  -> move 100 pixels
        Action.GIRAR_DIREITA(90)  -> gira 90 graus
        Action.ATIRAR             -> dispara uma vez
    """

    def __init__(self, nome: str = "Tanque Desconhecido", cor: Tuple[int, int, int] = (100, 100, 100)):
        self.__vida: int = 100
        self.__energia: float = 100.0
        self.__velocidade: float = 1.5
        self.__angulo: float = 0.0
        self.__posicao: Tuple[float, float] = (0.0, 0.0)
        self.__municao: int = 30
        self.__nome: str = nome
        self.__cor: Tuple[int, int, int] = cor
        self.__contador_acertos: int = 0
        
        self._cooldown_tiro: float = 0.0
        
        # Listas de ações para cada estado (ConfiguredAction)
        self._acoes_patrulhar: List[ConfiguredAction] = []
        self._acoes_inimigo: List[ConfiguredAction] = []
        self._acoes_ataque: List[ConfiguredAction] = []
        self._acoes_fugir: List[ConfiguredAction] = []
        
        # Controle de sequência
        self._estado_atual: str = "patrulhando"
        self._indice_acao: int = 0
        self._progresso_acao: float = 0.0
        self._acao_atual: Optional[ConfiguredAction] = None
        self._sequencia_recuperacao: List[ConfiguredAction] = []
        self._frames_parado: int = 0  # Contador para detectar tanque preso na parede
        
        # Detecção de dano
        self._vida_anterior: int = self.__vida
        self._timer_sob_ataque: float = 0.0
        
        # Gatilhos configuráveis
        self._limite_vida_fuga: int = 40
        self._limite_municao_fuga: int = 4
        self._tempo_alerta_dano: float = 2.0

    # ==========================================
    # PROPRIEDADES (Acesso somente leitura)
    # ==========================================
    @property
    def vida(self) -> int:
        return self.__vida

    @property
    def velocidade(self) -> float:
        return self.__velocidade

    @property
    def angulo(self) -> float:
        return self.__angulo

    @property
    def posicao(self) -> Tuple[float, float]:
        return self.__posicao

    @property
    def municao(self) -> int:
        return self.__municao

    @property
    def energia(self) -> int:
        return int(self.__energia)

    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def cor(self) -> Tuple[int, int, int]:
        return self.__cor

    # ==========================================
    # MÉTODOS DE CONFIGURAÇÃO DE ESTADOS
    # ==========================================
    
    def _normalizar_acoes(self, acoes: list) -> List[ConfiguredAction]:
        """Converte ActionType bare para ConfiguredAction com valor padrão."""
        resultado = []
        for acao in acoes[:5]:
            if isinstance(acao, ConfiguredAction):
                resultado.append(acao)
            elif isinstance(acao, ActionType):
                resultado.append(acao())  # Usa valor padrão
        return resultado
    
    def patrulhar(self, acoes: list):
        """Define até 5 ações sequenciais para o estado de Patrulha (loop contínuo)."""
        self._acoes_patrulhar = self._normalizar_acoes(acoes)
    
    def inimigo_encontrado(self, acoes: list):
        """Define até 5 ações sequenciais para quando um inimigo é detectado."""
        self._acoes_inimigo = self._normalizar_acoes(acoes)
    
    def recebendo_ataque(self, acoes: list):
        """Define até 5 ações sequenciais para quando o tanque recebe dano."""
        self._acoes_ataque = self._normalizar_acoes(acoes)
    
    def fugir(self, acoes: list):
        """Define até 5 ações sequenciais para quando a vida/munição está baixa."""
        self._acoes_fugir = self._normalizar_acoes(acoes)

    def configurar_gatilhos(self, vida: int = 40, municao: int = 4, alerta: float = 2.0):
        """
        Configura os limites que disparam as mudanças de estado.
        :param vida: Porcentagem de vida abaixo da qual o tanque entra em modo de fuga.
        :param municao: Quantidade de munição abaixo da qual o tanque entra em modo de fuga.
        :param alerta: Tempo (segundos) que o tanque permanece em alerta após receber dano.
        """
        self._limite_vida_fuga = vida
        self._limite_municao_fuga = municao
        self._tempo_alerta_dano = alerta

    # ==========================================
    # MÉTODO ABSTRATO (Obrigatório para o Aluno)
    # ==========================================
    @abstractmethod
    def programar(self):
        """
        Método onde o aluno programa o comportamento do tanque.
        Exemplo:
            self.patrulhar([Action.MOVER_FRENTE(150), Action.GIRAR_DIREITA(90)])
            self.inimigo_encontrado([Action.ATIRAR, Action.MOVER_FRENTE(30)])
            self.recebendo_ataque([Action.GIRAR_DIREITA(90), Action.MOVER_FRENTE(100)])
            self.fugir([Action.MOVER_TRAS(80), Action.GIRAR_ESQUERDA(90)])
        """
        pass

    # ==========================================
    # MÁQUINA DE ESTADOS
    # ==========================================
    def _get_lista_estado(self, estado: str) -> List[ConfiguredAction]:
        if estado == "fugindo":
            return self._acoes_fugir
        elif estado == "sob_ataque":
            return self._acoes_ataque
        elif estado == "atacando":
            return self._acoes_inimigo
        else:
            return self._acoes_patrulhar

    def decidir(self, sensores: Sensor):
        """Seleciona o estado e define a ação atual na sequência."""
        # Detectar dano
        if self.__vida < self._vida_anterior:
            self._timer_sob_ataque = self._tempo_alerta_dano
        self._vida_anterior = self.__vida
        
        # Determinar novo estado (prioridade: Fugir > Ataque > Inimigo > Patrulha)
        if self.__vida <= self._limite_vida_fuga or self.__municao <= self._limite_municao_fuga:
            novo_estado = "fugindo"
        elif self._timer_sob_ataque > 0:
            novo_estado = "sob_ataque"
        elif sensores.inimigos_proximos:
            novo_estado = "atacando"
        else:
            novo_estado = "patrulhando"
        
        # Se mudou de estado, resetar sequência
        if novo_estado != self._estado_atual:
            self._estado_atual = novo_estado
            self._indice_acao = 0
            self._progresso_acao = 0.0
        
        # Definir ação atual
        # Prioridade: Sequência de Recuperação (Colisões) > Programa do Aluno
        if self._sequencia_recuperacao:
            if self._indice_acao < len(self._sequencia_recuperacao):
                self._acao_atual = self._sequencia_recuperacao[self._indice_acao]
            else:
                # Terminou recuperação, volta para o programa normal
                self._sequencia_recuperacao = []
                self._indice_acao = 0
                self._progresso_acao = 0.0
                acoes = self._get_lista_estado(self._estado_atual)
                self._acao_atual = acoes[0] if acoes else None
        else:
            acoes = self._get_lista_estado(self._estado_atual)
            if acoes and self._indice_acao < len(acoes):
                self._acao_atual = acoes[self._indice_acao]
            else:
                self._acao_atual = None

    def _avancar_acao(self):
        """Avança para a próxima ação na sequência (loop automático)."""
        if self._sequencia_recuperacao:
            acoes = self._sequencia_recuperacao
        else:
            acoes = self._get_lista_estado(self._estado_atual)
            
        self._indice_acao += 1
        self._progresso_acao = 0.0
        
        if self._indice_acao >= len(acoes):
            if self._sequencia_recuperacao:
                # Fim da recuperação, reset para voltar ao programa normal na próxima decisão
                self._sequencia_recuperacao = []
            self._indice_acao = 0  # Loop

    # ==========================================
    # MÉTODOS INTERNOS (Engine Only)
    # ==========================================
    def _atualizar(self, dt: float):
        if self._cooldown_tiro > 0:
            self._cooldown_tiro -= dt
        if self._timer_sob_ataque > 0:
            self._timer_sob_ataque -= dt
            
        # Recarga de energia: +0.35 por frame (~21 por segundo)
        if self.__energia < 100:
            self.__energia = min(100.0, self.__energia + 21 * dt)

    def _registrar_acerto(self):
        """Recupera 1 munição a cada 3 acertos."""
        self.__contador_acertos += 1
        if self.__contador_acertos >= 3:
            self.__contador_acertos -= 3
            self.__municao += 1

    def _receber_dano(self, dano: int):
        self.__vida -= dano
        if self.__vida < 0:
            self.__vida = 0

    def _esta_vivo(self) -> bool:
        return self.__vida > 0
        
    def _set_posicao(self, x: float, y: float):
        self.__posicao = (x, y)

    def _set_nome(self, novo_nome: str):
        self.__nome = novo_nome
        
    def _set_angulo(self, angulo: float):
        self.__angulo = angulo % 360

    def _consumir_municao(self, custo_energia: int = 25) -> bool:
        if self.__municao > 0 and self.__energia >= custo_energia and self._cooldown_tiro <= 0:
            self.__municao -= 1
            self.__energia -= custo_energia
            self._cooldown_tiro = 45 / 60.0 # 45 frames
            return True
        return False
