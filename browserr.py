from selenium.webdriver import Firefox
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.webdriver import WebDriver
from tabuleiro import *
from interface import desenhar_b_menu, desenhar_mensagem


class Browser:
    def __init__(self, driver):
        self.driver = driver
        self.driver.get('https://gabrielecirulli.github.io/2048/')

    def pegar_tabuleiro(self):
        html = self.driver.find_elements_by_xpath("//div[@class='tile-container']/div")
        tabuleiro = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        for bloco in html:
            classe = (bloco.get_attribute("class")).split(" ")
            linha = int(classe[2][16]) - 1
            coluna = int(classe[2][14]) - 1
            valor = int(classe[1].split('-')[1])
            tabuleiro[linha][coluna] = valor
        return tabuleiro

    def enviar_tecla(self, tecla):
        elem = self.driver.find_element_by_tag_name('body')
        elem.send_keys(self.interpretar_tecla(tecla))

    def perdeu_browser(self):
        try:
            mensagem = self.driver.find_element_by_xpath("//div[@class='game-message game-over']")
            return True
        except Exception:
            return False
    
    def interpretar_tecla(self, tecla):
        if tecla == 'c':
            return Keys.ARROW_UP
        elif tecla == 'b':
            return Keys.ARROW_DOWN
        elif tecla == 'd':
            return Keys.ARROW_RIGHT
        elif tecla == 'e':
            return Keys.ARROW_LEFT

    def jogar_novamente(self):
        try:
            self.driver.find_element_by_xpath("//a[@class='retry-button']").click()
        except Exception:
            pass

    def ganhou_browser(self):
        try:
            mensagem = self.driver.find_element_by_xpath("//div[@class='game-message game-won']")
            return True
        except Exception:
            return False
