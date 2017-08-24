class Bomb:
    def __init__(self, bomb_x, bomb_y):
        self.x = bomb_x
        self.y = bomb_y
        self.timer = 0

    def tick(self):
        self.timer += 1

    def find_bomb(self, coord, bombs):
        for bomb in bombs:
            if bomb.x == coord[0] and bomb.y == coord[1]:
                return bombs.index(bomb)
        return None

    def explode(self, grid_indestruct, grid_destruct, coord, player_coord, bombs, bomb_time, FPS, length, powerups, powerups_to_draw):
        # Koordinate koje se menjaju u range-u od bombe
        up_y = list(range(self.y - 50, self.y - (length+1) * 50, -50))
        down_y = list(range(self.y + 50, self.y + (length+1) * 50, 50))
        left_x = list(range(self.x - 50, self.x - (length+1) * 50, -50))
        right_x = list(range(self.x + 50, self.x + (length+1) * 50, 50))

        died_up = False
        died_down = False
        died_left = False
        died_right = False
        dead = False

        bomb_coord = []
        for bomb in bombs:
            bomb_coord.append((bomb.x, bomb.y))

        if (self.x, self.y) == player_coord:
            dead = True

        else:
#  _____________________________________________________________________________________
#  NEUNISTIV I UNISTIV GRID I BOMBE I COVECULJAK

            # nismo naisli na indestruct
            indestruct = False
            # nismo naisli na destruct
            destruct = False
            # nismo naisli na bombu
            found_bomb = False

            # Popunjavamo koord gore, koje treba da eksplodiraju
            for y in up_y:
                if 0 <= y < 550 \
                        and (self.x, y) not in grid_indestruct and indestruct is False \
                        and (self.x, y) not in grid_destruct and destruct is False \
                        and (self.x, y) not in bomb_coord and found_bomb is False \
                        and (self.x, y) != player_coord and died_up is False:
                    coord.append((self.x, y))

                else:
                    if (self.x, y) in grid_indestruct and indestruct is False:
                        indestruct = True

                    if (self.x, y) in grid_destruct and destruct is False \
                            and indestruct is False and found_bomb is False \
                            and died_up is False:
                        if (self.x, y) in powerups:
                            powerups_to_draw.append((self.x, y))
                        grid_destruct.remove((self.x, y))
                        destruct = True

                    if (self.x, y) in bomb_coord and destruct is False\
                            and indestruct is False and found_bomb is False\
                            and died_up is False:
                        index = self.find_bomb((self.x, y), bombs)
                        bombs[index].timer = bomb_time * FPS
                        found_bomb = True

                    if (self.x, y) == player_coord and destruct is False \
                            and indestruct is False and found_bomb is False \
                            and died_up is False:
                        died_up = True

            indestruct = False
            destruct = False
            found_bomb = False

            # popunjavamo koord dole
            for y in down_y:
                if 0 <= y < 550 \
                        and (self.x, y) not in grid_indestruct and indestruct is False \
                        and (self.x, y) not in grid_destruct and destruct is False \
                        and (self.x, y) not in bomb_coord and found_bomb is False \
                        and (self.x, y) != player_coord and died_down is False:
                    coord.append((self.x, y))

                else:
                    if (self.x, y) in grid_indestruct and indestruct is False:
                        indestruct = True

                    if (self.x, y) in grid_destruct and destruct is False \
                            and indestruct is False and found_bomb is False \
                            and died_down is False:
                        if (self.x, y) in powerups:
                            powerups_to_draw.append((self.x, y))
                        grid_destruct.remove((self.x, y))
                        destruct = True

                    if (self.x, y) in bomb_coord and destruct is False\
                            and indestruct is False and found_bomb is False\
                            and died_down is False:
                        index = self.find_bomb((self.x, y), bombs)
                        bombs[index].timer = bomb_time * FPS
                        found_bomb = True

                    if (self.x, y) == player_coord and destruct is False \
                            and indestruct is False and found_bomb is False \
                            and died_down is False:
                        died_down = True

            indestruct = False
            destruct = False
            found_bomb = False

            # popunjavamo koord levo
            for x in left_x:
                if 0 <= x < 750 \
                        and (x, self.y) not in grid_indestruct and indestruct is False \
                        and (x, self.y) not in grid_destruct and destruct is False \
                        and (x, self.y) not in bomb_coord and found_bomb is False \
                        and (x, self.y) != player_coord and died_left is False:
                    coord.append((x, self.y))

                else:
                    if (x, self.y) in grid_indestruct and indestruct is False:
                        indestruct = True

                    if (x, self.y) in grid_destruct and destruct is False \
                            and indestruct is False and found_bomb is False \
                            and died_left is False:
                        if (x, self.y) in powerups:
                            powerups_to_draw.append((x, self.y))
                        grid_destruct.remove((x, self.y))
                        destruct = True

                    if (x, self.y) in bomb_coord and destruct is False \
                            and indestruct is False and found_bomb is False \
                            and died_left is False:
                        index = self.find_bomb((x, self.y), bombs)
                        bombs[index].timer = bomb_time * FPS
                        found_bomb = True

                    if (x, self.y) == player_coord and destruct is False \
                            and indestruct is False and found_bomb is False \
                            and died_left is False:
                        died_left = True

            indestruct = False
            destruct = False
            found_bomb = False

            # popunjavamo koord desno
            for x in right_x:
                if 0 <= x < 750 \
                        and (x, self.y) not in grid_indestruct and indestruct is False \
                        and (x, self.y) not in grid_destruct and destruct is False \
                        and (x, self.y) not in bomb_coord and found_bomb is False \
                        and (x, self.y) != player_coord and died_left is False:
                    coord.append((x, self.y))
                else:
                    if (x, self.y) in grid_indestruct and indestruct is False:
                        indestruct = True

                    if (x, self.y) in grid_destruct and destruct is False \
                            and indestruct is False and found_bomb is False \
                            and died_right is False:
                        if (x, self.y) in powerups:
                            powerups_to_draw.append((x, self.y))
                        grid_destruct.remove((x, self.y))
                        destruct = True

                    if (x, self.y) in bomb_coord and destruct is False \
                            and indestruct is False and found_bomb is False \
                            and died_right is False:
                        index = self.find_bomb((x, self.y), bombs)
                        bombs[index].timer = bomb_time * FPS
                        found_bomb = True

                    if (x, self.y) == player_coord and destruct is False \
                            and indestruct is False and found_bomb is False \
                            and died_right is False:
                        died_right = True

            dead = died_up or died_down or died_left or died_right

        return dead


    #coord = expl_coords
    #bombs = list of bombs
    #length = bomb range
    def explode_server(self, grid_indestruct, grid_destruct, coord, p1_coords, p2_coords, bombs, bomb_time, FPS, length, powerups, powerups_to_draw):
        # Koordinate koje se menjaju u range-u od bombe
        up_y = list(range(self.y - 50, self.y - (length+1) * 50, -50))
        down_y = list(range(self.y + 50, self.y + (length+1) * 50, 50))
        left_x = list(range(self.x - 50, self.x - (length+1) * 50, -50))
        right_x = list(range(self.x + 50, self.x + (length+1) * 50, 50))

        p1_died_up = False
        p1_died_down = False
        p1_died_left = False
        p1_died_right = False

        p2_died_up = False
        p2_died_down = False
        p2_died_left = False
        p2_died_right = False

        p1_dead = False
        p2_dead = False

        bomb_coord = []
        for bomb in bombs:
            bomb_coord.append((bomb.x, bomb.y))

        #if (self.x, self.y) == p1_coords:
        #    p1_dead = True
        #if (self.x, self.y) == p2_coords:
        #    p2_dead = True

        #else:
