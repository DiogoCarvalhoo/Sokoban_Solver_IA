#Nmecs: 92969 e 93367

from abc import ABC, abstractmethod
import asyncio
import copy

from consts import Tiles, TILES
import time
class SearchDomainBox(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    async def actions(self, state, all_coords, diamonds, walls, blocked_pos):
        pass

    # resultado de uma accao num estado, ou seja, o estado seguinte
    @abstractmethod
    def result(self, state, action):
        pass

    # custo de uma accao num estado
    @abstractmethod
    def cost(self, state, action):
        pass

    # custo estimado de chegar de um estado a outro
    @abstractmethod
    def heuristic(self, state):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblemBox:
    def __init__(self, domain, initial, goal,  all_coords, diamonds, walls, blocked_pos, tiles_divisoras_mapa):
        self.domain = domain
        self.initial = initial
        self.goal = goal
        self.all_coords = all_coords
        self.diamonds = diamonds
        self.walls = walls
        self.blocked_pos = blocked_pos
        self.tiles_divisoras_mapa = tiles_divisoras_mapa

    def goal_test(self, state):
        return self.domain.satisfies(state, self.goal)


# Nos de uma arvore de pesquisa
class SearchNodeBox:
    def __init__(self, state, parent, cost, heuristic, action): 
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
        self.action = action

    def in_parent(self, newstate):
        if self.parent == None:
            return False
        if self.parent.state == newstate:
            return True
        return self.parent.in_parent(newstate)

    def __str__(self):
        return "no(" + str(self.state) + "," + str(self.parent) + ")"
    

# Arvores de pesquisa
class SearchTreeBox:
    # construtor
    def __init__(self,problem, strategy='A*'): 
        self.problem = problem
        root = SearchNodeBox(problem.initial, None, 0, 0, None)
        self.open_nodes = [root]
        #self.all_nodes = {}
        #self.all_nodes[hash((tuple(sorted(problem.initial[0])), problem.initial[1]))] = [problem.initial]
        self.all_nodes_hashpositivo = {}
        self.all_nodes_hashnegativo = {}
        roothash = hash((tuple(sorted(problem.initial[0])), problem.initial[1]))
        if roothash > 0:
            self.all_nodes_hashpositivo[roothash] = [problem.initial]
        else:
            self.all_nodes_hashnegativo[roothash] = [problem.initial]
        self.strategy = strategy
        self.length = 0
        self.terminals = 0
        self.non_terminals = 0
        self.plan = []

    
    def get_plan_action(self, node):
        if node.parent == None:
            return []
        actions = self.get_plan_action(node.parent)
        actions += [node.action]
        return actions
    
    # procurar a solucao
    async def search(self):
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                self.terminals = len(self.open_nodes)+1
                self.solution = node
                self.plan = self.get_plan_action(node)
                return
            self.non_terminals += 1
            lnewnodes = []
            resultadoactions = await self.problem.domain.actions(node.state, self.problem.all_coords, self.problem.diamonds, self.problem.walls, self.problem.blocked_pos, self.problem.tiles_divisoras_mapa)
            for a in resultadoactions:
                newstate = self.problem.domain.result(node.state, a)
                var_hash = hash((tuple(sorted(newstate[0])), newstate[1]))
                if var_hash > 0:
                    if var_hash in self.all_nodes_hashpositivo.keys():
                        if newstate not in self.all_nodes_hashpositivo[var_hash]:
                            novaheuristica = self.problem.domain.heuristic(newstate, self.problem.diamonds,self.problem.all_coords)
                            newnode = SearchNodeBox(newstate, node, node.cost + 5, novaheuristica, a)
                            lnewnodes.append(newnode)
                            self.all_nodes_hashpositivo[var_hash].append(newstate)
                    else:
                        self.all_nodes_hashpositivo[var_hash] = [newstate]
                        novaheuristica = self.problem.domain.heuristic(newstate, self.problem.diamonds,self.problem.all_coords)
                        newnode = SearchNodeBox(newstate, node, node.cost + 5, novaheuristica, a)
                        lnewnodes.append(newnode)
                else:
                    if var_hash in self.all_nodes_hashnegativo.keys():
                        if newstate not in self.all_nodes_hashnegativo[var_hash]:
                            novaheuristica = self.problem.domain.heuristic(newstate, self.problem.diamonds,self.problem.all_coords)
                            newnode = SearchNodeBox(newstate, node, node.cost + 5, novaheuristica, a)
                            lnewnodes.append(newnode)
                            self.all_nodes_hashnegativo[var_hash].append(newstate)
                    else:
                        self.all_nodes_hashnegativo[var_hash] = [newstate]
                        novaheuristica = self.problem.domain.heuristic(newstate, self.problem.diamonds,self.problem.all_coords)
                        newnode = SearchNodeBox(newstate, node, node.cost + 5, novaheuristica, a)
                        lnewnodes.append(newnode)
            self.open_nodes.extend(lnewnodes)
            if (self.strategy == "A*"):
                self.open_nodes.sort(key=lambda x: x.cost + x.heuristic)
            else:
                self.open_nodes.sort(key=lambda x: x.heuristic)
            await asyncio.sleep(0)
        return None