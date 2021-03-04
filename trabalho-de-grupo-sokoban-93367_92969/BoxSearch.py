#Nmecs: 92969 e 93367

import copy
import math
from tree_search_box import *
from KeeperSearch import *
from consts import Tiles, TILES
from math import inf

class BoxDomain(SearchDomainBox):
    def __init__(self):
        pass

    async def actions(self, state, all_coords, diamonds, walls, blocked_pos, tiles_divisoras_mapa):
        actlist = []
        
        all_coords = set({d for d in all_coords if d not in state[0]})

        list_boxes = state[0].copy()

        dominio = KeeperDomain(all_coords)
        p = SearchProblem(dominio, state[-1], (-1,-1))
        t = SearchTree(p, 'Greedy')
        await t.search()

        for box in state[0]:
            list_boxes.remove(box)

            pos_box_moveup = (box[0], box[1] - 1)
            tile_keeper_pos = (box[0], box[1] + 1)
            contador = 0
            n_blocked_pos = 0
            keys = ""
            if (tile_keeper_pos in t.all_nodes):
                while 1:
                    if pos_box_moveup in all_coords and pos_box_moveup not in blocked_pos:
                        if not (checkifblocks(pos_box_moveup, diamonds, walls, list_boxes)):
                            if ((pos_box_moveup[0] - 1, pos_box_moveup[1]) in walls or (pos_box_moveup[0] - 1, pos_box_moveup[1]) in blocked_pos) and ((pos_box_moveup[0] + 1, pos_box_moveup[1]) in walls or (pos_box_moveup[0] + 1, pos_box_moveup[1]) in blocked_pos):
                                if (pos_box_moveup[0] - 1, pos_box_moveup[1]) in blocked_pos or (pos_box_moveup[0] + 1, pos_box_moveup[1]) in blocked_pos:
                                    if n_blocked_pos == 0:
                                        n_blocked_pos = 1
                                        if (pos_box_moveup not in diamonds):
                                            pos_box_moveup = (pos_box_moveup[0], pos_box_moveup[1] - 1)
                                            contador += 1
                                        else:
                                            keys = (contador + 1) * 'w'
                                            actlist = actlist + [[box, pos_box_moveup, keys]]
                                            break
                                    else:
                                        keys = (contador) * 'w'
                                        actlist = actlist + [[box, (pos_box_moveup[0], pos_box_moveup[1] + 1), keys]]
                                        break

                                else:
                                    keys = (contador + 1) * 'w'
                                    if (pos_box_moveup not in diamonds):
                                        if pos_box_moveup in tiles_divisoras_mapa:
                                            if (pos_box_moveup[0], pos_box_moveup[1] - 1) in all_coords and (pos_box_moveup[0], pos_box_moveup[1] - 1) not in blocked_pos:
                                                if not (checkifblocks((pos_box_moveup[0], pos_box_moveup[1] - 1), diamonds, walls, list_boxes)):
                                                    if (pos_box_moveup[0], pos_box_moveup[1] - 1) not in diamonds:
                                                        if (pos_box_moveup[0], pos_box_moveup[1] - 2) in all_coords and (pos_box_moveup[0], pos_box_moveup[1] - 2) not in blocked_pos:
                                                            if not (checkifblocks((pos_box_moveup[0], pos_box_moveup[1] - 2), diamonds, walls, list_boxes)):
                                                                pos_box_moveup = (pos_box_moveup[0], pos_box_moveup[1] - 2)
                                                                keys = keys + 'ww'
                                                                actlist = actlist + [[box, pos_box_moveup, keys]]
                                                    else:
                                                        keys = keys + 'w'
                                                        actlist = actlist + [[box, (pos_box_moveup[0], pos_box_moveup[1] - 1), keys]]
                                            break
                                        else:
                                            pos_box_moveup = (pos_box_moveup[0], pos_box_moveup[1] - 1)
                                            contador += 1
                                    else:
                                        actlist = actlist + [[box, pos_box_moveup, keys]]
                                        break
                            else:
                                if (pos_box_moveup[0], pos_box_moveup[1] - 1) in walls or (pos_box_moveup[0] +1, pos_box_moveup[1] - 1) in walls or (pos_box_moveup[0] -1, pos_box_moveup[1] - 1) in walls:
                                    if contador == 0:
                                        keys = (contador + 1) * 'w'
                                        actlist = actlist + [[box, pos_box_moveup, keys]]
                                        break
                                    else:
                                        keys = (contador) * 'w'
                                        actlist = actlist + [[box, (pos_box_moveup[0], pos_box_moveup[1] + 1), keys]]
                                        break
                                else:
                                    keys = (contador + 1) * 'w'
                                    actlist = actlist + [[box, pos_box_moveup, keys]]
                                    break
                        else:
                            if contador != 0:
                                keys = (contador) * 'w'
                                actlist = actlist + [[box, (pos_box_moveup[0], pos_box_moveup[1] + 1), keys]]
                            break
                    else:
                        if contador != 0:
                            keys = (contador) * 'w'
                            actlist = actlist + [[box, (pos_box_moveup[0], pos_box_moveup[1] + 1), keys]]
                        break

            pos_box_movedown = (box[0], box[1] + 1)
            tile_keeper_pos = (box[0], box[1] - 1)
            contador = 0
            n_blocked_pos = 0
            keys = ""
            if (tile_keeper_pos in t.all_nodes):
                while 1:
                    if pos_box_movedown in all_coords and pos_box_movedown not in blocked_pos:
                        if not (checkifblocks(pos_box_movedown, diamonds, walls, list_boxes)):
                            if ((pos_box_movedown[0] - 1, pos_box_movedown[1]) in walls or (pos_box_movedown[0] - 1, pos_box_movedown[1]) in blocked_pos) and ((pos_box_movedown[0] + 1, pos_box_movedown[1]) in walls or (pos_box_movedown[0] + 1, pos_box_movedown[1]) in blocked_pos):
                                if (pos_box_movedown[0] - 1, pos_box_movedown[1]) in blocked_pos or (pos_box_movedown[0] + 1, pos_box_movedown[1]) in blocked_pos:
                                    if n_blocked_pos == 0:
                                        n_blocked_pos = 1
                                        if (pos_box_movedown not in diamonds):
                                            pos_box_movedown = (pos_box_movedown[0], pos_box_movedown[1] + 1)
                                            contador += 1
                                        else:
                                            keys = (contador + 1) * 's'
                                            actlist = actlist + [[box, pos_box_movedown, keys]]
                                            break
                                    else:
                                        keys = (contador) * 's'
                                        actlist = actlist + [
                                            [box, (pos_box_movedown[0], pos_box_movedown[1] - 1), keys]]
                                        break
                                else:
                                    keys = (contador + 1) * 's'
                                    if (pos_box_movedown not in diamonds):
                                        if pos_box_movedown in tiles_divisoras_mapa:
                                            if (pos_box_movedown[0], pos_box_movedown[1] + 1) in all_coords and (pos_box_movedown[0], pos_box_movedown[1] + 1) not in blocked_pos:
                                                if not (checkifblocks((pos_box_movedown[0], pos_box_movedown[1] + 1), diamonds, walls, list_boxes)):
                                                    if (pos_box_movedown[0], pos_box_movedown[1] + 1) not in diamonds:
                                                        if (pos_box_movedown[0], pos_box_movedown[1] + 2) in all_coords and (pos_box_movedown[0], pos_box_movedown[1] + 2) not in blocked_pos:
                                                            if not (checkifblocks((pos_box_movedown[0], pos_box_movedown[1] + 2), diamonds, walls, list_boxes)):
                                                                pos_box_movedown = (pos_box_movedown[0], pos_box_movedown[1] + 2)
                                                                keys = keys + 'ss'
                                                                actlist = actlist + [[box, pos_box_movedown, keys]]
                                                    else:
                                                        keys = keys + 's'
                                                        actlist = actlist + [[box, (pos_box_movedown[0], pos_box_moveup[1] + 1), keys]]
                                            break
                                        else:
                                            pos_box_movedown = (pos_box_movedown[0], pos_box_movedown[1] + 1)
                                            contador += 1
                                    else:
                                        actlist = actlist + [[box, pos_box_movedown, keys]]
                                        break

                            else:
                                if (pos_box_movedown[0], pos_box_movedown[1] + 1) in walls or (pos_box_movedown[0] +1, pos_box_movedown[1] + 1) in walls or (pos_box_movedown[0] -1, pos_box_movedown[1] + 1) in walls:
                                    if contador == 0:
                                        keys = (contador + 1) * 's'
                                        actlist = actlist + [[box, pos_box_movedown, keys]]
                                        break
                                    else:
                                        keys = (contador) * 's'
                                        actlist = actlist + [
                                            [box, (pos_box_movedown[0], pos_box_movedown[1] - 1), keys]]
                                        break
                                else:
                                    keys = (contador + 1) * 's'
                                    actlist = actlist + [[box, pos_box_movedown, keys]]
                                    break
                        else:
                            if contador != 0:
                                keys = (contador) * 's'
                                actlist = actlist + [[box, (pos_box_movedown[0], pos_box_movedown[1] - 1), keys]]
                            break
                    else:
                        if contador != 0:
                            keys = (contador) * 's'
                            actlist = actlist + [[box, (pos_box_movedown[0], pos_box_movedown[1] - 1), keys]]
                        break

            pos_box_moveleft = (box[0] - 1, box[1])
            tile_keeper_pos = (box[0] + 1, box[1])
            contador = 0
            n_blocked_pos = 0
            keys = ""
            if (tile_keeper_pos in t.all_nodes):
                while 1:
                    if pos_box_moveleft in all_coords and pos_box_moveleft not in blocked_pos:
                        if not (checkifblocks(pos_box_moveleft, diamonds, walls, list_boxes)):
                            if ((pos_box_moveleft[0], pos_box_moveleft[1] - 1) in walls or (pos_box_moveleft[0], pos_box_moveleft[1] - 1) in blocked_pos) and ((pos_box_moveleft[0], pos_box_moveleft[1] + 1) in walls or (pos_box_moveleft[0], pos_box_moveleft[1] + 1) in blocked_pos):
                                if (pos_box_moveleft[0], pos_box_moveleft[1] - 1) in blocked_pos or (pos_box_moveleft[0], pos_box_moveleft[1] + 1) in blocked_pos:

                                    if n_blocked_pos == 0:
                                        n_blocked_pos = 1
                                        if (pos_box_moveleft not in diamonds):
                                            pos_box_moveleft = (pos_box_moveleft[0] - 1, pos_box_moveleft[1])
                                            contador += 1
                                        else:
                                            keys = (contador + 1) * 'a'
                                            actlist = actlist + [[box, pos_box_moveleft, keys]]
                                            break
                                    else:
                                        keys = (contador) * 'a'
                                        actlist = actlist + [
                                            [box, (pos_box_moveleft[0] + 1, pos_box_moveleft[1]), keys]]
                                        break

                                else:
                                    keys = (contador + 1) * 'a'
                                    if (pos_box_moveleft not in diamonds):
                                        if pos_box_moveleft in tiles_divisoras_mapa:
                                            if (pos_box_moveleft[0] -1, pos_box_moveleft[1]) in all_coords and (pos_box_moveleft[0]-1, pos_box_moveleft[1]) not in blocked_pos:
                                                if not (checkifblocks((pos_box_moveleft[0]-1, pos_box_moveleft[1]), diamonds, walls, list_boxes)):
                                                    if (pos_box_moveleft[0]-1, pos_box_moveleft[1]) not in diamonds:
                                                        if (pos_box_moveleft[0]-2, pos_box_moveleft[1]) in all_coords and (pos_box_moveleft[0]-2, pos_box_moveleft[1]) not in blocked_pos:
                                                            if not (checkifblocks((pos_box_moveleft[0]-2, pos_box_moveleft[1]), diamonds, walls, list_boxes)):
                                                                pos_box_moveleft = (pos_box_moveleft[0]-2, pos_box_moveleft[1])
                                                                keys = keys + 'aa'
                                                                actlist = actlist + [[box, pos_box_moveleft, keys]]
                                                    else:
                                                        keys = keys + 'a'
                                                        actlist = actlist + [[box, (pos_box_moveleft[0] - 1, pos_box_moveleft[1]), keys]]
                                            break
                                        else:
                                            pos_box_moveleft = (pos_box_moveleft[0] - 1, pos_box_moveleft[1])
                                            contador += 1
                                    else:
                                        actlist = actlist + [[box, pos_box_moveleft, keys]]
                                        break

                            else:
                                if (pos_box_moveleft[0] - 1, pos_box_moveleft[1]) in walls or (pos_box_moveleft[0] - 1, pos_box_moveleft[1] +1) in walls or (pos_box_moveleft[0] - 1, pos_box_moveleft[1] -1) in walls:
                                    if contador == 0:
                                        keys = (contador + 1) * 'a'
                                        actlist = actlist + [[box, pos_box_moveleft, keys]]
                                        break
                                    else:
                                        keys = (contador) * 'a'
                                        actlist = actlist + [
                                            [box, (pos_box_moveleft[0] + 1, pos_box_moveleft[1]), keys]]
                                        break
                                else:
                                    keys = (contador + 1) * 'a'
                                    actlist = actlist + [[box, pos_box_moveleft, keys]]
                                    break
                        else:
                            if contador != 0:
                                keys = (contador) * 'a'
                                actlist = actlist + [[box, (pos_box_moveleft[0] + 1, pos_box_moveleft[1]), keys]]
                            break
                    else:
                        if contador != 0:
                            keys = (contador) * 'a'
                            actlist = actlist + [[box, (pos_box_moveleft[0] + 1, pos_box_moveleft[1]), keys]]
                        break

            pos_box_moveright = (box[0] + 1, box[1])
            tile_keeper_pos = (box[0] - 1, box[1])
            contador = 0
            n_blocked_pos = 0
            keys = ""
            if (tile_keeper_pos in t.all_nodes):
                while 1:
                    if pos_box_moveright in all_coords and pos_box_moveright not in blocked_pos:
                        if not (checkifblocks(pos_box_moveright, diamonds, walls, list_boxes)):
                            if ((pos_box_moveright[0], pos_box_moveright[1] - 1) in walls or (pos_box_moveright[0], pos_box_moveright[1] - 1) in blocked_pos) and ((pos_box_moveright[0], pos_box_moveright[1] + 1) in walls or (pos_box_moveright[0], pos_box_moveright[1] + 1) in blocked_pos):
                                if (pos_box_moveright[0], pos_box_moveright[1] - 1) in blocked_pos or (pos_box_moveright[0], pos_box_moveright[1] + 1) in blocked_pos:
                                    if n_blocked_pos == 0:
                                        n_blocked_pos = 1
                                        if (pos_box_moveright not in diamonds):
                                            pos_box_moveright = (pos_box_moveright[0] + 1, pos_box_moveright[1])
                                            contador += 1
                                        else:
                                            keys = (contador + 1) * 'd'
                                            actlist = actlist + [[box, pos_box_moveright, keys]]
                                            break
                                    else:
                                        keys = (contador) * 'd'
                                        actlist = actlist + [
                                            [box, (pos_box_moveright[0] - 1, pos_box_moveright[1]), keys]]
                                        break
                                else:
                                    keys = (contador + 1) * 'd'
                                    if (pos_box_moveright not in diamonds):
                                        if pos_box_moveright in tiles_divisoras_mapa:
                                            if (pos_box_moveright[0] +1, pos_box_moveright[1]) in all_coords and (pos_box_moveright[0]+1, pos_box_moveright[1]) not in blocked_pos:
                                                if not (checkifblocks((pos_box_moveright[0]+1, pos_box_moveright[1]), diamonds, walls, list_boxes)):
                                                    if (pos_box_moveright[0]+1, pos_box_moveright[1]) not in diamonds:
                                                        if (pos_box_moveright[0]+2, pos_box_moveright[1]) in all_coords and (pos_box_moveright[0]+2, pos_box_moveright[1]) not in blocked_pos:
                                                            if not (checkifblocks((pos_box_moveright[0]+2, pos_box_moveright[1]), diamonds, walls, list_boxes)):
                                                                pos_box_moveright = (pos_box_moveright[0]+2, pos_box_moveright[1])
                                                                keys = keys + 'dd'
                                                                actlist = actlist + [[box, pos_box_moveright, keys]]
                                                    else:
                                                        keys = keys + 'd'
                                                        actlist = actlist + [[box, (pos_box_moveright[0] + 1, pos_box_moveright[1]), keys]]
                                            break
                                        else:
                                            pos_box_moveright = (pos_box_moveright[0] + 1, pos_box_moveright[1])
                                            contador += 1
                                    else:
                                        actlist = actlist + [[box, pos_box_moveright, keys]]
                                        break

                            else:
                                if (pos_box_moveright[0] + 1, pos_box_moveright[1]) in walls or (pos_box_moveright[0] + 1, pos_box_moveright[1] +1) in walls or (pos_box_moveright[0] + 1, pos_box_moveright[1] -1) in walls:
                                    if contador == 0:
                                        keys = (contador + 1) * 'd'
                                        actlist = actlist + [[box, pos_box_moveright, keys]]
                                        break
                                    else:
                                        keys = (contador) * 'd'
                                        actlist = actlist + [
                                            [box, (pos_box_moveright[0] - 1, pos_box_moveright[1]), keys]]
                                        break
                                else:
                                    keys = (contador + 1) * 'd'
                                    actlist = actlist + [[box, pos_box_moveright, keys]]
                                    break
                        else:
                            if contador != 0:
                                keys = (contador) * 'd'
                                actlist = actlist + [[box, (pos_box_moveright[0] - 1, pos_box_moveright[1]), keys]]
                            break
                    else:
                        if contador != 0:
                            keys = (contador) * 'd'
                            actlist = actlist + [[box, (pos_box_moveright[0] - 1, pos_box_moveright[1]), keys]]
                        break

            list_boxes.add(box)
        return actlist

    def result(self,state,action):
        result = [set(), action[0]]
        for box in state[0]:
            if box != action[0]:
                result[0].add(box)
            else:
                result[0].add(action[1])

        return result

    def cost(self, state, action):
        return 5

    def heuristic(self, state, diamonds, all_coords):
        coordenadasBox = [d for d in state[0] if d not in diamonds]
        coordenadasGoal = [d for d in diamonds if d not in state[0]]

        total = 0
        for box in coordenadasBox:
            for goal in coordenadasGoal:
                custo = abs(box[0] - goal[0]) + abs(box[1] - goal[1])
                total = total + custo
        return total


    def satisfies(self, mapa, goal):
        return mapa[0] == goal



