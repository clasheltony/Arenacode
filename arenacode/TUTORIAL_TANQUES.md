# 📘 Manual Oficial do Piloto: ArenaCode

Bem-vindo ao **ArenaCode**! Você foi convocado para construir e comandar um tanque de guerra digital. Mas aqui você não controla o tanque com um controle de videogame ou teclado. O seu desafio é **programar a inteligência** dele. 

Você vai ensinar o seu tanque a pensar: como procurar inimigos, quando atirar, como desviar de tiros e como não bater nas paredes.

Este manual foi feito para ser lido passo a passo. Vamos lá?

---

## 🛠️ 1. O Básico: Criando o seu Tanque

Todos os tanques devem morar na pasta chamada `tanks/`. Para começar, você deve criar um arquivo Python novo lá dentro. Por exemplo: `meu_tanque.py`.

No seu arquivo, você sempre começará importando as ferramentas básicas e criando a "fôrma" (Classe) do seu tanque.

### O Código Inicial Obrigatório:
```python
# Importamos a base de um tanque
from core.tank import Tank

# Criamos a nossa classe, que HERDA da classe Tank.
# Mude o "MeuTanque" para o nome que desejar (sem espaços)!
class MeuTanque(Tank):
    
    # O método __init__ é chamado quando o tanque "nasce"
    def __init__(self):
        super().__init__(nome="Destruidor", cor=(255, 0, 0))

    # O método decidir é o "cérebro" do tanque
    def decidir(self, sensores):
        # Aqui ficará a nossa lógica!
        pass
```

---

## 🎨 2. Personalizando o Tanque: O método `__init__`

O método `__init__` é o construtor. Ele roda apenas **uma única vez** no momento em que a batalha começa. É aqui que você batiza seu tanque e pinta a armadura dele.

```python
    def __init__(self):
        super().__init__(nome="Nome do Seu Tanque", cor=(R, G, B))
```

- **`nome`**: O nome que vai aparecer em cima dele na tela da batalha.
- **`cor`**: O ArenaCode usa o sistema **RGB** (Red, Green, Blue) para formar cores. Os valores vão de `0` (nada daquela cor) até `255` (máximo daquela cor).
  - Vermelho forte: `(255, 0, 0)`
  - Verde forte: `(0, 255, 0)`
  - Azul forte: `(0, 0, 255)`
  - Preto: `(0, 0, 0)`
  - Branco: `(255, 255, 255)`
  - Roxo: `(128, 0, 128)`

Você também pode usar o `__init__` para criar **memórias** para o seu tanque, variáveis onde ele guarda informações para lembrar depois. Exemplo: `self.giro_padrao = Action.GIRAR_DIREITA`.

---

## 🧠 3. O Cérebro do Tanque: O método `decidir`

Esta é a parte mais importante de todas. A arena do jogo é extremamente rápida. O jogo chama o seu método `decidir` **60 vezes por segundo**!

```python
    def decidir(self, sensores):
        # (Sua lógica entra aqui)
        pass
```

### A Regra de Ouro do método decidir:
Dentro dessa função, você pode chamar os comandos do próprio tanque (como `self.mover_frente()`).
Mas lembre-se: **O tanque só consegue executar no máximo 2 ações ao mesmo tempo!** Se você mandar ele atirar, andar pra frente e girar tudo de uma vez, ele vai ignorar o terceiro comando.

---

## ⚙️ 4. O que o tanque pode fazer? (As Ações)

Para controlar o seu tanque, você chama os métodos dele usando o `self.`. 

- `self.mover_frente()`: O tanque acelera para a frente.
- `self.mover_tras()`: O tanque dá marcha ré.
- `self.girar_direita()`: O tanque vira para a direita (sentido horário).
- `self.girar_esquerda()`: O tanque vira para a esquerda (sentido anti-horário).
- `self.atirar()`: Dispara um míssil na direção em que está olhando.

**Como combinar ações?**
Você pode querer dar ré e virar ao mesmo tempo para fugir de um tiro:
```python
    self.mover_tras()
    self.girar_direita()
```
Ou atirar enquanto persegue:
```python
    self.mover_frente()
    self.atirar()
```

**⚠️ Atenção sobre o Tiro:** Você tem uma quantidade limitada de munição. Além disso, depois de atirar, a arma superaquece (cooldown). Demora meio segundo (0.5s) até você poder atirar novamente. Se você mandar atirar enquanto recarrega, a ordem é simplesmente ignorada.

---

## 📡 5. Os Olhos e Ouvidos do Tanque: Os `sensores`

Como o seu tanque sabe onde ir? Através do parâmetro `sensores`. O jogo atualiza essas informações e te entrega mastigadas a cada milissegundo.

O `sensores` possui várias variáveis prontas para você checar com `if`:

### Status do seu próprio tanque:
- **`sensores.propria_vida`**: Retorna um número inteiro indicando quanta vida você tem (começa em 100).
- **`sensores.propria_municao`**: Quantas balas restam no estoque.
- **`sensores.posicao_atual`**: Mostra sua localização no mapa no formato `(x, y)`.

