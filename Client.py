import pygame
import random
from lib import Bomb
import socket
import struct
import pickle
from ast import literal_eval

pygame.init()

DISP_WIDTH = 750
DISP_HEIGHT = 550

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 155, 0)
GRAY = (211, 211, 211)

FONT = pygame.font.SysFont("monospace", 25)

game_display = pygame.display.set_mode((DISP_WIDTH, DISP_HEIGHT))
pygame.display.set_caption('Bomberman')

CLOCK = pygame.time.Clock()
BLOCK_SIZE = 50
FPS = 60

START_X = 0
START_Y = 0
PLAYER_INDEX = None
destructable_blocks = None
END_OF_MSG = ":***"

# Loading assets
p1_img = pygame.image.load("./lib/_img_/stickman.png")
p2_img = pygame.image.load("./lib/_img_/stickman_2.png")
bomb_img = pygame.image.load("./lib/_img_/bomb.png")
boom_img = pygame.image.load("./lib/_img_/boom.png")
powerup_img = pygame.image.load("./lib/_img_/powerup.png")
dest_img = pygame.image.load("./lib/_img_/destructable.png")
concrete_bg = pygame.image.load("./lib/_img_/concrete_bg.png")
you_won = pygame.image.load("./lib/_img_/you_won_bg.png")
you_won_dc = pygame.image.load("./lib/_img_/you_won_dc_bg.png")
you_lost = pygame.image.load("./lib/_img_/you_lost_bg.png")
button_play_again = pygame.image.load("./lib/_img_/button_play_again.png")
button_quit = pygame.image.load("./lib/_img_/button_quit.png")
waiting_0 = pygame.image.load("./lib/_img_/waiting_0.png")
waiting_1 = pygame.image.load("./lib/_img_/waiting_1.png")
waiting_2 = pygame.image.load("./lib/_img_/waiting_2.png")
waiting_3 = pygame.image.load("./lib/_img_/waiting_3.png")
waiting_4 = pygame.image.load("./lib/_img_/waiting_4.png")
waiting_5 = pygame.image.load("./lib/_img_/waiting_5.png")
waiting_gif = [waiting_0, waiting_1, waiting_2, waiting_3, waiting_4, waiting_5]

# --------------------------------------
# ---------- CONNECTION ----------------
# --------------------------------------

def connect_to_server():
    # SOCKET
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    HOST = '192.168.1.102'
    PORT = 11114
    server_address = (HOST, PORT)
    print('Connecting to {}'.format(server_address))

    sock.connect(server_address)
    print("Connected")

    ind = sock.recv(256)
    destr = sock.recv(256)
    PLAYER_INDEX = struct.unpack('!i', ind[:4])[0]
    print("Got player index ", PLAYER_INDEX)
    destructable_blocks = pickle.loads(destr)
    sock.settimeout(0.2)

    if PLAYER_INDEX == 1:
        START_X = 0
        START_Y = 0
        START_X_P2 = 700
        START_Y_P2 = 500
    else:
        START_X = 700
        START_Y = 500
        START_X_P2 = 0
        START_Y_P2 = 0
    return START_X, START_Y, destructable_blocks, START_X_P2, START_Y_P2, sock


# --------------------------------------

def start_grid_list():
    grid_x = range(50, 700, 100)
    grid_y = range(50, 500, 100)
    grid = []

    for i in grid_x:
        for j in grid_y:
            grid.append((i, j))

    return grid


def start_grid_draw(grid):
    for i in grid:
        pygame.draw.rect(game_display, BLACK, [i[0], i[1], BLOCK_SIZE, BLOCK_SIZE])


def destro_blocks_draw(grid):
    for i in grid:
        game_display.blit(dest_img, (i[0], i[1]))


def powerup_draw(powerups):
    for i in powerups:
        game_display.blit(powerup_img, (i[0], i[1]))


def explosion_draw(explosion_coord):
    for coord in explosion_coord:
        pygame.draw.rect(game_display, GREEN, [coord[0], coord[1], BLOCK_SIZE, BLOCK_SIZE])


def text_objects(text, color):
    text_surface = FONT.render(text, True, color)
    return text_surface, text_surface.get_rect()


def message_to_screen(msg, color):
    text_surface, text_rect = text_objects(msg, color)
    text_rect.center = (DISP_WIDTH / 2), (DISP_HEIGHT / 2)
    game_display.blit(text_surface, text_rect)


def game_over_draw():
    game_display.fill(WHITE)
    message_to_screen('GAME OVER!', RED)
    pygame.display.update()


def you_won_draw():
    game_display.fill(WHITE)
    message_to_screen('YOU WON!', RED)
    pygame.display.update()


