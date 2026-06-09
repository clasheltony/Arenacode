from dataclasses import dataclass
from typing import List, Tuple, Dict

@dataclass(frozen=True)
class Sensor:
    """
    Objeto de sensores passado a cada frame para o método decidir() do tanque.
    Representa o que o tanque "enxerga" no ambiente.
    Todos os atributos são somente leitura (frozen=True) para evitar que o aluno trapaceie alterando os valores.
    """
    inimigos_proximos: List[Dict[str, float]]
    # Cada dict contém: {'distancia': float, 'angulo_relativo': float, 'vida': int}
    
    parede_frente: float
    parede_direita: float
    parede_esquerda: float
    
    propria_vida: int
    propria_municao: int
    posicao_atual: Tuple[float, float]
    
    balas_proximas: List[Dict[str, float]]
    # Cada dict contém: {'distancia': float, 'angulo_relativo': float}
