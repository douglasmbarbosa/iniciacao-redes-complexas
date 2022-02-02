import numpy as np
import matplotlib.pyplot as plt
import igraph as ig
import random
import math
import time
import pandas as pd
from geneticalgorithm import geneticalgorithm as ga

def sol_recalculated(g, metric):

    ini = time.time()

    g_copy = g.copy()

    N = g_copy.vcount()
   
    for i in range (N):   

        g_copy.vs[i]['label'] = str(i) # Dando nome aos nós, é o mesmo que o próprio índice

    g_copy.vs["name"] = g_copy.vs['label']

    seq = []
    
    if (metric == "degree"):

        for i in range (N):
            grau =  g_copy.degree()
            maior =  max(grau)

            index = grau.index(maior)
            
            seq.append(int(g_copy.vs["name"][index]))
            
            g_copy.delete_vertices(index)

    elif (metric == "betweenness"):

        for i in range (N):
            bet =  g_copy.betweenness()
            maior =  max(bet)

            index = bet.index(maior)
            
            seq.append(int(g_copy.vs["name"][index]))
            
            g_copy.delete_vertices(index)

    tempo = time.time() - ini

    return seq, tempo



def find_r(g,P_infty): # cálculo de R

    r = 0

    for i in range(g.vcount()):

        r = r + P_infty[i+1]

    r = r *(1/g.vcount())

    return r

def delete_vertices_seq(g, X): # remoção de nós com base em uma sequência dada, retornando R
                        

    g_copy = g.copy()

    label = []

    for i in range (len(X)):

        lbl = g_copy.vs[int(X[i])]['label']

        label.append(str(lbl))   

    #-------------------------remoção_de_nós---------------------------
    
    N = g_copy.vcount()
    
    number_removed = np.zeros(N+1)

    for i in range(g_copy.vcount()):

        number_removed[i] = i / float(N)

    number_removed[N] = 1.0

    P_infty = np.zeros(N + 1)

    # Find larger component

    #cl = g_copy.components()

    #P_infty_baseline = float(max(cl.sizes()))
    P_infty_baseline = float(g.clusters().giant().vcount())

    P_infty[0] = 1.0

    count = 1

    while (g_copy.vcount() > 0):

        seq = g_copy.vs.select(label_eq = label[count-1])

        g_copy.delete_vertices(seq[0].index)
        
        #cl = g_copy.components()

        #if(len(cl) > 0):
        lc = g_copy.clusters()
        if (lc):

            P_infty[count] += float(lc.giant().vcount()) / P_infty_baseline 

        else:

            P_infty[count] += 0.0 

        count = count + 1

    if(count < g.vcount()):
        number_removed = number_removed[0:count]
        P_infty = P_infty[0:count]

    return find_r(g,P_infty)

def removed(g): # número de nós removidos

    N = g.vcount()
    number_removed = np.zeros(N+1)
    for i in range(g.vcount()):
        number_removed[i] = i / float(N)
    number_removed[N] = 1.0

    return number_removed


def removalFunction(g, metric): #falhas com base em alguma métrica
    ini = time.time()

    N = g.vcount()
    g_copy = g.copy()
    seq = [] #sequência de nós removidos 
 
    number_removed = removed(g_copy)

    P_infty = np.zeros(N+1)

	# Find larger component
    #cl = g_copy.components()
    P_infty_baseline = float(g.clusters().giant().vcount())

    P_infty[0] = 1.0

    #removaList = np.zeros(N+1)
    #removaList[0] = 1.0
    count = 1
    while g_copy.vcount() >= 1:
        #ig.plot(g_copy)
            
        _max = max(metric)
        index = metric.index(_max)

        seq.append(int(g_copy.vs['name'][index]))
        
        #ig.plot(g_copy)
        g_copy.delete_vertices(index)
    
        del metric[index]
        #cl = g_copy.components()
        #removaList[count] =  max(clusters.sizes())/N
        lc = g_copy.clusters()
        if (lc):

            P_infty[count] += float(lc.giant().vcount()) / P_infty_baseline  
        else:
            P_infty[count] += 0.0

        count+=1
    if(count < g.vcount()):
        number_removed = number_removed[0:count]
        P_infty = P_infty[0:count]
    
    tempo = time.time() - ini
    return number_removed, P_infty, seq, tempo

def robustness_failure_node(g,N): #falhas aleatórias

    simulations = N

    #number_removed = removed(g)

    N = g.vcount()
    number_removed = np.zeros(N+1)
    for i in range(g.vcount()):
        number_removed[i] = i / float(N)
    number_removed[N] = 1.0

    P_infty = np.zeros(N+1)

    # Find larger component
    cl = g.components()
    P_infty_baseline = float(max(cl.sizes()))

    for sim in range(simulations):
        
        g_copy = g.copy()
        P_infty[0] += 1.0

        count = 1
        while(g_copy.vcount() > 0):
            
            index = int(random.random() * g_copy.vcount())
            g_copy.delete_vertices(index)

            cl = g_copy.components()
            if(len(cl) > 0):
                P_infty[count] += float(max(cl.sizes())) / P_infty_baseline 
            else:
                P_infty[count] += 0.0

            count = count + 1

    # Compute the average
    P_infty = P_infty / float(simulations)

    return number_removed,P_infty