import pygame as pg
from vector import Vector


class Pacman:
    def __init__(self, game):
        self.game = game
        self.screen = game.screen
        # self.velocity = vector

        # Pacman moves constantly in a direction without input
        self.direction = 'Right'
        self.moving = False

        # Set Position
        self.x = 13
        self.y = 23
        self.toX = 13
        self.toY = 23

        # Set Image
        self.screen_rect = game.screen.get_rect()
        self.image = pg.image.load('ship.png')
        self.image = pg.transform.scale(self.image, (80, 80))
        self.rect = self.image.get_rect()

        # Set Image Position,
        self.rect.left = game.graph.getX(self.x)
        self.rect.top = game.graph.getY(self.y)

    def __repr__(self):
        r = self.rect
        return 'Pacman({},{}),direction={},moving={}'.format(r.x, r.y, self.direction, self.moving)

    def center(self): self.rect.midbottom = self.screen_rect.midbottom

    def draw(self): self.screen.blit(self.image, self.rect)

    def move(self):
        vect = Vector(0, 0)

        # inputs to move set true, left true as long as Pacman can still move in his set direction
        if not self.moving:
            return

        # Check direction to move, was set by input
        if self.direction == 'up':
            # Check via maze graph, if movement is possible in specified direction

            vect = Vector(0, -1)
        if self.direction == 'down':
            # Check via maze graph, if movement is possible in specified direction

            vect = Vector(0, 1)
        if self.direction == 'left':
            # Check via maze graph, if movement is possible in specified direction

            vect = Vector(-1, 0)
        if self.direction == 'right':
            # Check via maze graph, if movement is possible in specified direction

            vect = Vector(1, 0)

        # Increment Destination
        if self.x == self.toX:
            self.toX += vect.x
        if self.y == self.toY:
            self.toY += vect.y

        # Increment position
        if self.rect.left != self.game.graph.getX(self.toX):
            self.rect.left += vect.x
        elif self.rect.top != self.game.graph.getX(self.toY):
            self.rect.top += vect.y
        else:
            # Reached Destination
            self.x = self.toX
            self.y = self.toY

        # self.game.limit_on_screen(self.rect)

    def update(self):
        self.move()
        self.draw()
