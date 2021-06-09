import random
import copy
from parametros import *

#Contem tudo relacionado ao funcionamento interno do tabuleiro

def transpor_matriz(matriz):
    '''
    Troca a linhas de uma matriz por suas colunas.

    list -> list
    '''
    nova = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
    for i in range(len(matriz)):
        for j in range(len(matriz[0])):
            nova[j][i] = matriz[i][j]
    return nova


class Tabuleiro:
    def __init__(self, tabuleiro=[[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]], pontos=0):
        self.tabuleiro = tabuleiro
        self.pontos = pontos

    def direita(self):
        '''A função desloca os elementos do tabuleiro para a direita e, se elementos adjacentes na linha tiverem o mesmo valor,
        eles serão somados.
        list -> None'''
        self.pontos = 0
        for i in range(len(self.tabuleiro)):
            # Se houver pelo menos algum zero, ele será removido
            if 0 in self.tabuleiro[i]:
                contador = 0
                qnt_de_zeros = self.tabuleiro[i].count(0)
                while contador < qnt_de_zeros:
                    self.tabuleiro[i].remove(0)
                    contador += 1

            # Lista auxiliar usada para evitar que um elemento récem formado seja somado a outro
            lista_aux = self.tabuleiro[i][:]
            for j in range(len(lista_aux) - 1, 0, -1):
                if lista_aux[j] == lista_aux[j - 1]:
                    self.tabuleiro[i][j] *= 2
                    self.tabuleiro[i].pop(j - 1)
                    self.tabuleiro[i].insert(0, 0)

                    lista_aux[j] = -1
                    lista_aux.pop(j - 1)
                    lista_aux.insert(0, 0)

            self.pontos += sum(self.tabuleiro[i])  # Adiciona a pontuação
            self.tabuleiro[i] = [0] * \
                (4 - len(self.tabuleiro[i])) + self.tabuleiro[i]

    def esquerda(self):
        '''
        A função desloca os elementos do tabuleiro para a esquerda e, se elementos adjacentes tiverem o mesmo valor, 
        eles serao somados.
        list -> None
        '''
        self.pontos = 0
        for i in range(len(self.tabuleiro)):

            # Se houver pelo menos algum zero, ele sera removido
            if 0 in self.tabuleiro[i]:
                contador = 0
                qnt_de_zeros = self.tabuleiro[i].count(0)
                while contador < qnt_de_zeros:
                    self.tabuleiro[i].remove(0)
                    contador += 1

            lista_aux = self.tabuleiro[i][:]  # Lista auxiliar
            for j in range(len(lista_aux) - 1):
                if lista_aux[j] == lista_aux[j + 1]:
                    self.tabuleiro[i][j] *= 2
                    self.tabuleiro[i].pop(j + 1)
                    self.tabuleiro[i].append(0)

                    lista_aux[j] = -1
                    lista_aux.pop(j + 1)
                    lista_aux.append(0)

            self.pontos += sum(self.tabuleiro[i])  # Adiciona a pontuação
            self.tabuleiro[i].extend([0] * (4 - len(self.tabuleiro[i])))

    def cima(self):
        '''
        A função desloca os elementos do tabuleiro para cima e, se elementos adjacentes na coluna tiverem o mesmo valor, 
        eles serão somados.

        list -> None
        '''
        self.tabuleiro = transpor_matriz(self.tabuleiro)
        self.esquerda()
        self.tabuleiro = transpor_matriz(self.tabuleiro)

    def baixo(self):
        '''
        A função desloca os elementos do tabuleiro para baixo e, se elementos adjacentes na coluna tiverem o mesmo valor, 
        eles serão somados.

        list -> None
        '''
        self.tabuleiro = transpor_matriz(self.tabuleiro)
        self.direita()
        self.tabuleiro = transpor_matriz(self.tabuleiro)

    def dois_ou_quatro(self):
        '''
        Adiciona um 2 ou 4 no tabuleiro em uma posicao vazia, com 90% de chance de ser um 2 e 10% de ser um 4 (as chances podem 
        ser alteradas por meio da lista probablilidade).

        list --> None
        '''
        probabilidade = [2, 2, 2, 2, 2, 2, 2, 2, 2, 4]# O 2 tera 90% de chance de ser adicionado.
        num = random.choice(probabilidade)
        vagos = []
        for i in range(len(self.tabuleiro)):
            for j in range(len(self.tabuleiro)):
                if self.tabuleiro[i][j] == 0:
                    # armazena na lista vagos uma tupla com a linha e coluna dos elementos iguais a 0
                    vagos.append((i, j))
        if len(vagos) == 0:
            return
        pos = random.choice(vagos)  # Sorteia uma das tuplas dentro de vagos
        self.tabuleiro[pos[0]][pos[1]] = num
        self.pontos += num

    def mover(self, move):
        '''
        Realiza um movimento no tabuleiro ao se informar a letra correspondente.

        str -> None  
        '''
        if move == 'c':
            self.cima()
        elif move == 'b':
            self.baixo()
        elif move == 'd':
            self.direita()
        elif move == 'e':
            self.esquerda()

    def aleatorio(self):
        '''
        Realiza um movimento aleatório no tabuleiro.

        None -> None
        '''
        moves = ['c', 'b', 'd', 'e']
        self.mover(random.choice(moves))

    def melhor(self, profund, n):
        tab = copy.deepcopy(self.tabuleiro)
        copia = Tabuleiro(tab)
        teclas = ['e', 'd', 'c', 'b']
        pontos = {'e': 0, 'd': 0, 'c': 0, 'b': 0}

        # Verica quais sãos as possibilidades para o primeiro movimento
        for tecla in teclas:
            tab1 = copy.deepcopy(self.tabuleiro)
            copia1 = Tabuleiro(tab1)
            copia1.mover(tecla)
            if copia1.tabuleiro == copia.tabuleiro:
                del pontos[tecla]
        teclas = pontos.keys()
        for tecla in teclas:
            for _ in range(n):
                copia = Tabuleiro(copy.deepcopy(tab))
                ganhou, perdeu = copia.ganhou(), copia.perdeu()
                count = 0
                copia.mover(tecla)
                while not perdeu and not ganhou and count < profund:
                    copia.dois_ou_quatro()
                    copia.aleatorio() 
                    ganhou, perdeu = copia.ganhou(), copia.perdeu()
                    count += 1
                # if perdeu:
                #     pontos[tecla] -= (copia.pontos)/(count + 1)**2
                # else:
                #     pontos[tecla] += copia.pontos
                if ganhou:
                    pontos[tecla] += 1000*copia.pontos
                pontos[tecla] += copia.pontos
        return max(pontos, key=lambda key: pontos[key])

    def perdeu(self):
        '''
        A função determina se há algum movimento possível no jogo 2048. Caso não haja,
        o retorno será False, se houver, True.

        list -> bool
        '''
        temp = Tabuleiro(copy.deepcopy(self.tabuleiro))

        temp.esquerda()
        if temp.tabuleiro == self.tabuleiro:
            temp.direita()
            if temp.tabuleiro == self.tabuleiro:
                temp.cima()
                if temp.tabuleiro == self.tabuleiro:
                    temp.baixo()
                    return True
        return False

    def ganhou(self):
        for linha in self.tabuleiro:
            if VarG.DIFICULDADE in linha:
                return True
        return False
