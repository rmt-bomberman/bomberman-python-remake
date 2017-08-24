import socket
from _struct import *
import pickle
import random
from ast import literal_eval
from lib import Bomb

END_OF_MSG = ":***"
START_P1 = (0, 0)
START_P2 = (700, 500)

BOMB_TIME = 3
MAX_BOMB_RANGE = 3

p1_bombs = []  # LIST OF BOMB OBJECTS
p1_bombs_temp = []
p1_bomb_limit = 3
p1_bomb_range = 1

p2_bombs = []  # LIST OF BOMB OBJECTS
p2_bombs_temp = []
p2_bomb_limit = 3
p2_bomb_range = 1

BLOCK_SIZE = 50
FPS = 60

player_connections = []
pos = 1


def socket_create():
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    PORT = 11114
    HOST = socket.gethostbyname(socket.gethostname())

    print(HOST, PORT)
    sock.bind((HOST, PORT))
    sock.listen(5)
    return sock


def start_grid_list():
    grid_x = range(50, 700, 100)
    grid_y = range(50, 500, 100)
    grid = []

    for i in grid_x:
        for j in grid_y:
            grid.append((i, j))

    return grid


def destro_blocks_list():
    limit = 25
    poss_x = list(range(0, 750, 50))
    poss_y = list(range(0, 550, 50))
    start_grid = start_grid_list()
    grid = []

    i = 0
    while i < limit:
        while True:
            rand = (random.choice(poss_x), random.choice(poss_y))
            if rand not in start_grid \
                    and rand not in grid \
                    and rand != (START_P1[0], START_P1[1]) \
                    and rand != (START_P1[0] + BLOCK_SIZE, START_P1[1]) \
                    and rand != (START_P1[0], START_P1[1] + BLOCK_SIZE) \
                    and rand != (START_P2[0], START_P2[1]) \
                    and rand != (START_P2[0] - BLOCK_SIZE, START_P2[1]) \
                    and rand != (START_P2[0], START_P2[1] - BLOCK_SIZE):
                grid.append(rand)
                break
        i += 1
    return grid


def bomb_coords_generator(bombs):
    bomb_coord = []
    for bomb in bombs:
        bomb_coord.append((bomb.x, bomb.y))
    return bomb_coord


def powerups_list(destro_blocks):
    limit = len(destro_blocks)//2
    powerups = []
    i = 0
    while i < limit:
        while True:
            block = random.choice(destro_blocks)
            if block not in powerups:
                powerups.append(block)
                break
        i = i + 1
    return powerups


def connecting(pos, destructable_blocks, sock):
    while pos <= 2:
        while True:
            print("Waiting for connections...")

            connection, client_address = sock.accept()

            if connection:
                player_connections.append(connection)
                val = pack('!i', pos)
                player_connections[pos-1].send(val)
                destro_list = pickle.dumps(destructable_blocks)
                player_connections[pos-1].send(destro_list)

                if pos == 1:
                    pos += 1
                    print('Player 1 connected!')
                    break

                if pos == 2:
                    pos += 1
                    print('Player 2 connected!')
                    break

                break

            else:
                sock.settimeout(5)
                break


