#Nmecs: 92969 e 93367

import time
import asyncio
import getpass
import json
import os
import random

import websockets
import sys
from mapa import Map
from BoxSearch import *
from consts import Tiles, TILES


def check_blocks(nova_pos, list_diamond, list_walls):
    if (nova_pos[0], nova_pos[1] - 1) in list_walls and (nova_pos[0] + 1, nova_pos[1]) in list_walls:
        if nova_pos in list_diamond:
            return False
        return True
    if (nova_pos[0], nova_pos[1] - 1) in list_walls and (nova_pos[0] - 1, nova_pos[1]) in list_walls:
        if nova_pos in list_diamond:
            return False
        return True
    if (nova_pos[0], nova_pos[1] + 1) in list_walls and (nova_pos[0] - 1, nova_pos[1]) in list_walls:
        if nova_pos in list_diamond:
            return False
        return True
    if (nova_pos[0], nova_pos[1] + 1) in list_walls and (nova_pos[0] + 1, nova_pos[1]) in list_walls:
        if nova_pos in list_diamond:
            return False
        return True

    minXCaixa = inf
    maxXCaixa = -1
    minYCaixa = inf
    maxYCaixa = -1

    for element in list_walls:
        if element[0] > maxXCaixa:
            maxXCaixa = element[0]
        if element[1] > maxYCaixa:
            maxYCaixa = element[1]
        if element[0] < minXCaixa:
            minXCaixa = element[0]
        if element[1] < minYCaixa:
            minYCaixa = element[1]

    minXCaixa = minXCaixa + 1
    maxXCaixa = maxXCaixa - 1
    minYCaixa = minYCaixa + 1
    maxYCaixa = maxYCaixa - 1

    if (nova_pos[0] + 1, nova_pos[1]) in list_walls and nova_pos[0] == maxXCaixa:
        block = True
        for element in list_diamond:  # Caixa presa direita
            if nova_pos[0] == element[0]:
                block = False
                break
        if block == True:
            return True

    if (nova_pos[0] - 1, nova_pos[1]) in list_walls and nova_pos[0] == minXCaixa:
        block = True
        for element in list_diamond:  # Caixa presa esquerda
            if nova_pos[0] == element[0]:
                block = False
                break
        if block == True:
            return True

    if (nova_pos[0], nova_pos[1] - 1) in list_walls and nova_pos[1] == minYCaixa:
        block = True
        for element in list_diamond:  # Caixa presa cima
            if nova_pos[1] == element[1]:
                block = False
                break
        if block == True:
            return True

    if (nova_pos[0], nova_pos[1] + 1) in list_walls and nova_pos[1] == maxYCaixa:
        block = True
        for element in list_diamond:  # Caixa presa baixo
            if nova_pos[1] == element[1]:
                block = False
                break
        if block == True:
            return True

    if (nova_pos[0], nova_pos[1] - 1) in list_walls and nova_pos not in list_diamond:
        block1 = False
        block2 = False
        contador = 1
        while not (block1 and block2):
            if not block1:
                if (nova_pos[0] + contador, nova_pos[1]) in list_diamond:
                    block1 = False
                    break
                if (nova_pos[0] + contador, nova_pos[1] - 1) not in list_walls and (
                nova_pos[0] + contador, nova_pos[1]) not in list_walls:
                    block1 = False
                    break
                if (nova_pos[0] + contador, nova_pos[1]) in list_walls:
                    block1 = True
            if not block2:
                if (nova_pos[0] - contador, nova_pos[1]) in list_diamond:
                    block2 = False
                    break
                if (nova_pos[0] - contador, nova_pos[1] - 1) not in list_walls and (
                nova_pos[0] - contador, nova_pos[1]) not in list_walls:
                    block2 = False
                    break
                if (nova_pos[0] - contador, nova_pos[1]) in list_walls:
                    block2 = True
            contador = contador + 1
        if (block1 and block2):
            return True

    if (nova_pos[0], nova_pos[1] + 1) in list_walls and nova_pos not in list_diamond:
        block1 = False
        block2 = False
        contador = 1
        while not (block1 and block2):
            if not block1:
                if (nova_pos[0] + contador, nova_pos[1]) in list_diamond:
                    block1 = False
                    break
                if (nova_pos[0] + contador, nova_pos[1] + 1) not in list_walls and (
                nova_pos[0] + contador, nova_pos[1]) not in list_walls:
                    block1 = False
                    break
                if (nova_pos[0] + contador, nova_pos[1]) in list_walls:
                    block1 = True
            if not block2:
                if (nova_pos[0] - contador, nova_pos[1]) in list_diamond:
                    block2 = False
                    break
                if (nova_pos[0] - contador, nova_pos[1] + 1) not in list_walls and (
                nova_pos[0] - contador, nova_pos[1]) not in list_walls:
                    block2 = False
                    break
                if (nova_pos[0] - contador, nova_pos[1]) in list_walls:
                    block2 = True
            contador = contador + 1
        if (block1 and block2):
            return True

    if (nova_pos[0] - 1, nova_pos[1]) in list_walls and nova_pos not in list_diamond:
        block1 = False
        block2 = False
        contador = 1
        while not (block1 and block2):
            if not block1:
                if (nova_pos[0], nova_pos[1] + contador) in list_diamond:
                    block1 = False
                    break
                if (nova_pos[0] - 1, nova_pos[1] + contador) not in list_walls and (
                nova_pos[0], nova_pos[1] + contador) not in list_walls:
                    block1 = False
                    break
                if (nova_pos[0], nova_pos[1] + contador) in list_walls:
                    block1 = True
            if not block2:
                if (nova_pos[0], nova_pos[1] - contador) in list_diamond:
                    block2 = False
                    break
                if (nova_pos[0] - 1, nova_pos[1] - contador) not in list_walls and (
                nova_pos[0], nova_pos[1] - contador) not in list_walls:
                    block2 = False
                    break
                if (nova_pos[0], nova_pos[1] - contador) in list_walls:
                    block2 = True
            contador = contador + 1
        if (block1 and block2):
            return True

    if (nova_pos[0] + 1, nova_pos[1]) in list_walls and nova_pos not in list_diamond:
        block1 = False
        block2 = False
        contador = 1
        while not (block1 and block2):
            if not block1:
                if (nova_pos[0], nova_pos[1] + contador) in list_diamond:
                    block1 = False
                    break
                if (nova_pos[0] + 1, nova_pos[1] + contador) not in list_walls and (
                nova_pos[0], nova_pos[1] + contador) not in list_walls:
                    block1 = False
                    break
                if (nova_pos[0], nova_pos[1] + contador) in list_walls:
                    block1 = True
            if not block2:
                if (nova_pos[0], nova_pos[1] - contador) in list_diamond:
                    block2 = False
                    break
                if (nova_pos[0] + 1, nova_pos[1] - contador) not in list_walls and (
                nova_pos[0], nova_pos[1] - contador) not in list_walls:
                    block2 = False
                    break
                if (nova_pos[0], nova_pos[1] - contador) in list_walls:
                    block2 = True
            contador = contador + 1
        if (block1 and block2):
            return True
    return False


