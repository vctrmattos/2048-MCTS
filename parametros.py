class VarG():
    PROFD_I = 8  # Quantidade inicial de movimentos simulados
    PROFD_PASSO = 16
    PROFD_MAX = 500
    
    N_I = 15  # Número inicial de tabuleiros simulados por tecla
    N_PASSO = 7
    N_MAX = 400
    DIFICULDADE = 2048 # Dificuldade padrao


FPS = 60
ALTURA = 800
LARGURA = 700


# cores inpiradas no 2048 do Duckduckgo
cor_blocos = {
    0:      (150, 150, 150),
    2:      (124, 181, 226),
    4:      (68, 149, 212),
    8:      (47, 104, 149),
    16:     (245, 189, 112),
    32:     (242, 160, 50),
    64:     (205, 136, 41),
    128:    (227, 112, 81),
    256:    (222, 88, 51),
    512:    (189, 74, 43),
    1024:   (84, 84, 218),
    2048:   (59, 60, 153),
    4096:   (255, 215, 0)
}

cor_bg = {
    "fundo":        (51, 51, 51),
    "tabuleiro":    (0, 0),
    "contador":     (0, 0)
}