def checkifblocks(nova_pos, list_diamond, list_walls, list_boxes):

    if (nova_pos[0],nova_pos[1]-1) in list_walls:
        if (nova_pos[0],nova_pos[1]) not in list_diamond:
            if (nova_pos[0]+1,nova_pos[1]-1) in list_walls and (nova_pos[0]+1,nova_pos[1]) in list_boxes:
                return True
            if (nova_pos[0]-1,nova_pos[1]-1) in list_walls and (nova_pos[0]-1,nova_pos[1]) in list_boxes:
                return True
        else:
            if (nova_pos[0]+1,nova_pos[1]-1) in list_walls and (nova_pos[0]+1,nova_pos[1]) in list_boxes and (nova_pos[0]+1,nova_pos[1]) not in list_diamond:
                return True
            if (nova_pos[0]-1,nova_pos[1]-1) in list_walls and (nova_pos[0]-1,nova_pos[1]) in list_boxes and (nova_pos[0]-1,nova_pos[1]) not in list_diamond:
                return True

    if (nova_pos[0],nova_pos[1]+1) in list_walls:
        if (nova_pos[0],nova_pos[1]) not in list_diamond:
            if (nova_pos[0]+1,nova_pos[1]+1) in list_walls and (nova_pos[0]+1,nova_pos[1]) in list_boxes:
                return True
            if (nova_pos[0]-1,nova_pos[1]+1) in list_walls and (nova_pos[0]-1,nova_pos[1]) in list_boxes:
                return True
        else:
            if (nova_pos[0]+1,nova_pos[1]+1) in list_walls and (nova_pos[0]+1,nova_pos[1]) in list_boxes and (nova_pos[0]+1,nova_pos[1]) not in list_diamond:
                return True
            if (nova_pos[0]-1,nova_pos[1]+1) in list_walls and (nova_pos[0]-1,nova_pos[1]) in list_boxes and (nova_pos[0]-1,nova_pos[1]) not in list_diamond:
                return True

    if (nova_pos[0]-1,nova_pos[1]) in list_walls:
        if (nova_pos[0],nova_pos[1]) not in list_diamond:
            if (nova_pos[0]-1,nova_pos[1]+1) in list_walls and (nova_pos[0],nova_pos[1]+1) in list_boxes:
                return True
            if (nova_pos[0]-1,nova_pos[1]-1) in list_walls and (nova_pos[0],nova_pos[1]-1) in list_boxes:
                return True
        else:
            if (nova_pos[0]-1,nova_pos[1]+1) in list_walls and (nova_pos[0],nova_pos[1]+1) in list_boxes and (nova_pos[0],nova_pos[1]+1) not in list_diamond:
                return True
            if (nova_pos[0]-1,nova_pos[1]-1) in list_walls and (nova_pos[0],nova_pos[1]-1) in list_boxes and (nova_pos[0],nova_pos[1]-1) not in list_diamond:
                return True

    if (nova_pos[0]+1,nova_pos[1]) in list_walls:
        if (nova_pos[0],nova_pos[1]) not in list_diamond:
            if (nova_pos[0]+1,nova_pos[1]+1) in list_walls and (nova_pos[0],nova_pos[1]+1) in list_boxes:
                return True
            if (nova_pos[0]+1,nova_pos[1]-1) in list_walls and (nova_pos[0],nova_pos[1]-1) in list_boxes:
                return True
        else:
            if (nova_pos[0]+1,nova_pos[1]+1) in list_walls and (nova_pos[0],nova_pos[1]+1) in list_boxes and (nova_pos[0],nova_pos[1]+1) not in list_diamond:
                return True
            if (nova_pos[0]+1,nova_pos[1]-1) in list_walls and (nova_pos[0],nova_pos[1]-1) in list_boxes and (nova_pos[0],nova_pos[1]-1) not in list_diamond:
                return True

    return False


