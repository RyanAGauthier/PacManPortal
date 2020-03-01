import pygame as pg
from settings import Settings
from pygame.locals import *
from vector import Vector
from pacman import Pacman
import time


class Game:

    def __init__(self):
        pg.init()
        self.settings = Settings()
        self.screen = pg.display.set_mode((self.settings.screen_width, self.settings.screen_height))
        self.finished = False

        self.pacman = Pacman(self)


    def process_events(self):
        key_up_down = [pg.KEYDOWN, pg.KEYUP]
        movement = {K_RIGHT: 'right', K_LEFT: 'left', K_UP: 'up', K_DOWN: 'down'}
        translate = {K_d: K_RIGHT, K_a: K_LEFT, K_w: K_UP, K_s: K_DOWN}
        for event in pg.event.get():
            e_type = event.type
            # if e_type == pg.KEYUP:
            #     self.ship.velocity = Game.SHIP_SPEED * Vector(0, 0)
            if e_type in key_up_down:
                k = event.key
                if k in translate.keys() or k in translate.values():     # movement
                    if k in translate.keys():
                        k = translate[k]
                    self.pacman.direction = movement[k]
                    self.pacman.moving = True
                # elif k == pg.K_SPACE and e_type == pg.KEYDOWN:           # shoot laser
                #     self.ship.fire()
                #     return
            elif e_type == QUIT:                                         # quit
                self.finished = True


    def update(self):
        self.pacman.update()

    def play(self):
        while not self.finished:
            self.process_events()
            self.update()
            pg.display.update()
            pg.time.delay(200)


def main():
    g = Game()
    g.play()


if __name__ == '__main__':
    main()
