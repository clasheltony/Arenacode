import pygame
import sys
import os
from typing import List

pygame.init()

class Menu:
    def __init__(self, largura: int = 900, altura: int = 700):
        self.largura = largura
        self.altura = altura
        self.tela = pygame.display.set_mode((largura, altura))
        pygame.display.set_caption("ArenaCode - Menu")
        
        assets_dir = os.path.join(os.path.dirname(os.path.dirname(__file__)), "assets")
        img_path = os.path.join(assets_dir, "tela_Inicial_ArenaCode.png")
        if os.path.exists(img_path):
            self.img_fundo = pygame.image.load(img_path)
            self.img_fundo = pygame.transform.scale(self.img_fundo, (largura, altura))
        else:
            self.img_fundo = None
        
        self.fonte_botao = pygame.font.SysFont("bebasneueregular", 28)
        self.fonte_opcao = pygame.font.SysFont("bebasneueregular", 22)
        self.fonte_pequena = pygame.font.SysFont("bebasneueregular", 14)
        
        self.cores = {
            "fundo": (25, 27, 35),
            "botao_normal": (70, 130, 180),
            "botao_hover": (100, 160, 220),
            "botao_selecionado": (50, 200, 100),
            "texto": (255, 255, 255),
            "borda": (100, 150, 200),
            "fundo_panel": (35, 40, 55)
        }
        
        self.estado = "menu_principal"
        self.selecao_modo = None
        self.selecao_rounds = 3
        self.tanques_selecionados: List[int] = []
        self.tanques_disponiveis: List[type] = []
        self.confirmar_tanques = False
        self.ranking_resultados = None
        self.modo_anterior = None
        self.botao_clicado = None
        
        # Carregar imagens dos botões (Redimensionados para caberem 4 na tela de 900px)
        larg_bt = 200
        self.bt_batalha_img = self._carregar_e_redimensionar(os.path.join(assets_dir, "botao_batalha.png"), larg_bt)
        self.bt_torneio_img = self._carregar_e_redimensionar(os.path.join(assets_dir, "botao_torneio.png"), larg_bt)
        self.bt_treinamento_img = self._carregar_e_redimensionar(os.path.join(assets_dir, "Botao_treinamento.png"), larg_bt)
        self.bt_sair_img = self._carregar_e_redimensionar(os.path.join(assets_dir, "botao_sair.png"), larg_bt)

    def _carregar_e_redimensionar(self, caminho, largura_alvo):
        if os.path.exists(caminho):
            img = pygame.image.load(caminho).convert_alpha()
            w, h = img.get_size()
            proporcao = h / w
            altura_alvo = int(largura_alvo * proporcao)
            return pygame.transform.smoothscale(img, (largura_alvo, altura_alvo))
        return None
        
    def carregar_tanques(self, classes: List[type]):
        self.tanques_disponiveis = classes
        self.tanques_selecionados = []
        
    def _desenhar_botao(self, rect: pygame.Rect, texto: str, hover: bool = False):
        cor = self.cores["botao_hover"] if hover else self.cores["botao_normal"]
        pygame.draw.rect(self.tela, cor, rect, border_radius=10)
        pygame.draw.rect(self.tela, self.cores["borda"], rect, 2, border_radius=10)
        
        texto_surf = self.fonte_botao.render(texto, True, self.cores["texto"])
        self.tela.blit(texto_surf, (rect.centerx - texto_surf.get_width() // 2, 
                                   rect.centery - texto_surf.get_height() // 2))
    
    def _desenhar_fundo_menu_principal(self):
        if self.img_fundo:
            self.tela.blit(self.img_fundo, (0, 0))
        else:
            self.tela.fill(self.cores["fundo"])
    
    def _desenhar_fundo_outras_telas(self):
        self.tela.fill(self.cores["fundo"])
        
        pygame.draw.rect(self.tela, self.cores["borda"], (0, 0, self.largura, self.altura), 8)
        
        for x in range(40, self.largura, 40):
            pygame.draw.line(self.tela, (40, 45, 55), (x, 10), (x, self.altura - 10), 1)
        for y in range(40, self.altura - 10, 40):
            pygame.draw.line(self.tela, (40, 45, 55), (10, y), (self.largura - 10, y), 1)
         
    def _desenhar_menu_principal(self):
        self._desenhar_fundo_menu_principal()
        
        # Dimensões para layout
        espaco = 30
        largura_total = 0
        botoes_info = []
        
        if self.bt_batalha_img:
            botoes_info.append((self.bt_batalha_img, "simples", None))
        else:
            botoes_info.append((None, "simples", "BATALHA"))
            
        if self.bt_torneio_img:
            botoes_info.append((self.bt_torneio_img, "torneio", None))
        else:
            botoes_info.append((None, "torneio", "TORNEIO"))
            
        if self.bt_treinamento_img:
            botoes_info.append((self.bt_treinamento_img, "treinamento", None))
        else:
            botoes_info.append((None, "treinamento", "TREINAMENTO"))
            
        if self.bt_sair_img:
            botoes_info.append((self.bt_sair_img, "sair", None))
        else:
            botoes_info.append((None, "sair", "SAIR"))
            
        largura_total = sum((img.get_width() if img else 200) for img, _, _ in botoes_info) + espaco * (len(botoes_info) - 1)
        x_atual = self.largura // 2 - largura_total // 2
        y_botoes = self.altura - 120
        
        mouse_pos = pygame.mouse.get_pos()
        self.rects_menu_principal = {} # Guardar rects para detecção de clique
        
        for img, acao, texto in botoes_info:
            if img:
                rect = img.get_rect(topleft=(x_atual, y_botoes))

            
                if rect.collidepoint(mouse_pos):
                    w, h = img.get_size()
                    img_hover = pygame.transform.smoothscale(img, (int(w * 1.05), int(h * 1.05)))
                    rect_hover = img_hover.get_rect(center=rect.center)
                    self.tela.blit(img_hover, rect_hover)
                else:
                    self.tela.blit(img, rect)
                self.rects_menu_principal[acao] = rect
                x_atual += img.get_width() + espaco
            else:
                rect = pygame.Rect(x_atual, y_botoes, 200, 50)
                self._desenhar_botao(rect, texto, rect.collidepoint(mouse_pos))
                self.rects_menu_principal[acao] = rect
                x_atual += 200 + espaco
            
    def _desenhar_selecao_rounds(self):
        self._desenhar_fundo_outras_telas()
        
        texto_titulo = self.fonte_botao.render("CONFIGURAR BATALHA", True, self.cores["texto"])
        self.tela.blit(texto_titulo, (self.largura // 2 - texto_titulo.get_width() // 2, 80))
        
        texto_rounds = self.fonte_botao.render(f"ROUNDS: {self.selecao_rounds}", True, self.cores["texto"])
        self.tela.blit(texto_rounds, (self.largura // 2 - texto_rounds.get_width() // 2, 180))
        
        botoes = [
            (pygame.Rect(self.largura // 2 - 60, 280, 120, 45), "-", "menos"),
            (pygame.Rect(self.largura // 2 - 60, 340, 120, 45), "+", "mais"),
            (pygame.Rect(self.largura // 2 - 120, 420, 240, 50), "CONFIRMAR", "confirmar"),
            (pygame.Rect(self.largura // 2 - 120, 500, 240, 50), "VOLTAR", "voltar"),
        ]
        
        mouse_pos = pygame.mouse.get_pos()
        for rect, texto, acao in botoes:
            self._desenhar_botao(rect, texto, rect.collidepoint(mouse_pos))
            
    def _desenhar_selecao_tanques(self):
        self._desenhar_fundo_outras_telas()
        
        if self.selecao_modo == "simples":
            titulo_txt = "SELECIONE OS TANQUES"
        elif self.selecao_modo == "treinamento":
            titulo_txt = "SELECIONE 1 TANQUE PARA TREINO"
        else:
            titulo_txt = "TORNEIO"
        titulo = self.fonte_botao.render(titulo_txt, True, self.cores["texto"])
        self.tela.blit(titulo, (self.largura // 2 - titulo.get_width() // 2, 50))
        
        info = self.fonte_opcao.render(f"Selecionados: {len(self.tanques_selecionados)}/{len(self.tanques_disponiveis)}", True, self.cores["texto"])
        self.tela.blit(info, (self.largura // 2 - info.get_width() // 2, 100))
        
        panel_larg = 340
        panel_alt = 340
        panel_x = self.largura // 2 - panel_larg // 2
        panel_y = 130
        
        pygame.draw.rect(self.tela, self.cores["fundo_panel"], (panel_x, panel_y, panel_larg, panel_alt), border_radius=8)
        
        y_inicio = panel_y + 15
        espaco = 38
        
        for i, TankClass in enumerate(self.tanques_disponiveis):
            rect = pygame.Rect(panel_x + 15, y_inicio + i * espaco, panel_larg - 30, 32)
            selecionado = i in self.tanques_selecionados
            
            cor_bg = self.cores["botao_selecionado"] if selecionado else self.cores["botao_normal"]
            pygame.draw.rect(self.tela, cor_bg, rect, border_radius=6)
            
            texto = self.fonte_opcao.render(TankClass.__name__, True, self.cores["texto"])
            self.tela.blit(texto, (rect.x + 15, rect.y + 4))
            
            if selecionado:
                check = self.fonte_opcao.render("✓", True, (255, 255, 255))
                self.tela.blit(check, (rect.right - 25, rect.y + 4))
        
        y_botoes = panel_y + panel_alt + 15
        
        if self.selecao_modo == "treinamento":
            texto_iniciar = "INICIAR" if len(self.tanques_selecionados) == 1 else "SELECIONE 1"
        else:
            texto_iniciar = "INICIAR" if len(self.tanques_selecionados) >= 2 else "VOLTAR"

        botoes = [
            (pygame.Rect(panel_x + 10, y_botoes, 150, 40), "SELECIONAR TODOS" if len(self.tanques_selecionados) < len(self.tanques_disponiveis) else "DESMARCAR TODOS", "alternar"),
            (pygame.Rect(panel_x + panel_larg - 160, y_botoes, 150, 40), texto_iniciar, "confirmar"),
        ]
        
        mouse_pos = pygame.mouse.get_pos()
        for rect, texto, acao in botoes:
            self._desenhar_botao(rect, texto, rect.collidepoint(mouse_pos))
    
    def _desenhar_ranking(self):
        self._desenhar_fundo_outras_telas()
        
        titulo_txt = "RESULTADO FINAL" if self.modo_anterior == "simples" else "CLASSIFICAÇÃO"
        titulo = self.fonte_botao.render(titulo_txt, True, self.cores["texto"])
        self.tela.blit(titulo, (self.largura // 2 - titulo.get_width() // 2, 40))
        
        # Ordenar pelo total
        ranking = sorted(self.ranking_resultados.items(), key=lambda x: x[1]["total"] if isinstance(x[1], dict) else x[1], reverse=True)
        
        panel_larg = 700
        panel_alt = 400
        panel_x = self.largura // 2 - panel_larg // 2
        panel_y = 100
        
        pygame.draw.rect(self.tela, self.cores["fundo_panel"], (panel_x, panel_y, panel_larg, panel_alt), border_radius=8)
        
        # Cabeçalho da tabela
        y_header = panel_y + 15
        headers = ["POS", "TANQUE", "VIT/SOB", "DANO", "ACER/ERR", "KILLS", "TOTAL"]
        x_offsets = [15, 60, 200, 310, 400, 520, 610]
        for h, x_off in zip(headers, x_offsets):
            txt = self.fonte_pequena.render(h, True, (150, 150, 150))
            self.tela.blit(txt, (panel_x + x_off, y_header))

        y_inicio = panel_y + 45
        espaco = 45
        
        posicoes = ["1º", "2º", "3º", "4º", "5º", "6º", "7º", "8º"]
        cores_posicoes = [(255, 215, 0), (192, 192, 192), (205, 127, 50), (100, 200, 100), (100, 150, 200)]
        
        for i, (nome, data) in enumerate(ranking):
            if i < 7:
                rect = pygame.Rect(panel_x + 10, y_inicio + i * espaco, panel_larg - 20, 40)
                cor_bg = cores_posicoes[i] if i < len(cores_posicoes) else self.cores["botao_normal"]
                pygame.draw.rect(self.tela, cor_bg, rect, border_radius=6)
                
                # Valores (se for o novo formato de dicionário)
                if isinstance(data, dict):
                    vit_sob = data.get("vitoria", 0) + data.get("sobrevivencia", 0)
                    dano = data.get("dano_causado", 0)
                    acertos = data.get("acertos", 0)
                    erros = data.get("erros", 0)
                    kills = data.get("destruicoes", 0)
                    total = data.get("total", 0)
                else:
                    vit_sob = dano = acertos = erros = kills = 0
                    total = data

                # Renderizar colunas
                self.tela.blit(self.fonte_botao.render(posicoes[i], True, self.cores["texto"]), (rect.x + 5, rect.y + 5))
                self.tela.blit(self.fonte_opcao.render(nome[:15], True, self.cores["texto"]), (rect.x + 50, rect.y + 8))
                
                # Detalhes
                txt_vit = self.fonte_opcao.render(f"+{vit_sob}", True, self.cores["texto"])
                self.tela.blit(txt_vit, (panel_x + 200, rect.y + 8))
                
                txt_dano = self.fonte_opcao.render(f"+{dano*2}", True, self.cores["texto"])
                self.tela.blit(txt_dano, (panel_x + 310, rect.y + 8))
                
                txt_tiros = self.fonte_opcao.render(f"{acertos*10}/-{erros*2}", True, self.cores["texto"])
                self.tela.blit(txt_tiros, (panel_x + 400, rect.y + 8))

                txt_kills = self.fonte_opcao.render(f"{kills}", True, self.cores["texto"])
                self.tela.blit(txt_kills, (panel_x + 520, rect.y + 8))
                
                txt_total = self.fonte_botao.render(f"{total}", True, self.cores["texto"])
                self.tela.blit(txt_total, (panel_x + 610, rect.y + 5))
        
        botao_voltar = pygame.Rect(self.largura // 2 - 130, panel_y + panel_alt + 15, 260, 45)
        mouse_pos = pygame.mouse.get_pos()
        self._desenhar_botao(botao_voltar, "VOLTAR AO MENU", botao_voltar.collidepoint(mouse_pos))
        
    def executar(self):
        # Só reseta se não tem ranking para mostrar
        if not self.ranking_resultados:
            self.estado = "menu_principal"
            self.selecao_modo = None
            self.selecao_rounds = 3
            self.tanques_selecionados = []
        
        while True:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit(0)
                    
                if evento.type == pygame.MOUSEBUTTONDOWN and evento.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    
                    if self.estado == "menu_principal":
                        if hasattr(self, 'rects_menu_principal'):
                            for acao, rect in self.rects_menu_principal.items():
                                if rect.collidepoint(mouse_pos):
                                    self.botao_clicado = acao
                                    break
                                
                    elif self.estado == "selecao_rounds":
                        botoes = [
                            (pygame.Rect(self.largura // 2 - 60, 280, 120, 45), "menos"),
                            (pygame.Rect(self.largura // 2 - 60, 340, 120, 45), "mais"),
                            (pygame.Rect(self.largura // 2 - 120, 420, 240, 50), "confirmar"),
                            (pygame.Rect(self.largura // 2 - 120, 500, 240, 50), "voltar"),
                        ]
                        for rect, acao in botoes:
                            if rect.collidepoint(mouse_pos):
                                self.botao_clicado = acao
                                break
                                
                    elif self.estado == "selecao_tanques":
                        panel_larg = 340
                        panel_alt = 340
                        panel_x = self.largura // 2 - panel_larg // 2
                        panel_y = 130
                        y_inicio = panel_y + 15
                        espaco = 38
                        
                        for i in range(len(self.tanques_disponiveis)):
                            rect = pygame.Rect(panel_x + 15, y_inicio + i * espaco, panel_larg - 30, 32)
                            if rect.collidepoint(mouse_pos):
                                if self.selecao_modo == "treinamento":
                                    self.tanques_selecionados = [i] # No treino, só um pode ser selecionado
                                else:
                                    if i in self.tanques_selecionados:
                                        self.tanques_selecionados.remove(i)
                                    else:
                                        self.tanques_selecionados.append(i)
                                break
                        
                        y_botoes = panel_y + panel_alt + 15
                        botoes = [
                            (pygame.Rect(panel_x + 10, y_botoes, 150, 40), "alternar"),
                            (pygame.Rect(panel_x + panel_larg - 160, y_botoes, 150, 40), "confirmar"),
                        ]
                        for rect, acao in botoes:
                            if rect.collidepoint(mouse_pos):
                                self.botao_clicado = acao
                                break
                                
                    elif self.estado == "ranking":
                        # Usar as mesmas dimensões do _desenhar_ranking
                        panel_alt = 400
                        panel_y = 100
                        botao_voltar = pygame.Rect(self.largura // 2 - 130, panel_y + panel_alt + 15, 260, 45)
                        if botao_voltar.collidepoint(mouse_pos):
                            self.botao_clicado = "voltar"
            
            acao = self.botao_clicado
            self.botao_clicado = None
            
            if self.estado == "menu_principal":
                self._desenhar_menu_principal()
            elif self.estado == "selecao_rounds":
                self._desenhar_selecao_rounds()
            elif self.estado == "selecao_tanques":
                self._desenhar_selecao_tanques()
            elif self.estado == "ranking":
                self._desenhar_ranking()
            
            if acao:
                if self.estado == "menu_principal":
                    if acao == "simples":
                        self.selecao_modo = "simples"
                        self.estado = "selecao_rounds"
                    elif acao == "torneio":
                        self.selecao_modo = "torneio"
                        self.selecao_rounds = len(self.tanques_disponiveis)
                        self.tanques_selecionados = list(range(len(self.tanques_disponiveis)))
                        self.estado = "selecao_tanques"
                    elif acao == "treinamento":
                        self.selecao_modo = "treinamento"
                        self.selecao_rounds = 1
                        self.estado = "selecao_tanques"
                    elif acao == "sair":
                        pygame.quit()
                        sys.exit(0)
                        
                elif self.estado == "selecao_rounds":
                    if acao == "menos" and self.selecao_rounds > 1:
                        self.selecao_rounds -= 1
                    elif acao == "mais" and self.selecao_rounds < 10:
                        self.selecao_rounds += 1
                    elif acao == "confirmar":
                        self.estado = "selecao_tanques"
                    elif acao == "voltar":
                        self.estado = "menu_principal"
                        
                elif self.estado == "selecao_tanques":
                    if acao == "alternar":
                        if len(self.tanques_selecionados) < len(self.tanques_disponiveis):
                            self.tanques_selecionados = list(range(len(self.tanques_disponiveis)))
                        else:
                            self.tanques_selecionados = []
                    elif acao == "confirmar":
                        if self.selecao_modo == "treinamento" and len(self.tanques_selecionados) == 1:
                            return {
                                "modo": self.selecao_modo,
                                "rounds": self.selecao_rounds,
                                "tanques": [self.tanques_disponiveis[self.tanques_selecionados[0]]]
                            }
                        elif self.selecao_modo != "treinamento" and len(self.tanques_selecionados) >= 2:
                            return {
                                "modo": self.selecao_modo,
                                "rounds": self.selecao_rounds,
                                "tanques": [self.tanques_disponiveis[i] for i in self.tanques_selecionados]
                            }
                        else:
                            self.estado = "menu_principal"
                            
                elif self.estado == "ranking":
                    if acao == "voltar":
                        self.estado = "menu_principal"
                        self.ranking_resultados = None
                        self.selecao_modo = None
                        self.selecao_rounds = 3
                        self.tanques_selecionados = []
            
            pygame.display.flip()
            pygame.time.wait(16)