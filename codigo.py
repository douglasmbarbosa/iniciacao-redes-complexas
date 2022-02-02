import igraph as ig
import numpy as np
import math
import random
import time
from functions.other_functions import sol_recalculated, find_r, removalFunction, robustness_failure_node, delete_vertices_seq
from functions.heuristic import heuristic
from functions.tabu_search import search_tabu

ini = time.time()  # horário que o código iniciou

# matriz_adj = np.genfromtxt('./networks/exemplo_rede.txt', delimiter=',') # Gerando a rede a partir de uma matriz de adjacências

#g = ig.Graph.Weighted_Adjacency(matriz_adj.tolist(),attr="weight",mode=ig.ADJ_MAX)

file = './networks/aerial.GraphML'

# 1º Passo: Gerando a rede a partir de um arquivo GraphML
g = ig.Graph.Read_GraphML(file)

N = g.vcount()

for i in range(N):

    # Dando nome aos nós, é o mesmo que o próprio índice
    g.vs[i]['label'] = str(i)

g.vs["name"] = g.vs['label']

# 2º Passo: Gerando dados iniciais
# sequência de nós com base no grau
sol_degree = removalFunction(g, g.degree())
# sequência de nós com base em betweenness
sol_bet = removalFunction(g, g.betweenness())
#sol_random = robustness_failure_node(g, 1000)        # sequência de nós aleatória
sol_bigger_degree = sol_recalculated(g, "degree")   # grau recalculado
sol_bigger_bet = sol_recalculated(g, "betweenness")  # betweenness recalculado
r_bet = find_r(g, sol_bet[1])
# cálculo de R com base na sequência dada
r_degree = find_r(g, sol_degree[1])
#r_random = find_r(g, sol_random[1])

r_bigger_degree = delete_vertices_seq(g, sol_bigger_degree[0])
r_bigger_bet = delete_vertices_seq(g, sol_bigger_bet[0])

# (rede, sequência de nós, valor de r, número de iterações)
#sol_search_tabu = search_tabu(g, sol_degree[2], r_degree, 20)
#sol_heuristic = heuristic(g, sol_degree[2], r_degree, 1000)

sol_search_tabu = search_tabu(g, sol_bet[2], r_bet, 20)
sol_heuristic = heuristic(g, sol_bet[2], r_bet, 1000)
#best_sol = refinement_function(g,sol_bet[2],r_bet,1000)

print(f"\nR Grau = {r_degree}\n"
      f"R Bet = {r_bet}\n"
      #f"R Random = {r_random}\n"
      f"R Grau Recalculado: {r_bigger_degree}\n"
      f"R Betweenness Recalculado: {r_bigger_bet}\n"
      f"R Busca Tabu = {sol_search_tabu[1]}\n"
      f"R Heurística = {sol_heuristic[1]}\n\n"
      f"T Grau = {sol_degree[3]} s\n"
      f"T Bet = {sol_bet[3]} s\n"
      f"T Grau Recalculado: {sol_bigger_degree[1]} s\n"
      f"T Betweenness Recalculado: {sol_bigger_bet[1]} s\n"
      f"T Busca Tabu = {sol_search_tabu[2]} s\n"
      f"T Heurística = {sol_heuristic[2]} s\n")

fim = time.time()   # horário final de execução do código

print("Tempo Total: {} segundos\n".format(fim-ini))
