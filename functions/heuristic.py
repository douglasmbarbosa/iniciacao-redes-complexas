import time
import random
import math
from functions.other_functions import delete_vertices_seq

def heuristic(g, best_sol,r_best_sol,iter_max): 

    ini = time.time()

    # 4º Passo: Execução da função de refinamento

    g_copy = g.copy()
            
    
    # gerando vizinho

    # se temos uma sequência [0,1,2,3], podemos gerar um vizinho [2,1,0,3]

    # Então, eu calculo o R pra essa sequência gerada

    iter = 0 # contador de iterações

    n =  math.ceil(len(best_sol)*0.5)
    
    neighbor = best_sol.copy()  # o vizinho inicial é a melhor sequência

    while (iter < iter_max):
          
        #print("{:.2f}, {}, {}".format(j, n, len(best_sol)-1))
        swap1 = random.randint(n,len(best_sol)-1)
        swap2 = random.randint(n,len(best_sol)-1)

        '''
        1) Fazemos trocas entre os nós entre o nó N e o nó final da rede.

        2) Se temos uma rede com 10 nós e J = 0.3, N = 10*0.3 = 3. 

        3) Dessa forma, geramos dois valores inteiros aleatórios entre 3 e 9, e trocamos eles de posição.

        '''
    
        if (swap1 != swap2): # os números inteiros gerados precisam ser diferentes
            print(f"heurística {iter}")
            x = neighbor[swap1]
            neighbor[swap1] = neighbor[swap2] # Fazemos a troca de posições
            neighbor[swap2] = x

            r_neighbor = delete_vertices_seq(g_copy,neighbor)

            # calculamos R para essa nova sequência gerada

            if (r_neighbor < r_best_sol): # se o R da sequência gerada for menor que o melhor R

                i = iter

                print(i)

                #iter = 0

                r_best_sol = r_neighbor # registramos o melhor valor gerado 

                best_sol = neighbor.copy()

        iter = iter + 1

        #print(iter) 

        tempo = time.time() - ini 

    return best_sol, r_best_sol, tempo # 5º Passo: Retorno da função