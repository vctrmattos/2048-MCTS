# 2048-MCTS
Implementação de um algoritmo de Monte Carlo para a resolução do jogo 2048.

Nesse projeto, além do jogo tradicional, eu implementei uma automação do 2048, usando o algoritmo de Monte Carlo com algumas pequenas modificações
A ideia foi inspirada por um vídeo do canal Universo Programado.

O algoritmo funciona da seguinte forma:
 O tabuleiro inicial com um arranjo de peças é copiada N vezes para cada movimento possível do tabuleiro naquele momento, digamos que N seja 1000 e que todos movimentos sejam possíveis, assim teriamos 1000 cópias atribuidas para cada movimento, e as cópias atribuidas ao movimento "cima", por exemplo, todas iniciariam com o esse movimento. Depois disso, cada tabuleiro segue se movimentando de maneira aleatória por um certo número de jogadas até ele não ter mais movimentos possíveis (perder),  vencer ou chegar ao limite que nesse programa é chamado de "profundidade". 
Cada tabuleiro tem uma pontuação associada a soma de todos os blocos no tabuleiro, isso será usado para ter uma referência aproximada de bom desempenho.
Durante o processo acima, a pontuação dos tabuleiro de mesmo movimento inicial tem suas pontuações somadas e a direção com a maior pontuação associada será que o algorítmo irá seguir.

Esse algorítmo quando com parâmetro que eu não lembro deu cerca de 42% de sucesso na obtenção do objetivo de 2048, o que não é de todo ruim, mas havia bastante espaço para melhora, principalmente por eu ter observado alguns problemas como: 

-Em várias situações havia 2 blocos de 1024 que não se juntavam por serem sempre interposto por algum outro, de forma que o número de derrotas em parte considerável vinha dessa situação.

- No inicio do 2048 praticamente qualquer movimento gera um avanço e uma derrota é bem improvável, no entanto o programa gastava a mesma quantidade de recursos no início e no fim, o que não faz sentido em questão de eficiência porque a dificuldade aumenta aproximadamente de modo proporcional ao número de jogadas.


