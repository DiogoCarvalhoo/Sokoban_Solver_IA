#Nmecs: 92969 e 93367

import math
from tree_search import *

class KeeperDomain(SearchDomain):
    def __init__(self,casas):
        self.casas = casas
        
    async def actions(self,casaAtual):
        actlist = []
        if (casaAtual[0], casaAtual[1] + 1) in self.casas:
            actlist = actlist + [[casaAtual, (casaAtual[0], casaAtual[1] + 1)]]
        if (casaAtual[0], casaAtual[1] - 1) in self.casas:
            actlist = actlist + [[casaAtual, (casaAtual[0], casaAtual[1] - 1)]]
        if (casaAtual[0] + 1, casaAtual[1]) in self.casas:
            actlist = actlist + [[casaAtual, (casaAtual[0] + 1, casaAtual[1])]]
        if (casaAtual[0] - 1, casaAtual[1]) in self.casas:
            actlist = actlist + [[casaAtual, (casaAtual[0] - 1, casaAtual[1])]]
        return actlist 
        
    def result(self,casaAtual,action):
        return action[1]

    def cost(self, city, action):
        return 0

    def heuristic(self, city, goal):
        heuristica = abs(city[0] - goal[0]) + abs(city[1] - goal[1])
        return heuristica
    
    def satisfies(self, state, goal):
        return goal==state