def main_loop(powerups_list, p1_bomb_range, p2_bomb_range, pos):
    # Initial variables
    destructable_blocks = destro_blocks_list()
    powerups_list = powerups_list(destructable_blocks)
    powerups_to_draw = []

    # Technically, the main loop starts here
    while True:
        sock = socket_create()
        connecting(pos, destructable_blocks, sock)
        dead = (False, False)

        while True:
            data = ""
            p1_data = ""
            p2_data = ""
            expl_coord = []

            if True in dead:
                break

            if END_OF_MSG not in p1_data:
                while END_OF_MSG not in p1_data:
                    try:
                        data = player_connections[0].recv(16)
                        p1_data += data.decode()
                        if p1_data == '':
                            print('Player 1 disconnected, Player 2 won.')
                            for conn in player_connections:
                                conn.close()
                            sock.close()
                            return
                    except:
                        print('Player 1 disconnected, Player 2 won.')
                        for conn in player_connections:
                            conn.close()
                        sock.close()
                        return

            if END_OF_MSG not in p2_data:
                while END_OF_MSG not in p2_data:
                    try:
                        data = player_connections[1].recv(16)
                        p2_data += data.decode()
                        if p2_data == '':
                            print('Player 2 disconnected, Player 1 won.')
                            for conn in player_connections:
                                conn.close()
                            sock.close()
                            return
                    except:
                        print('Player 2 disconnected, Player 1 won.')
                        for conn in player_connections:
                            conn.close()
                        sock.close()
                        return

            p1_coord = literal_eval(p1_data.split(':')[1])
            p2_coord = literal_eval(p2_data.split(':')[1])

            if p1_coord in powerups_to_draw:
                if p1_bomb_range < MAX_BOMB_RANGE:
                    p1_bomb_range += 1
                    print("p1 range aded", p1_bomb_range)
                powerups_to_draw.remove(p1_coord)

            if p2_coord in powerups_to_draw:
                if p2_bomb_range < MAX_BOMB_RANGE:
                    p2_bomb_range += 1
                    print("p2 range aded", p2_bomb_range)
                powerups_to_draw.remove(p2_coord)

            if "BOMB" in p1_data:
                bomb = literal_eval(p1_data.split(':')[3])

                if len(p1_bombs) >= p1_bomb_limit or (bomb[0], bomb[1]) in p2_bomb_coords:
                    pass
                else:
                    overlap = False
                    for b in p1_bombs:
                        if (b.x == p1_coord[0] and b.y == p1_coord[1]) or \
                                (b.x == p2_coord[0] and b.y == p2_coord[1]):
                            overlap = True
                            break

                    if not overlap:
                        p1_bombs.append(Bomb.Bomb(bomb[0], bomb[1]))

            if "BOMB" in p2_data:
                bomb = literal_eval(p2_data.split(':')[3])

                if len(p2_bombs) >= p2_bomb_limit or (bomb[0], bomb[1]) in p1_bomb_coords:
                    pass
                else:
                    overlap = False
                    for b in p2_bombs:
                        if (b.x == p1_coord[0] and b.y == p1_coord[1]) or \
                                (b.x == p2_coord[0] and b.y == p2_coord[1]):
                            overlap = True
                            break

                    if not overlap:
                        p2_bombs.append(Bomb.Bomb(bomb[0], bomb[1]))

            for b in p1_bombs:
                if b.timer <= BOMB_TIME * FPS:
                    b.tick()
                else:
                    if True in dead:
                        break
                    expl_coord = []
                    dead = b.explode_server(start_grid_list(), destructable_blocks, expl_coord, p1_coord, p2_coord,
                                            p1_bombs, BOMB_TIME, FPS, p1_bomb_range, powerups_list,
                                            powerups_to_draw)

                    p1_bombs.remove(b)

            if True not in dead:
                for b in p2_bombs:
                    if b.timer <= BOMB_TIME * FPS:
                        b.tick()
                    else:
                        dead = b.explode_server(start_grid_list(), destructable_blocks, expl_coord, p1_coord,
                                                p2_coord,
                                                p2_bombs, BOMB_TIME, FPS, p2_bomb_range, powerups_list,
                                                powerups_to_draw)

                        p2_bombs.remove(b)
                    if True in dead:
                        break

            p1_bomb_coords = bomb_coords_generator(p1_bombs)
            p2_bomb_coords = bomb_coords_generator(p2_bombs)
            bomb_coords = p1_bomb_coords + p2_bomb_coords
            to_send_p1 = "P2COORDS:{}:BOMBS:{}:DESTR:{}:EXPL:{}:POWTODRAW:{}:DEAD:{}".format(p2_coord, bomb_coords,
                                                                                             destructable_blocks,
                                                                                             expl_coord,
                                                                                             powerups_to_draw,
                                                                                             (dead[0], dead[1]))\
                         + END_OF_MSG
            to_send_p2 = "P2COORDS:{}:BOMBS:{}:DESTR:{}:EXPL:{}:POWTODRAW:{}:DEAD:{}".format(p1_coord, bomb_coords,
                                                                                             destructable_blocks,
                                                                                             expl_coord,
                                                                                             powerups_to_draw,
                                                                                             (dead[1], dead[0]))\
                         + END_OF_MSG

            player_connections[0].send(to_send_p1.encode())
            player_connections[1].send(to_send_p2.encode())

main_loop(powerups_list, p1_bomb_range, p2_bomb_range, pos)