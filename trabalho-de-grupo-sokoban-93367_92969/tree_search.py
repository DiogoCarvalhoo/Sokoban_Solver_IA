#Nmecs: 92969 e 93367

from abc import ABC, abstractmethod
import asyncio

class SearchDomain(ABC):

    # construtor
    @abstractmethod
    def __init__(self):
        pass

    # lista de accoes possiveis num estado
    @abstractmethod
    async def actions(self, state):
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
    def heuristic(self, state, goal):
        pass

    # test if the given "goal" is satisfied in "state"
    @abstractmethod
    def satisfies(self, state, goal):
        pass


# Problemas concretos a resolver
# dentro de um determinado dominio
class SearchProblem:
    def __init__(self, domain, initial, goal):
        self.domain = domain
        self.initial = initial
        self.goal = goal


    def goal_test(self, state):
        return self.domain.satisfies(state, self.goal)


# Nos de uma arvore de pesquisa
class SearchNode:
    def __init__(self, state, parent, heuristic, action):
        self.state = state
        self.parent = parent
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
class SearchTree:
    # construtor
    def __init__(self, problem, strategy='Greedy'):
        self.problem = problem
        heuristicaroot = self.problem.domain.heuristic(self.problem.initial, self.problem.goal)
        root = SearchNode(problem.initial, None, heuristicaroot, None)
        self.open_nodes = [root]
        #self.all_nodes = [problem.initial]
        self.all_nodes = set([problem.initial])
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
        await asyncio.sleep(0)
        while self.open_nodes != []:
            node = self.open_nodes.pop(0)
            if self.problem.goal_test(node.state):
                self.terminals = len(self.open_nodes)+1
                self.solution = node
                self.plan = self.get_plan_action(node)
                return
            self.non_terminals += 1
            lnewnodes = []
            resultadoactions = await self.problem.domain.actions(node.state)
            for a in resultadoactions:
                newstate = self.problem.domain.result(node.state, a)
                if newstate not in self.all_nodes:
                    novaheuristica = self.problem.domain.heuristic(newstate, self.problem.goal)
                    newnode = SearchNode(newstate, node, novaheuristica, a)
                    lnewnodes.append(newnode)
                    self.all_nodes.add(newstate)
            self.open_nodes.extend(lnewnodes)
            self.open_nodes.sort(key=lambda x: x.heuristic)
        return None

        


    