def game_end_screen(win):
    while True:
        if win is True:
            game_display.blit(you_won, (0, 0))
        if win is False:
            game_display.blit(you_lost, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 550 > mouse_pos[0] > 200:
                    if 392 > mouse_pos[1] > 300:
                        return  # Quits the game


def opponent_left_screen(win, dc=False):
    while True:  # While loop can maybe start just before the for loop
        if win is True:
            game_display.blit(you_won, (0, 0))
        if win is False:
            game_display.blit(you_lost, (0, 0))
        if dc is True:
            game_display.blit(you_won_dc, (0, 0))
        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            elif event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                if 550 > mouse_pos[0] > 200:
                    if 392 > mouse_pos[1] > 300:
                        return  # Quits the game


def game_loop():
    START_X, START_Y, destructable_blocks, START_X_P2, START_Y_P2, sock = connect_to_server()

    game_exit = False

    game_over = False
    you_won = False
    dead = ()

    p1_x = START_X
    p1_y = START_Y

    p2_x = START_X_P2
    p2_y = START_Y_P2
    move_x = 0
    move_y = 0

    grid = start_grid_list()
    power_ups_to_draw = []
    explosions = []

    BOMB = False

    game_end = False

    while not game_exit:

        p1_coord = (p1_x, p1_y)
        to_send = "COORDS:{}".format(p1_coord)

        if BOMB is True:
            to_send += ":BOMB:{}".format(p1_coord) + END_OF_MSG
            BOMB = False
        else:
            to_send += END_OF_MSG

        sock.send(to_send.encode())

        rcv_data = ""
        i = 0
        while END_OF_MSG not in rcv_data:
            try:
                data = sock.recv(16)
                rcv_data += data.decode()
                sock.settimeout(10)
                if rcv_data == '':
                    sock.close()
                    opponent_left_screen(True, True)
                    game_exit = True
                    break
            except:
                game_display.blit(waiting_gif[i % 6], (0, 0))
                pygame.display.update()
                i += 1
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        game_exit = True
                        break
                if game_exit is True:
                    break

        try:
            p2_coord = literal_eval(rcv_data.split(':')[1])
            p2_x = p2_coord[0]
            p2_y = p2_coord[1]
        except:
            pass

        try:
            bomb_coord = literal_eval(rcv_data.split(':')[3])
            destructable_blocks = literal_eval(rcv_data.split(':')[5])
            expl_coord = literal_eval(rcv_data.split(':')[7])
            power_ups_to_draw = literal_eval(rcv_data.split(':')[9])
            dead = literal_eval(rcv_data.split(':')[11])
        except:
            pass

        try:
            if dead[0] is True:
                sock.close()
                game_end_screen(False)
                break
            if dead[1] is True:
                sock.close()
                game_end_screen(True)
                break
        except:
            pass

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_exit = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    move_x = -BLOCK_SIZE
                    move_y = 0

                elif event.key == pygame.K_RIGHT:
                    move_x = BLOCK_SIZE
                    move_y = 0

                elif event.key == pygame.K_UP:
                    move_x = 0
                    move_y = -BLOCK_SIZE

                elif event.key == pygame.K_DOWN:
                    move_x = 0
                    move_y = BLOCK_SIZE

                if event.key == pygame.K_q:
                    BOMB = True

        pos = (p1_x, p1_y)
        try:
            if (0 <= pos[0] + move_x <= DISP_WIDTH - BLOCK_SIZE and 0 <= pos[1] + move_y <= DISP_HEIGHT - BLOCK_SIZE) \
                    and (pos[0] + move_x, pos[1] + move_y) not in grid \
                    and (pos[0] + move_x, pos[1] + move_y) not in destructable_blocks \
                    and (pos[0] + move_x, pos[1] + move_y) not in bomb_coord \
                    and (pos[0] + move_x, pos[1] + move_y) != p2_coord:
                p1_x += move_x
                p1_y += move_y
        except:
            pass

        move_x = 0
        move_y = 0

        game_display.blit(concrete_bg, (0, 0))
        start_grid_draw(grid)
        destro_blocks_draw(destructable_blocks)
        powerup_draw(power_ups_to_draw)

        try:
            for bomb in bomb_coord:
                game_display.blit(bomb_img, (bomb[0], bomb[1]))
            if expl_coord:
                explosion_draw(expl_coord)
        except:
            pass

        game_display.blit(p1_img, (p1_x, p1_y))
        game_display.blit(p2_img, (p2_x, p2_y))
        pygame.display.update()
        CLOCK.tick(FPS)

    pygame.quit()
    quit()


game_loop()