async def solver(puzzle, solution):
    while True:
        game_properties = await puzzle.get()
        mapa = Map(game_properties["map"])
        
        inittime = time.time()

        dominio = BoxDomain()
    
        initial = [set(mapa.boxes), mapa.keeper]
        walls = set(mapa.filter_tiles([Tiles.WALL]))
        diamonds = set(mapa.filter_tiles([Tiles.GOAL, Tiles.BOX_ON_GOAL, Tiles.MAN_ON_GOAL]))
        all_coords = set(mapa.filter_tiles([Tiles.BOX, Tiles.BOX_ON_GOAL, Tiles.FLOOR, Tiles.GOAL, Tiles.MAN_ON_GOAL, Tiles.MAN]))
        goal = diamonds

        dominio2 = KeeperDomain(all_coords)
        p = SearchProblem(dominio2, mapa.keeper, (-1, -1))
        t = SearchTree(p, 'Greedy')
        await t.search()
        all_coords = set(t.all_nodes)

        blocked_pos = set({})
        for coord in all_coords:
            if check_blocks(coord, diamonds, walls):
                blocked_pos.add(coord)
        
        tiles_divisoras_mapa = set({})
        contador = 0
        possivel_tile = None
        for i in range(0,mapa.size[0]):
            for coord in all_coords:
                if coord[0] == i:
                    contador += 1
                    possivel_tile = coord 
                if contador > 1:
                    possivel_tile = None
                    break
            if possivel_tile != None:
                tiles_divisoras_mapa.add(possivel_tile)
            contador = 0
        contador = 0
        possivel_tile = None
        for i in range(0,mapa.size[1]):
            for coord in all_coords:
                if coord[1] == i:
                    contador += 1
                    possivel_tile = coord 
                if contador > 1:
                    possivel_tile = None
                    break
            if possivel_tile != None:
                tiles_divisoras_mapa.add(possivel_tile)
            contador = 0
                

        p = SearchProblemBox(dominio, initial, goal, all_coords, diamonds, walls, blocked_pos, tiles_divisoras_mapa)
        total = 0
        for box in initial[0]:
            if box not in goal:
                for goal in diamonds:
                    if goal not in initial[0]:
                        custo = abs(box[0] - goal[0]) + abs(box[1] - goal[1])
                        total = total + custo

        if total*len(initial[0])< 500:
            t = SearchTreeBox(p, strategy="A*")
            await t.search()
        else:
            t = SearchTreeBox(p, strategy="Greedy")
            await t.search()
        

        
        no = t.solution
        dicionario_nos = {}
        contador = 0
        while no != None:
            dicionario_nos[str(contador)] = no
            no = no.parent
            contador = contador+1

        keys = ""
        pos_keeper = mapa.keeper
        contador2 = contador-1
        for action in t.plan:
            caixaX = action[0][0]
            caixaY = action[0][1]

            if (action[2][0] == 'w'):
                keeper_empurrar_pos = (caixaX, caixaY + 1)
            elif (action[2][0] == 's'):
                keeper_empurrar_pos = (caixaX, caixaY - 1)
            elif (action[2][0] == 'a'):
                keeper_empurrar_pos = (caixaX + 1, caixaY)
            elif (action[2][0] == 'd'):
                keeper_empurrar_pos = (caixaX - 1, caixaY)

            coords = set({d for d in all_coords if d not in dicionario_nos[str(contador2)].state[0]})
            dominio = KeeperDomain(coords)
            p = SearchProblem(dominio, pos_keeper, keeper_empurrar_pos)
            t = SearchTree(p, 'A*')
            await t.search()

            for move in t.plan:
                firstCoordX = move[0][0]
                firstCoordY = move[0][1]
                secondCoordX = move[1][0]
                secondCoordY = move[1][1]
                if (firstCoordX == secondCoordX + 1 and firstCoordY == secondCoordY):
                    keys = keys + "a"
                elif (firstCoordX == secondCoordX - 1 and firstCoordY == secondCoordY):
                    keys = keys + "d"
                elif (firstCoordX == secondCoordX and firstCoordY == secondCoordY + 1):
                    keys = keys + "w"
                elif (firstCoordX == secondCoordX and firstCoordY == secondCoordY - 1):
                    keys = keys + "s"

            keys = keys + action[2]
            if (action[2][0] == 'w'):
                pos_keeper = (action[1][0], action[1][1] + 1)
            elif (action[2][0] == 's'):
                pos_keeper = (action[1][0], action[1][1] - 1)
            elif (action[2][0] == 'a'):
                pos_keeper = (action[1][0] + 1, action[1][1])
            elif (action[2][0] == 'd'):
                pos_keeper = (action[1][0] - 1, action[1][1])
            contador2 = contador2 - 1

        await solution.put(keys)
        

