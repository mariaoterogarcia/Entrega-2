# -*- coding: utf-8 -*-
"""
Created on Tue Nov  4 13:58:43 2025

@author: ingeb
"""

# 1. Importar

import pulp as lp

# 2. crear problema

problema = lp.LpProblem('Entrega 2', lp.LpMinimize)
# 3. componentes y parámetros
nodos = ['N1', 'N2', 'N3', 'N4','N5','N6','N7','N8','N9','N10',
    'N11','N12','N13','N14','N15','N16','N17','N18','N19','N20']

arcos = {
    ('N1','N2'): {'f': 5, 'c':5},
    ('N1','N4'): {'f': 10, 'c':30},
    ('N2','N3'): {'f':25, 'c':5},
    ('N2','N4'): {'f': 15, 'c':6},
    ('N3','N4'): {'f':20, 'c':5},
    ('N4','N5'): {'f': 8, 'c':5},
    ('N5','N6'): {'f': 10, 'c':6},
    ('N6','N7'): {'f': 7, 'c':4},
    ('N7','N8'): {'f': 12, 'c':5},
    ('N8','N9'): {'f': 9, 'c':4},
    ('N9','N10'): {'f': 11, 'c':5},
    ('N10','N11'): {'f': 6, 'c':5},
    ('N11','N12'): {'f': 8, 'c':6},
    ('N12','N13'): {'f': 10, 'c':5},
    ('N13','N14'): {'f': 9, 'c':5},
    ('N14','N15'): {'f': 7, 'c':4},
    ('N15','N16'): {'f': 8, 'c':5},
    ('N16','N17'): {'f': 10, 'c':6},
    ('N17','N18'): {'f': 9, 'c':4},
    ('N18','N19'): {'f': 8, 'c':5},
    ('N19','N20'): {'f': 11, 'c':6},
    ('N5','N10'): {'f': 9, 'c':5},
    ('N10','N15'): {'f': 7, 'c':4},
    ('N15','N20'): {'f': 6, 'c':5},
    ('N2','N6'): {'f': 10, 'c':5},
    ('N3','N7'): {'f': 9, 'c':5},
    ('N6','N11'): {'f': 12, 'c':6},
    ('N8','N13'): {'f': 8, 'c':4},
    ('N11','N16'): {'f': 7, 'c':5},
    ('N13','N18'): {'f': 10, 'c':5},
    ('N14','N19'): {'f': 9, 'c':4}}

productos = ['p1', 'p2','p3','p4','p5','p6','p7','p8','p9','p10']
origen = {'p1': 'N1', 'p2': 'N1', 'p3': 'N2', 'p4': 'N3', 'p5':'N4', 'p5':'N4',
          'p6':'N5', 'p7':'N6','p8': 'N7','p9': 'N8','p10': 'N9'}
destino = {'p1': 'N3', 'p2': 'N4','p3': 'N10','p4': 'N11','p5': 'N12',
           'p6': 'N13','p7': 'N14','p8': 'N15','p9': 'N16','p10': 'N17'}
demanda = {'p1': 1, 'p2': 1,'p3': 1,'p4': 2,'p5': 1,
           'p6': 2,'p7': 1, 'p8': 1,'p9': 2,'p10': 1}

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