### Evitando Paredes:
O tanque possui lasers que medem a distância até a parede mais próxima em três direções:
- **`sensores.parede_frente`**
- **`sensores.parede_direita`**
- **`sensores.parede_esquerda`**
*(Retornam um número Float. Se for menor que 50, você está muito perto!)*

### O Radar de Inimigos (`sensores.inimigos_proximos`):
Este radar é uma Lista contendo todos os inimigos que o seu tanque está enxergando. A lista **já vem ordenada do mais próximo para o mais distante**.

Como é uma lista, o inimigo mais perto sempre será o item zero: `sensores.inimigos_proximos[0]`.

Para saber sobre esse inimigo, você acessa o "dicionário" de informações dele:
- `inimigo['distancia']`: Quão longe ele está.
- `inimigo['vida']`: Quanta vida ele tem.
- `inimigo['angulo_relativo']`: **O valor mais importante!** Indica para onde você tem que virar para mirar nele.
  - Se o ângulo for **zero (0)**, ele está perfeitamente na sua frente (hora de atirar!).
  - Se o ângulo for **positivo (+)**, ele está à sua direita (você deve virar à direita).
  - Se o ângulo for **negativo (-)**, ele está à sua esquerda (você deve virar à esquerda).

### O Sentido Aranha (`sensores.balas_proximas`):
Funciona exatamente igual aos inimigos, mas detecta os tiros que estão voando pela arena.
O tiro mais perto será `sensores.balas_proximas[0]`.
Você pode ler a `bala['distancia']` e o `bala['angulo_relativo']` para tentar calcular uma esquiva perfeita (dando ré e girando, por exemplo).

---

## 🚀 6. Montando a Inteligência (Passo a Passo)

Vamos construir um tanque inteligente agora. Leia os comentários para entender a lógica.

```python
from core.tank import Tank

class TanqueDidatico(Tank):
    def __init__(self):
        super().__init__(nome="Professor", cor=(100, 100, 255))

    def decidir(self, sensores):

        # REGRA 1: Não bater na parede!
        # Se a parede da frente estiver a menos de 60 pixels...
        if sensores.parede_frente < 60:
            self.mover_tras()     # Dá ré!
            self.girar_esquerda() # E vira para tentar sair de frente pra ela
            
            # Se for fugir da parede, encerramos a função aqui para não fazer mais nada
            return

        # REGRA 2: Procurar e destruir inimigos
        # PRIMEIRO VERIFICAMOS SE A LISTA DE INIMIGOS NÃO ESTÁ VAZIA! 
        if len(sensores.inimigos_proximos) > 0:
            
            # Pega o inimigo mais próximo
            inimigo_alvo = sensores.inimigos_proximos[0]
            
            # Pega o ângulo que ele está em relação ao nosso tanque
            angulo = inimigo_alvo['angulo_relativo']
            
            # Se a diferença do ângulo for bem pequena (entre -10 e +10 graus)
            if abs(angulo) < 10:
                self.atirar()
            
            # Se a mira não está boa, temos que girar na direção dele
            else:
                if angulo > 0:
                    self.girar_direita()
                else:
                    self.girar_esquerda()
                    
            # Acelera na direção dele se ele estiver meio longe
            if inimigo_alvo['distancia'] > 150:
                self.mover_frente()

        # REGRA 3: O que fazer se não tem parede perto e não estamos vendo inimigos?
        # Apenas andamos pra frente para explorar o mapa!
        # Podemos checar quantas ações já pedimos lendo a lista interna `self._acoes_atuais`
        if len(self._acoes_atuais) == 0:
            self.mover_frente()
```

---

## 🏆 7. Dicas de Ouro para Vencer

1. **Evite Erros de Código (Bugs):** Se o seu código der um erro (como tentar ler uma lista vazia ou escrever uma palavra errada), o seu tanque **desliga no meio da arena**. Use sempre `if sensores.inimigos_proximos:` antes de tentar acessar um inimigo.
2. **Fuja das balas:** Muitos alunos só programam o tanque para atacar. Um tanque que usa o sensor de `balas_proximas` para dar marcha ré na hora certa sobrevive por muito mais tempo.
3. **Não desperdice munição:** Não coloque o `Action.ATIRAR` como primeira coisa do código. Atire apenas se o `angulo_relativo` estiver entre -15 e +15 graus. Senão, sua bala vai atingir apenas a parede!
4. **Use Memórias:** No `__init__`, crie variáveis com o `self` (Ex: `self.direcao_fuga = Action.GIRAR_DIREITA`). Você pode alterar elas durante o jogo para fazer seu tanque criar comportamentos de longo prazo (como alternar entre um 'Modo Ofensivo' e 'Modo Defensivo' quando a vida cai abaixo de 30).

Boa sorte e boas linhas de código! Que o melhor tanque vença!