#  _____________________________________________________________________________________
#  NEUNISTIV I UNISTIV GRID I BOMBE I COVECULJAK

        # nismo naisli na indestruct
        indestruct = False
        # nismo naisli na destruct
        destruct = False
        # nismo naisli na bombu
        found_bomb = False

        # Popunjavamo koord gore, koje treba da eksplodiraju
        for y in up_y:
            if 0 <= y < 550 \
                    and (self.x, y) not in grid_indestruct and indestruct is False \
                    and (self.x, y) not in grid_destruct and destruct is False \
                    and (self.x, y) not in bomb_coord and found_bomb is False \
                    and (self.x, y) != p1_coords and (self.x, y) != p2_coords \
                    and p1_died_up is False and p2_died_up is False:
                coord.append((self.x, y))

            else:
                if (self.x, y) in grid_indestruct and indestruct is False:
                    indestruct = True

                if (self.x, y) in grid_destruct and destruct is False \
                        and indestruct is False and found_bomb is False \
                        and p1_died_up is False and p2_died_up is False:
                    if (self.x, y) in powerups:
                        powerups_to_draw.append((self.x, y))
                    grid_destruct.remove((self.x, y))
                    destruct = True

                if (self.x, y) in bomb_coord and destruct is False \
                        and indestruct is False and found_bomb is False \
                        and p1_died_up is False and p2_died_up is False:
                    index = self.find_bomb((self.x, y), bombs)
                    bombs[index].timer = bomb_time * FPS
                    found_bomb = True

                if (self.x, y) == p1_coords and destruct is False \
                        and indestruct is False and found_bomb is False \
                        and p1_died_up is False:
                    p1_died_up = True

                if (self.x, y) == p2_coords and destruct is False \
                        and indestruct is False and found_bomb is False \
                        and p2_died_up is False:
                    p2_died_up = True

        indestruct = False
        destruct = False
        found_bomb = False

        # popunjavamo koord dole
        for y in down_y:
            if 0 <= y < 550 \
                    and (self.x, y) not in grid_indestruct and indestruct is False \
                    and (self.x, y) not in grid_destruct and destruct is False \
                    and (self.x, y) not in bomb_coord and found_bomb is False \
                    and (self.x, y) != p1_coords and (self.x, y) != p2_coords \
                    and p1_died_down is False and p2_died_down is False:
                coord.append((self.x, y))

            else:
                if (self.x, y) in grid_indestruct and indestruct is False:
                    indestruct = True

                if (self.x, y) in grid_destruct and destruct is False \
                        and indestruct is False and found_bomb is False \
                        and p1_died_down is False and p2_died_down is False:
                    if (self.x, y) in powerups:
                        powerups_to_draw.append((self.x, y))
                    grid_destruct.remove((self.x, y))
                    destruct = True

                if (self.x, y) in bomb_coord and destruct is False\
                        and indestruct is False and found_bomb is False\
                        and p1_died_down is False and p2_died_down is False:
                    index = self.find_bomb((self.x, y), bombs)
                    bombs[index].timer = bomb_time * FPS
                    found_bomb = True

                if (self.x, y) == p1_coords and destruct is False \
                        and indestruct is False and found_bomb is False \
                        and p1_died_down is False:
                    p1_died_down = True

                if (self.x, y) == p2_coords and destruct is False \
                        and indestruct is False and found_bomb is False \
                        and p2_died_down is False:
                    p2_died_down = True

        indestruct = False
        destruct = False
        found_bomb = False

        # popunjavamo koord levo
        for x in left_x:
            if 0 <= x < 750 \
                    and (x, self.y) not in grid_indestruct and indestruct is False \
                    and (x, self.y) not in grid_destruct and destruct is False \
                    and (x, self.y) not in bomb_coord and found_bomb is False \
                    and (x, self.y) != p1_coords and (x, self.y) != p2_coords \
                    and p1_died_left is False and p2_died_left is False:
                coord.append((x, self.y))

            else:
                if (x, self.y) in grid_indestruct and indestruct is False:
                    indestruct = True

                if (x, self.y) in grid_destruct and destruct is False \
                        and indestruct is False and found_bomb is False \
                        and p1_died_left is False and p2_died_left is False:
                    if (x, self.y) in powerups:
                        powerups_to_draw.append((x, self.y))
                    grid_destruct.remove((x, self.y))
                    destruct = True

                if (x, self.y) in bomb_coord and destruct is False \
                        and indestruct is False and found_bomb is False \
                        and p1_died_left is False and p2_died_left is False:
                    index = self.find_bomb((x, self.y), bombs)
                    bombs[index].timer = bomb_time * FPS
                    found_bomb = True

                if (x, self.y) == p1_coords and destruct is False \
                        and indestruct is False and found_bomb is False \
                        and p1_died_left is False:
                    p1_died_left = True

                if (x, self.y) == p2_coords and destruct is False \
                        and indestruct is False and found_bomb is False \
                        and p2_died_left is False:
                    p2_died_left = True

        indestruct = False
        destruct = False
        found_bomb = False

        # popunjavamo koord desno
        for x in right_x:
            if 0 <= x < 750 \
                    and (x, self.y) not in grid_indestruct and indestruct is False \
                    and (x, self.y) not in grid_destruct and destruct is False \
                    and (x, self.y) not in bomb_coord and found_bomb is False \
                    and (x, self.y) != p1_coords and (x, self.y) != p2_coords \
                    and p1_died_left is False and p2_died_left is False:
                coord.append((x, self.y))
            else:
                if (x, self.y) in grid_indestruct and indestruct is False:
                    indestruct = True

                if (x, self.y) in grid_destruct and destruct is False \
                        and indestruct is False and found_bomb is False \
                        and p1_died_right is False and p2_died_left is False:
                    if (x, self.y) in powerups:
                        powerups_to_draw.append((x, self.y))
                    grid_destruct.remove((x, self.y))
                    destruct = True

                if (x, self.y) in bomb_coord and destruct is False \
                        and indestruct is False and found_bomb is False \
                        and p1_died_right is False and p2_died_left is False:
                    index = self.find_bomb((x, self.y), bombs)
                    bombs[index].timer = bomb_time * FPS
                    found_bomb = True

                if (x, self.y) == p1_coords and destruct is False \
                        and indestruct is False and found_bomb is False \
                        and p1_died_right is False:
                    p1_died_right = True

                if (x, self.y) == p2_coords and destruct is False \
                        and indestruct is False and found_bomb is False \
                        and p2_died_right is False:
                    p2_died_right = True

        p1_dead = p1_died_up or p1_died_down or p1_died_left or p1_died_right
        p2_dead = p2_died_up or p2_died_down or p2_died_left or p2_died_right

        return (p1_dead, p2_dead)