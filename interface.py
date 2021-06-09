import pygame, sys, pygame_menu, time
from pygame.locals import K_UP, K_DOWN, K_RIGHT, K_LEFT, K_q
from pygame_menu import sound
from pygame_menu import menu
from pygame_menu.locals import ALIGN_CENTER, ALIGN_LEFT, ALIGN_RIGHT, POSITION_CENTER

from tabuleiro import *
from parametros  import * 
from browserr import *

from selenium.common.exceptions import StaleElementReferenceException
from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver

#Funções gráficas
def desenhar_tabuleiro(tabuleiro):
    tela.fill(cor_bg["fundo"])
    posx = 60
    posy = 40
    lado = altura = 120

    for i in tabuleiro.tabuleiro:
        for j in i:
            pygame.draw.rect(tela, cor_blocos[j], pygame.Rect(posx, posy, lado,altura),border_radius=3)
            if j == 0:
                j = " " 
            numero = fonte.render(str(j), True, (0,0,0))
            pos_text = numero.get_rect(center=(posx + lado//2, posy + altura//2))
            tela.blit(numero, pos_text)
            posx += (LARGURA - 100)//4
        posy += (ALTURA - 210)//4
        posx = 60
    
    #pygame draw.rect(tela,cores.bg["contador"])

def desenhar_mensagem(mensagem):
    largura = 500
    altura = 300
    posy = 100
    posx = LARGURA//2 - largura//2

    #FRAME
    pygame.draw.rect(tela, (20, 20, 20), pygame.Rect(posx, posy, largura, altura), width=10)
    pygame.draw.rect(tela, (70, 74, 82), pygame.Rect(posx, posy, largura, altura), border_radius=4)
    numero = fonte_mensagem.render(mensagem, True, (210,210,210))
    centro_texto = numero.get_rect(center=(posx + largura//2, 160))
    tela.blit(numero, centro_texto)

    #BOTAO TENTAR NOVAMENTE
    botao1 = pygame.Rect(posx + 15, posy + 150, 210, 90)
    pygame.draw.rect(tela, (90, 100, 200), botao1, width=0)
    pygame.draw.rect(tela, (20, 20, 20), botao1, width=8)
    tentar = fonte_mensagem_25.render("TENTAR", True, (210,210,210))
    novamente = fonte_mensagem_25.render("NOVAMENTE", True, (210,210,210))
    tela.blit(tentar, (165,265))
    tela.blit(novamente, (135,295))

    #BOTAO MENU    
    botao2 = pygame.Rect(posx + 265, posy + 150, 210, 90)
    pygame.draw.rect(tela, (90, 100, 200), botao2, width=0)
    pygame.draw.rect(tela, (20, 20, 20), botao2, width=8)
    texto_menu = fonte_mensagem_35.render("MENU", True, (210,210,210))
    tela.blit(texto_menu, (415, 275))
    tela.blit(tela, (0,0))

    pygame.display.update()

    #DETECTAR COLISAO
    while True:
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sys.exit()

            if evento.type == pygame.MOUSEBUTTONUP:
                mouse_pos = evento.pos 
                if evento.button == 1:
                    if botao1.collidepoint(mouse_pos):
                        return "tentar"
                    elif botao2.collidepoint(mouse_pos):
                        return "menu"

def desenhar_score(tabuleiro):
    posx = 480
    posy = 620
    largura = 180
    altura = 65
    pygame.draw.rect(tela, (200,200,200), pygame.Rect(posx, posy, largura, altura), 3, border_radius=2)
    pontos = tabuleiro.pontos
    texto = "Score:  " + str(pontos)
    numero = fonte_score.render(texto, True, (200,200,200))
    centro_texto = numero.get_rect(center=(posx + largura//2, posy + altura//2))
    tela.blit(numero, centro_texto)

def desenhar_b_menu():
    posx = 40
    posy = 620
    largura = 180
    altura = 65
    botao = pygame.Rect(posx, posy, largura, altura)
    pygame.draw.rect(tela, (200,200,200), botao, 3, border_radius=2)
    texto = "MENU"
    numero = fonte_score.render(texto, True, (200,200,200))
    centro_texto = numero.get_rect(center=(posx + largura//2, posy + altura//2))
    tela.blit(numero, centro_texto)
    return botao

def desenhar_b_menu_maior():
    posx = 40
    posy = 620
    largura = 180
    altura = 65
    botao = pygame.Rect(posx, posy, largura, altura)
    pygame.draw.rect(tela, (200,200,200), botao, 3, border_radius=2)
    texto = "MENU"
    numero = fonte_mensagem_60.render(texto, True, (200,200,200))
    centro_texto = numero.get_rect(center=(posx + largura//2, posy + altura//2))
    tela.blit(numero, centro_texto)
    return botao


def menus():
    tema = pygame_menu.Theme(
                            background_color=cor_bg["fundo"], 
                            title_font=pygame_menu.font.FONT_8BIT, 
                            title_font_shadow=True,
                            title_font_shadow_color=(100,100,100),
                            title_font_shadow_offset=6,
                            title_font_size=110,
                            title_offset=(LARGURA//2 - 220, 60),
                            title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_NONE,
                            widget_font_size=40,
                            widget_background_color=(90,90,90),
                            widget_padding=(20,90),
                            widget_font = pygame_menu.font.FONT_NEVIS
    )
    
    tema2 = pygame_menu.themes.THEME_DARK.copy()
    tema2.background_color=cor_bg["fundo"]
    tema2.title_bar_style=pygame_menu.widgets.MENUBAR_STYLE_ADAPTIVE
    tema2.title_background_color=(40,40,40)    
    tema2.title_font_size = 50
    tema2.widget_margin = (0,0)
    tema2.scrollbar_cursor = pygame_menu.locals.CURSOR_HAND
    tema2.title_font= pygame_menu.font.FONT_NEVIS


    #MENU SOBRE - Informações gerais sobre o programa.
    menu_sobre = pygame_menu.Menu(
                            title="SOBRE", 
                            height=ALTURA, 
                            width=LARGURA, 
                            center_content=True, 
                            theme=tema2
    )

    frases = ['Normal: É o 2048 tradicional, use as setas do teclado para mover os blocos. Blocos com o mesmo número serão adicionados em um só. Adicione-os até atingir 2048 (ou outro valor, a depender da dificuldade).', 'Auto: Através de um algoritmo baseado na busca em árvore de Monte Carlo, o programa calculará o melhor movimento e jogará sozinho.', 'Auto - Browser: Será feito o mesmo do modo anterior, com a diferença que será em um browser (Firefox) no site do 2048 original (www.play2048.co), o programa continua rodando até vencer.']
    menu_sobre.add.label("O jogo possui 3 modos:",  align=ALIGN_LEFT, padding=(20,20),margin=(5,5) ,max_char=42, underline=True, )
    for frase in frases:
        menu_sobre.add.label(frase, align=ALIGN_LEFT, padding=(1, 20), max_char=44)
        menu_sobre.add.vertical_margin(30)
    
    menu_sobre.add.label("Para mais informações ", align=ALIGN_CENTER, padding=(1, 20) ,max_char=40)
    menu_sobre.add.url("https://www.github.com/Victor-Mattos")
    menu_sobre.add.vertical_margin(120)
    

    #MENU_MODOS - Modos de jogo
    tema3 = tema2.copy()
    tema3.widget_padding = (20,90)
    tema3.widget_font_size=40
    tema3.widget_font=pygame_menu.font.FONT_NEVIS
    menu_modos = pygame_menu.Menu(
                                   title="MODOS",
                                   height=ALTURA,
                                   width=LARGURA,
                                   center_content=True,
                                   theme=tema3
    )
    menu_modos.add.button("NORMAL", jogar_normal)
    menu_modos.add.vertical_margin(25)
    menu_modos.add.button("AUTO", jogar_auto)
    menu_modos.add.vertical_margin(25)
    menu_modos.add.button("AUTO - BROWSER", jogar_auto_browser)
    menu_modos.add.vertical_margin(100)
    

    #MENU PRINCIPAL
    global menu
    menu = pygame_menu.Menu(
                            title="2048", 
                            height=ALTURA, 
                            width=LARGURA, 
                            center_content=True, 
                            theme=tema
    )
    engine = sound.Sound()
    engine.set_sound(sound.SOUND_TYPE_KEY_ADDITION, "audio/pop.ogg")
    engine.set_sound(pygame_menu.sound.SOUND_TYPE_CLICK_MOUSE, "audio/pop.ogg")

    menu.set_sound(engine, recursive=True)
    menu_modos.set_sound(engine)
    menu.add.vertical_margin(25)
    menu.add.button("JOGAR", menu_modos)
    menu.add.vertical_margin(25)
    menu.add.dropselect('', 
                        [
                            ("DIFICIL (2048)", 2048), 
                            ("MEDIO (1024)", 1024),
                            ("FACIL (512)", 512),
                            ("MINIMA (32)", 32)
                        ], 
                        margin=(10,10), 
                        placeholder="DIFICULDADE",
                        selection_box_inflate=(10, 10),
                        selection_box_width=320,
                        selection_box_bgcolor=(100,100,100),
                        selection_box_border_color=(100, 100,100),
                        selection_option_font_size=36,
                        padding=(10, 18, 10, 0),
                        placeholder_add_to_selection_box=False, 
                        selection_option_selected_font_color=(110,50,110),
                        selection_option_font_color=(210,210,210),
                        default=0,
                        align=ALIGN_CENTER,
                        onchange=mudar_dificuldade
    )
    menu.add.vertical_margin(25)
    menu.add.button("SOBRE", menu_sobre)
    menu.add.vertical_margin(25)
    menu.add.button("SAIR", pygame_menu.events.EXIT)
    menu.add.vertical_margin(25)


#Funções dos modos de jogo
def jogar_normal():
    while True:
        tabuleiro = Tabuleiro([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
        tabuleiro.dois_ou_quatro()
        tabuleiro.dois_ou_quatro()

        ganhou = perdeu = sair = False
        
        desenhar_tabuleiro(tabuleiro)
        desenhar_score(tabuleiro)
        botao = desenhar_b_menu()
        pygame.display.update()

        while not (ganhou or perdeu):
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                elif evento.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = evento.pos
                    if evento.button == 1:
                        if botao.collidepoint(mouse_pos):
                            return
                elif evento.type == pygame.KEYDOWN: #Checa se alguma tecla foi pressionada
                    teclas = pygame.key.get_pressed()   #Armazena todas as teclas pressionadas em um dicionario, 1 se pressionada e 0 caso contrario
                    if teclas[K_UP]:
                        tabuleiro.cima()
                    elif teclas[K_DOWN]:
                        tabuleiro.baixo()
                    elif teclas[K_RIGHT]:
                        tabuleiro.direita()
                    elif teclas[K_LEFT]:
                        tabuleiro.esquerda() 
                    else:
                        continue                        
                
                    tabuleiro.dois_ou_quatro()
                    perdeu, ganhou = tabuleiro.perdeu(), tabuleiro.ganhou()
                    desenhar_tabuleiro(tabuleiro)
                    desenhar_score(tabuleiro)
                    desenhar_b_menu()
                    pygame.display.update()

        if perdeu:
            escolha = desenhar_mensagem("GAME OVER")

        elif ganhou:
            som = pygame.mixer.Sound('audio/vitoria.wav')
            som.play()
            time.sleep(2)
            escolha = desenhar_mensagem("PARABENS!")
            
        
        pygame.display.update()
        
        if escolha == "novamente":
            continue
        elif escolha == "menu":
            return

def jogar_auto():
    while True:
        tabuleiro = Tabuleiro([[0,0,0,0],[0,0,0,0],[0,0,0,0],[0,0,0,0]])
        tabuleiro.dois_ou_quatro()
        tabuleiro.dois_ou_quatro()
        tempo = pygame.time.Clock()
        
        ganhou = perdeu = sair = False
        n = VarG.N_I
        profund = VarG.PROFD_I
        num_moves = 0

        desenhar_tabuleiro(tabuleiro)
        desenhar_score(tabuleiro)
        botao = desenhar_b_menu()
        pygame.display.update()

        while not (ganhou or perdeu):     
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                        sys.exit()

                elif evento.type == pygame.MOUSEBUTTONUP:
                    mouse_pos = evento.pos
                    if evento.button == 1:
                        if botao.collidepoint(mouse_pos):
                            return

            tecla = tabuleiro.melhor(profund, n)
            tabuleiro.mover(tecla)
            num_moves += 1
            tabuleiro.dois_ou_quatro()
            ganhou = tabuleiro.ganhou()
            perdeu = tabuleiro.perdeu()
            if profund < VarG.PROFD_MAX and num_moves > 100:
                profund = num_moves//VarG.PROFD_PASSO + VarG.PROFD_I
            if n < VarG.N_MAX and num_moves > 100:
                n = num_moves//VarG.N_PASSO + VarG.N_I

            tempo.tick(FPS)   
            desenhar_tabuleiro(tabuleiro)
            desenhar_score(tabuleiro)
            desenhar_b_menu()
            pygame.display.update()
        
        if perdeu:
            escolha = desenhar_mensagem("GAME OVER")
        elif ganhou:
            escolha = desenhar_mensagem("PARABENS!")
        
        pygame.display.update()
        
        if escolha == "novamente":
            continue
        elif escolha == "menu":
            return

def jogar_auto_browser():
    global driver
    driver = Firefox()
    browser = Browser(driver)
    tab = Tabuleiro()

    
    while True:
        n = VarG.N_I
        profund = VarG.PROFD_I
        num_moves = 0
        perdeu = ganhou = False
        while True:
            try:
                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                            pygame.quit()
                            sys.exit()
                perdeu = browser.perdeu_browser()
                if perdeu:
                    browser.jogar_novamente()
                    break
                if ganhou:
                    return
                tabuleiro_atual = browser.pegar_tabuleiro()
                tab.tabuleiro = tabuleiro_atual
                tecla = tab.melhor(profund, n)
                browser.enviar_tecla(tecla)
                if profund < VarG.PROFD_MAX and num_moves > 100:
                    profund = num_moves//VarG.PROFD_PASSO + VarG.PROFD_I
                if n < VarG.N_MAX and num_moves > 100:
                    n = num_moves//VarG.N_PASSO + VarG.N_I
                num_moves += 1
                ganhou = browser.ganhou_browser()
                pygame.display.update()

            except StaleElementReferenceException:
                pass

            except Exception:
                return

            if ganhou:
                return
    
def mudar_dificuldade(_, dificuldade):
    VarG.DIFICULDADE = dificuldade

def main():
    pygame.init()
    pygame.mixer.init()
    pygame.display.set_caption("2048")
    global tela
    tela = pygame.display.set_mode((LARGURA, ALTURA))
    
    pygame.font.init()
    global fonte
    fonte = pygame.font.SysFont(None, 70)
    
    global fonte_score
    fonte_score = pygame.font.SysFont(None, 40)
    
    global fonte_mensagem
    fonte_mensagem = pygame.font.Font(pygame_menu.font.FONT_NEVIS, 50)

    global fonte_mensagem_25
    fonte_mensagem_25 = pygame.font.Font(pygame_menu.font.FONT_NEVIS, 25)

    global fonte_mensagem_35
    fonte_mensagem_35 = pygame.font.Font(pygame_menu.font.FONT_NEVIS, 35)

    global fonte_mensagem_60
    fonte_mensagem_60 = pygame.font.Font(pygame_menu.font.FONT_NEVIS, 60)

    menus()
    menu.mainloop(tela)


if __name__== "__main__":
    main()