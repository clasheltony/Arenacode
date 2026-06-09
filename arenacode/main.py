import os
import sys
import importlib.util
import inspect
import time
import pygame

from engine.menu import Menu
from engine.game import GameEngine
from core.tank import Tank

def carregar_tanques(diretorio="tanks"):
    classes_encontradas = []
    
    if not os.path.exists(diretorio):
        return classes_encontradas

    for arquivo in os.listdir(diretorio):
        if arquivo.endswith(".py") and not arquivo.startswith("__"):
            caminho = os.path.join(diretorio, arquivo)
            nome_modulo = arquivo[:-3]
            
            spec = importlib.util.spec_from_file_location(nome_modulo, caminho)
            if spec and spec.loader:
                modulo = importlib.util.module_from_spec(spec)
                try:
                    spec.loader.exec_module(modulo)
                    for nome, obj in vars(modulo).items():
                        if isinstance(obj, type) and issubclass(obj, Tank) and obj is not Tank:
                            classes_encontradas.append(obj)
                except Exception as e:
                    print(f"Erro ao carregar tanque de {arquivo}: {e}")
                    
    return classes_encontradas

def executar_batalha_simples(classes, num_rounds):
    placar_total = {}
    
    for r in range(num_rounds):
        print(f"\n--- INICIANDO ROUND {r+1} de {num_rounds} ---")
        engine = GameEngine(classes)
        resultado = engine.executar_batalha()
        engine.renderer.fechar()
        
        for nome, stats in resultado.items():
            if nome not in placar_total:
                placar_total[nome] = stats.copy()
            else:
                for chave, valor in stats.items():
                    placar_total[nome][chave] += valor
            
        if r < num_rounds - 1:
            print(f"Placar Parcial do Round {r+1}: {resultado}")
            print("Próximo round em 2 segundos...")
            time.sleep(2)

    return placar_total

def executar_torneio(classes):
    placar_geral = {cls.__name__: 0 for cls in classes}
    
    for i in range(len(classes)):
        for j in range(i + 1, len(classes)):
            t1, t2 = classes[i], classes[j]
            print(f"\nRodada: {t1.__name__} vs {t2.__name__} (iniciando em 2s...)")
            time.sleep(2)
            engine = GameEngine([t1, t2])
            resultado = engine.executar_batalha()
            engine.renderer.fechar()
            
            for cls in [t1, t2]:
                temp = cls()
                if temp.nome in resultado:
                    stats = resultado[temp.nome]
                    nome_cls = cls.__name__
                    if isinstance(placar_geral[nome_cls], int):
                        placar_geral[nome_cls] = stats.copy()
                    else:
                        for chave, valor in stats.items():
                            placar_geral[nome_cls][chave] += valor

    return placar_geral

def executar_treinamento(classe):
    print(f"\n--- INICIANDO TREINAMENTO: {classe.__name__} ---")
    
    class AlvoEstatico(Tank):
        def __init__(self):
            super().__init__(nome="Alvo", cor=(150, 50, 50))
            
        def programar(self):
            pass
            
        def decidir(self, sensores):
            pass
            
    # Cria uma batalha com o tanque do jogador e 2 alvos estáticos
    engine = GameEngine([classe, AlvoEstatico, AlvoEstatico])
    engine.tempo_batalha = 300.0 # Mais tempo para o treinamento
    resultado = engine.executar_batalha()
    engine.renderer.fechar()
    
    # Podemos retornar o resultado só do tanque principal para o ranking, ou nada
    placar_final = {classe.__name__: resultado.get(classe().nome, {})}
    return placar_final


def main():
    pygame.init()
    
    print("================================")
    print("Bem-vindo ao ArenaCode!")
    print("================================\n")
    
    pasta = os.path.join(os.path.dirname(__file__), "tanks")
    classes = carregar_tanques(pasta)
    
    if not classes:
        print("Nenhum tanque encontrado. Crie seu tanque na pasta tanks/!")
        sys.exit(0)
        
    print(f"Tanques carregados: {[c.__name__ for c in classes]}\n")
    
    menu = Menu(900, 700)
    menu.carregar_tanques(classes)
    
    ranking = None
    modo_anterior = None
    
    while True:
        if ranking:
            menu.ranking_resultados = ranking
            menu.estado = "ranking"
            menu.modo_anterior = modo_anterior
            ranking = None
            
        config = menu.executar()
        
        if config is None:
            break
            
        modo = config["modo"]
        num_rounds = config["rounds"]
        classes_selecionadas = config["tanques"]
        modo_anterior = modo
        
        try:
            pygame.display.init()
        except:
            pygame.init()
        
        if modo == "simples":
            print(f"\n=== BATALHA SIMPLES ({num_rounds} rounds) ===")
            ranking = executar_batalha_simples(classes_selecionadas, num_rounds)
        elif modo == "torneio":
            print("\n=== MODO TORNEIO ===")
            ranking = executar_torneio(classes_selecionadas)
        elif modo == "treinamento":
            print("\n=== MODO TREINAMENTO ===")
            ranking = executar_treinamento(classes_selecionadas[0])
        
        # Reiniciar menu após a batalha
        pygame.init()
        menu = Menu(900, 700)
        menu.carregar_tanques(classes)

if __name__ == "__main__":
    main()