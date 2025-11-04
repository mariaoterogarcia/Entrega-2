# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 12:58:42 2025

@author: ingeb
"""

# 1. importar

import pulp as lp

# 2. crear problema

problema = lp.LpProblem('Entrega 2', lp.LpMinimize)
# 3. componentes y parámetros
nodos = ['N1', 'N2', 'N3', 'N4']

arcos = {
    ('N1','N2'): {'f': 5, 'c':5},
    ('N1','N4'): {'f': 10, 'c':30},
    ('N2','N3'): {'f':25, 'c':5},
    ('N2','N4'): {'f': 15, 'c':6},
    ('N3','N4'): {'f':20, 'c':5}}

productos = ['p1', 'p2']
origen = {'p1': 'N1', 'p2': 'N1'}
destino = {'p1': 'N3', 'p2': 'N4'}
demanda = {'p1': 1, 'p2': 1}

# 4. variables
M=1000
x = lp.LpVariable.dicts('x',[(i, j, k) for (i, j) in arcos for k in productos],lowBound=0, cat='Continuous')
y = lp.LpVariable.dicts('y', [(i, j) for (i, j) in arcos],lowBound=0, upBound=1, cat='Binary')

# 5. restricciones
for k in productos:
    for n in nodos:
        salida = lp.lpSum(x[(i, j, k)] for (i, j) in arcos if i == n)
        entrada = lp.lpSum(x[(i, j, k)] for (i, j) in arcos if j == n)

        if n == origen[k]:
            problema += (salida - entrada == demanda[k])
        elif n == destino[k]:
            problema += (salida - entrada == -demanda[k])
        else:
            problema += (salida - entrada == 0)

for (i, j) in arcos:
    problema += (lp.lpSum(x[(i, j, k)] for k in productos) <= M * y[(i, j)])
    
# 6. función objetivo
problema += lp.lpSum(arcos[(i, j)]['f'] * y[(i, j)] + arcos[(i, j)]['c'] * lp.lpSum(x[(i, j, k)] for k in productos)for (i, j) in arcos)

# 7. solve + print
problema.solve()
lp.LpStatus[problema.status]


for v in problema.variables():
    print(v.name, "=", v.value())
    
print("Resultado de la función", lp.value(problema.objective))







