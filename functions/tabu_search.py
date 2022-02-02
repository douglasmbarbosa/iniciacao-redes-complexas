
import random
import math
import time
from functions.other_functions import delete_vertices_seq


def search_tabu(g, best_sol, r_best_sol, iter_max):

    ini = time.time()

    # 4º Passo: Execução da função de refinamento
    g_copy = g.copy()

    # gerando vizinho

    # se temos uma sequência [0,1,2,3], podemos gerar um vizinho [2,1,0,3]

    # Então, eu calculo o R pra essa sequência gerada

    iter = 0  # contador de iterações
    best_iter = 0

    n = math.ceil(len(best_sol)*0.5)

    neighbor = best_sol.copy()  # o vizinho inicial é a melhor sequência
    best_neighbor = neighbor.copy()
    tabu_list = [None]*100  # lista tabu

    r_neighbor = 1  # valor maior que qualquer outro valor de R

    while (iter < iter_max):

        '''
        1) Fazemos trocas entre os nós entre o nó N e o nó final da rede.

        2) Se temos uma rede com 10 nós e J = 0.3, N = 10*0.3 = 3. 

        3) Dessa forma, geramos dois valores inteiros aleatórios entre 3 e 9, e trocamos eles de posição.

        '''
        y = 50
        list_r_neighbor = []
        list_seq_neighbor = []

        A = r_best_sol

        while len(list_seq_neighbor) < y:  # serão gerados Y vizinhos

            neighbor = best_neighbor
            swap = [random.randint(n, len(best_sol)-1),
                    random.randint(n, len(best_sol)-1)]
            x1 = ([swap[0], swap[1]]) in tabu_list
            y1 = ([swap[1], swap[0]]) in tabu_list
            # print(list(swap[0]))

            if (swap[0] != swap[1]) \
                & (x1 == False) \
                    & (y1 == False):  # os números inteiros gerados precisam ser diferentes

                tabu_list.pop(0)  # eliminando o primeiro da fila
                tabu_list.append(swap)  # introduzindo o último na fila

                x = neighbor[(swap[0])]
                # Fazemos a troca de posições
                neighbor[(swap[0])] = neighbor[(swap[1])]
                neighbor[(swap[1])] = x
                # calculamos R para essa nova sequência gerada
                r_neighbor = delete_vertices_seq(g_copy, neighbor)

                list_r_neighbor.append(r_neighbor)
                list_seq_neighbor.append(neighbor)

            elif (swap[0] != swap[1]):

                x = neighbor[(swap[0])]
                # Fazemos a troca de posições
                neighbor[(swap[0])] = neighbor[(swap[1])]
                neighbor[(swap[1])] = x
                # calculamos R para essa nova sequência gerada
                r_neighbor = delete_vertices_seq(g_copy, neighbor)

                if (r_neighbor < A):

                    r_best_sol = r_neighbor
                    A = r_best_sol

        # print(list_r_neighbor)
        # print(list_r_neighbor.index(min(list_r_neighbor)))
        best_neighbor = list_seq_neighbor[(
            list_r_neighbor.index(min(list_r_neighbor)))]

        if (min(list_r_neighbor) < r_best_sol):  # se o R da sequência gerada for menor que o melhor R

            best_iter = iter

            #iter = 0

            # registramos o melhor valor gerado
            r_best_sol = list_r_neighbor[(
                list_r_neighbor.index(min(list_r_neighbor)))]

            best_sol = list_seq_neighbor[(
                list_r_neighbor.index(min(list_r_neighbor)))]

        #tabu_list = [None]*200
        print(f"busca tabu {iter}")

        iter = iter + 1
        # print(iter)

    tempo = time.time() - ini

    return best_sol, r_best_sol, tempo  # 5º Passo: Retorno da função
