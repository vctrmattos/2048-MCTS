# 2048-MCTS
Implementação de um algoritmo de Monte Carlo Tree Search (MCTS) para a resolução do jogo 2048.

Nesse projeto, além do jogo tradicional, eu implementei uma automação do 2048, usando o algoritmo de Monte Carlo com algumas pequenas modificações.
A ideia foi inspirada por um [vídeo](https://www.youtube.com/watch?v=BQ6a8Thjpsk) JVictorDias do canal Universo Programado .

Esse algoritmo também pode ser usado no site do 2048 original através da biblioteca Selenium no modo AUTO - BROWSER.

<img src="https://user-images.githubusercontent.com/76168138/121276344-e52c2780-c8a4-11eb-9d8b-7fc03aa27049.png" width="300" height="300"><img src=
"https://user-images.githubusercontent.com/76168138/121277216-836cbd00-c8a6-11eb-9bcf-c6a5587e4582.png" width="300" height="300"><img src="https://user-images.githubusercontent.com/76168138/121276402-faa15180-c8a4-11eb-9771-8ac7339f0e43.png" width="300" height="300">



# FUNCIONAMENTO

O algoritmo funciona da seguinte forma:
 O tabuleiro inicial com um arranjo de peças é copiada N vezes para cada movimento possível do tabuleiro naquele momento, digamos que N seja 1000 e que todos movimentos sejam possíveis, assim teriamos 1000 cópias atribuidas para cada movimento, e as cópias atribuidas ao movimento "cima", por exemplo, todas iniciariam com o esse movimento. Depois disso, cada tabuleiro segue se movimentando de maneira aleatória por um certo número de jogadas até ele não ter mais movimentos possíveis (perder),  vencer ou chegar ao limite que nesse programa é chamado de "profundidade". 
Cada tabuleiro tem uma pontuação associada a soma de todos os blocos no tabuleiro, isso será usado para ter uma referência aproximada de bom desempenho.
Durante o processo acima, a pontuação dos tabuleiro de mesmo movimento inicial tem suas pontuações somadas e a direção com a maior pontuação associada será que o algorítmo irá seguir e esse loop continua até a vitória ou derrota.

# PROBLEMAS

Esse algorítmo quando com parâmetro que eu não lembro deu cerca de 42% de sucesso na obtenção do objetivo de 2048, o que não é de todo ruim, mas havia bastante espaço para melhora, principalmente por eu ter observado alguns problemas como: 

1 - No inicio do 2048 praticamente qualquer movimento gera um avanço e uma derrota é bem improvável, no entanto o programa gastava a mesma quantidade de recursos no início e em um estado mais avançado do jogo.

2 - Em várias situações havia 2 blocos de 1024 que não se juntavam por serem sempre interposto por algum outro, de forma que o número de derrotas em parte considerável vinha dessa situação.

# SOLUÇÕES

Já quanto ao 1 problema, adicionei quatro novas variáveis globais chamadas PRFND_I, PRFND_PASSO, N_I e N_PASSO que são, respectivamente, a profundidade inicial e o passo em que ela, a quantidade de cópias e o passo em que ela aumenta. Com isso a pronfundidade e número de cópias aumentam linearmente com o número de jogadas, além disso fiz com que esses acréscimos só começassem a ocorrer depois da jogada número 100.

Na primeira tentativa para melhorar a porcentagem de sucesso, eu criei uma espécie de punição para o tabuleiro perdedores, de forma que a pontuação fosse subtraída ao invés de somada a tecla correspondente e dividi pelo número de jogadas feitas até a derrota elevado ao quadrado visando diminuir a punição na medida que a derrota ocorresse mais longe. Isso não levou a mudança positivas e tentei verificar se ao aumentar a punição multiplicando por -1000 a pontuação, iria acontecer algo e, de fato aconteceu, o resultado piorou muito, saindo dos 42% para por volta de 10%.

Depois de pensar um pouco e perceber o problema 2, adaptei essa mesma ideia para dar um incentivo aos tabuleiros vencedores ao invés de subtrair o programa soma a pontuação com multicada por 1000. Apesar da ideia similar, os impactos foram bastante positivos aumentando a taxa de sucesso para 69% fazendo essas duas melhorias.

Inclusive depois disso foi possível alcançar o bloco de 4096, apesar de somente em 22% dos teste realizados e demorar quase 25 minutos para isso.


# ALGUNS DADOS:
| OBJETIVO | 2048 | 2048 | 4096 |
|:-:|:-:|:-:|:-:|
| Profundidade inicial | 8 | 8 | 8 |
| Passo da profundidade | 20 | 16 | 15 |
| Cópias por tecla (N) | 15 | 15 | 15 |
| Passo do N | 8 | 7 | 6 |
| Media de Tempo (s) | 311.537 | 425.355 | 1.444.058 |
| Taxa de vitória (%) | 69 | 80 | 22 |


O código no geral não está perto de bem otimizado ou construido, mas cumpriu com os objetivos que eu buscava, talvez no futuro eu o melhore.
