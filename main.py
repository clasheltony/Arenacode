import pygame
from arena import Arena
from tanque_aluno1 import TanqueAluno1
from tanque_aluno2 import TanqueAluno2

pygame.init()

LARGURA = 800
ALTURA = 600

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("ArenaCode")

clock = pygame.time.Clock()

t1 = TanqueAluno1(100, 100, (0, 255, 0))
t2 = TanqueAluno2(700, 500, (255, 0, 0))

arena = Arena(LARGURA, ALTURA, [t1, t2])

rodando = True
while rodando:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            rodando = False

    tela.fill((30, 30, 30))

    arena.atualizar()
    arena.desenhar(tela)

    # condição de vitória
    if t1.vida <= 0:
        print("Tanque Vermelho venceu!")
        rodando = False

    if t2.vida <= 0:
        print("Tanque Verde venceu!")
        rodando = False

    pygame.display.flip()
    clock.tick(60)

pygame.quit()