# ArenaCode

Jogo educacional de batalha de tanques em Python usando pygame.

## Estrutura do Projeto
- `core/`: Classes base e API que o aluno vai utilizar (NÃO editar).
- `engine/`: Motor do jogo (renderização, colisões, loop principal) (NÃO editar).
- `tanks/`: Onde você criará o seu tanque. Use `tank_exemplo.py` como base.
- `main.py`: Ponto de entrada do jogo.

## Como criar um tanque
1. Crie um arquivo `.py` na pasta `tanks/` (ex: `meu_tanque.py`).
2. Herde da classe `Tank` (importada de `core.tank`).
3. Implemente o método `decidir(self, sensores)`.
4. Retorne uma lista de ações (ex: `[Action.MOVER_FRENTE, Action.ATIRAR]`).

## Como rodar
Instale o pygame:
```bash
pip install pygame
```

Execute o jogo:
```bash
python main.py
```