async def agent_loop(puzzle, solution, server_address="localhost:8000", agent_name="student"):
    async with websockets.connect(f"ws://{server_address}/player") as websocket:

        # Receive information about static game properties
        await websocket.send(json.dumps({"cmd": "join", "name": agent_name}))

        while True:
            try:
                update = json.loads(
                    await websocket.recv()
                )  # receive game update, this must be called timely or your game will get out of sync with the server

                if "map" in update:
                    # we got a new level
                    game_properties = update
                    keys = ""
                    await puzzle.put(game_properties)

                if not solution.empty():
                    keys = await solution.get()

                key = ""
                if len(keys):  # we got a solution!
                    key = keys[0]
                    keys = keys[1:]

                await websocket.send(
                    json.dumps({"cmd": "key", "key": key})
                )

            except websockets.exceptions.ConnectionClosedOK:
                print("Server has cleanly disconnected us")
                sys.exit(0)
                return

# DO NOT CHANGE THE LINES BELLOW
# You can change the default values using the command line, example:
# $ NAME='arrumador' python3 client.py
loop = asyncio.get_event_loop()
SERVER = os.environ.get("SERVER", "localhost")
PORT = os.environ.get("PORT", "8000")
NAME = os.environ.get("NAME", getpass.getuser())

puzzle = asyncio.Queue(loop=loop)
solution = asyncio.Queue(loop=loop)

net_task = loop.create_task(agent_loop(puzzle, solution, f"{SERVER}:{PORT}", NAME))
solver_task = loop.create_task(solver(puzzle, solution))

loop.run_until_complete(asyncio.gather(net_task, solver_task))
loop.close()


