import pygame as pg
import sys
from vector import Vector
from random import randrange

NODESIZE = 8


class Ghost(pg.sprite.Sprite):
    # This is the class that represents the ghosts, there will be four individual instances in total
    # The class inherits from sprite so that we can later use sprite.groupcollide() between pacman and each ghost
    # Each ghost can draw and update itself, currently it just needs to implement the state parameter, which is intended
    # to tell the ghost whether it is fleeing, respawning, just eyeballs, etc
    def __init__(self, surface, images, rect, direction, state, name=None, selfnode=None, allnodes=None):
        pg.sprite.Sprite.__init__(self)
        self.surface = surface
        self.name = name
        self.images = images
        self.currentframe = 0
        self.duration = 60
        self.shopping = 0
        self.velocity = Vector()
        self.speed = 5
        self.image = images[self.currentframe]
        self.rect = rect
        self.direction = direction
        self.selfnode = selfnode
        self.allnodes = allnodes
        self.targetnode = None
        self.state = state
        self.framecount = 11  # This dictates how many game frames should pass between different images
        self.frameclock = self.framecount

    def changedirection(self, newdirection):
        self.direction = newdirection
        if newdirection == "up":
            self.velocity = self.speed * (0, -1)
            self.currentframe = 4
            self.image = self.images[self.currentframe]
        elif newdirection == "down":
            self.velocity = self.speed * (0, 1)
            self.currentframe = 6
            self.image = self.images[self.currentframe]
        elif newdirection == "left":
            self.velocity = self.speed * (-1, 0)
            self.currentframe = 2
            self.image = self.images[self.currentframe]
        elif newdirection == "right":
            self.velocity = self.speed * (1, 0)
            self.currentframe = 0
            self.image = self.images[self.currentframe]

    def changestate(self, newstate):
        self.state = newstate
        if self.state == "vulnerable":
            pass
        elif self.state == "dead":
            pass
        elif self.state == "living":
            pass
        elif self.state == "shopping":
            pass
        elif self.state == "chasing":
            pass

    def draw(self):
        self.surface.blit(self.image, self.rect)

    def get_target(self):
        bestnode = self.targetnode
        # CHASING
        if self.state == 'chasing':
            # If we are at our target node, get the next one
            if (self.allnodes[self.selfnode[0]][self.selfnode[1]] == self.targetnode) or (self.targetnode is None):
                # In all edgenodes/neighbors
                for node in self.allnodes[self.selfnode[0]][self.selfnode[1]].edgeto:
                    # Get the node with the smallest distance
                    if (bestnode is None) or (bestnode == self.targetnode):
                        bestnode = node
                    else:
                        if (node.distfrompac < bestnode.distfrompac) and node.traversable:
                            bestnode = node

        # RUNNING or VULNERABLE
        if self.state == 'running' or self.state == 'vulnerable':
            # If we are at our target node, get the next one
            if (self.allnodes[self.selfnode[0]][self.selfnode[1]] == self.targetnode) or (
                    self.targetnode is None):
                # In all edgenodes/neighbors
                for node in self.allnodes[self.selfnode[0]][self.selfnode[1]].edgeto:
                    # Get the node with the largest distance
                    if (bestnode is None) or (bestnode == self.targetnode):
                        bestnode = node
                    else:
                        if (node.distfrompac > bestnode.distfrompac) and node.traversable:
                            bestnode = node

        # SHOPPING
        if self.state == 'shopping':
            # Neighbor nodes
            up = down = left = right = None

            # In all edgenodes/neighbors
            for node in self.allnodes[self.selfnode[0]][self.selfnode[1]].edgeto:
                # Determine direction of neighbor nodes
                if node == self.allnodes[self.selfnode[0] - 1][self.selfnode[1]]:
                    up = node
                if node == self.allnodes[self.selfnode[0] + 1][self.selfnode[1]]:
                    down = node
                if node == self.allnodes[self.selfnode[0]][self.selfnode[1] + 1]:
                    right = node
                if node == self.allnodes[self.selfnode[0]][self.selfnode[1] - 1]:
                    left = node

            # If we are at our target node, get the next one
            if (self.allnodes[self.selfnode[0]][self.selfnode[1]] == self.targetnode) or (
                    self.targetnode is None):
                shoptime = 8
                # Depending on direction
                if self.direction == 'up':
                    # If cant continue in the direction, or shopping time is up, try to turn
                    if (up is None) or (self.shopping == 0):
                        # if pinky turn opposite to other ghosts
                        if self.name == 'pinky':
                            if left is not None:
                                bestnode = left
                            elif up is not None:
                                bestnode = up
                            else:
                                bestnode = right
                        else:
                            if right is not None:
                                bestnode = right
                            elif up is not None:
                                bestnode = up
                            else:
                                bestnode = left
                        self.shopping = randrange(shoptime)
                    # Unable to turn and can continue
                    else:
                        bestnode = up
                        self.shopping -= 1
                # Direction
                elif self.direction == 'down':
                    # If cant continue in the direction, or shopping time is up, try to turn
                    if (down is None) or (self.shopping == 0):
                        # if pinky turn opposite to other ghosts
                        if self.name == 'pinky':
                            if right is not None:
                                bestnode = right
                            elif down is not None:
                                bestnode = down
                            else:
                                bestnode = left
                        else:
                            if left is not None:
                                bestnode = left
                            elif down is not None:
                                bestnode = down
                            else:
                                bestnode = right
                        self.shopping = randrange(shoptime)
                    # Unable to turn and can continue
                    else:
                        bestnode = down
                        self.shopping -= 1
                # Direction
                elif self.direction == 'right':
                    # If cant continue in the direction, or shopping time is up, try to turn
                    if (right is None) or (self.shopping == 0):
                        # if pinky turn opposite to other ghosts
                        if self.name == 'pinky':
                            if up is not None:
                                bestnode = up
                            elif right is not None:
                                bestnode = right
                            else:
                                bestnode = down
                        else:
                            if down is not None:
                                bestnode = down
                            elif right is not None:
                                bestnode = right
                            else:
                                bestnode = up
                        self.shopping = randrange(shoptime)
                    # Unable to turn and can continue
                    else:
                        bestnode = right
                        self.shopping -= 1
                # Direction
                elif self.direction == 'left':
                    # If cant continue in the direction, or shopping time is up, try to turn
                    if (left is None) or (self.shopping == 0):
                        # if pinky turn opposite to other ghosts
                        if self.name == 'pinky':
                            if down is not None:
                                bestnode = down
                            elif left is not None:
                                bestnode = left
                            else:
                                bestnode = up
                        else:
                            if up is not None:
                                bestnode = up
                            elif left is not None:
                                bestnode = left
                            else:
                                bestnode = down
                        self.shopping = randrange(shoptime)
                    # Unable to turn and can continue
                    else:
                        bestnode = left
                        self.shopping -= 1
            else:
                # Haven't reached target node
                return bestnode

        return bestnode

    def move(self):
        # fix centering
        if self.rect.centerx % 2 != 0:
            self.rect.centerx += 1
        if self.rect.centery % 2 != 0:
            self.rect.centery += 1

        if self.targetnode == self.allnodes[self.selfnode[0] - 1][self.selfnode[1]]:
            self.direction = 'up'
            if self.targetnode.traversable and self.rect.centerx == self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx:
                self.velocity = Vector(0, -2)
        elif self.targetnode == self.allnodes[self.selfnode[0] + 1][self.selfnode[1]]:
            self.direction = 'down'
            if self.targetnode.traversable and self.rect.centerx == self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx:
                self.velocity = Vector(0, 2)
        elif self.targetnode == self.allnodes[self.selfnode[0]][self.selfnode[1] + 1]:
            self.direction = 'right'
            if self.targetnode.traversable and self.rect.centery == self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery:
                self.velocity = Vector(2, 0)
        elif self.targetnode == self.allnodes[self.selfnode[0]][self.selfnode[1] - 1]:
            self.direction = 'left'
            if self.targetnode.traversable and self.rect.centery == self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery:
                self.velocity = Vector(-2, 0)

        # Checking centers to see if self node should be changed?
        if self.velocity == Vector(-2, 0):
            # self.targetnode = self.allnodes[self.selfnode[0]][self.selfnode[1] - 1]
            if self.targetnode.traversable or self.rect.centerx > self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx:
                self.rect.centerx += self.velocity.x
                if self.rect.centerx < self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx - 4:
                    self.selfnode = (self.selfnode[0], self.selfnode[1] - 1)
        elif self.velocity == Vector(2, 0):
            # self.targetnode = self.allnodes[self.selfnode[0]][self.selfnode[1] + 1]
            if self.targetnode.traversable or self.rect.centerx < self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx:
                self.rect.centerx += self.velocity.x
                if self.rect.centerx > self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx + 4:
                    self.selfnode = (self.selfnode[0], self.selfnode[1] + 1)
        elif self.velocity == Vector(0, 2):
            # self.targetnode = self.allnodes[self.selfnode[0]+1][self.selfnode[1]]
            if self.targetnode.traversable or self.rect.centery < self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery:
                self.rect.centery += self.velocity.y
                if self.rect.centery > self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery + 4:
                    self.selfnode = (self.selfnode[0] + 1, self.selfnode[1])
        elif self.velocity == Vector(0, -2):
            # self.targetnode = self.allnodes[self.selfnode[0] - 1][self.selfnode[1]]
            if self.targetnode.traversable or self.rect.centery > self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery:
                self.rect.centery += self.velocity.y
                if self.rect.centery < self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery - 4:
                    self.selfnode = (self.selfnode[0] - 1, self.selfnode[1])

        # if self.name == 'blinky':
        #     print("I'm at:")
        #     print(self.selfnode)
        #     print("I'm going to:")
        #     print(self.targetnode)
        #     print('with center: {}'.format(self.targetnode.rect.center))
        #     print("My center is at: {}".format(self.rect.center))

    def update(self):

        if self.name == 'blinky':
            # Blinky is always chasing
            # self.changestate('chasing')
            self.changestate('shopping')

        self.targetnode = self.get_target()

        self.move()
        self.draw()

        # This is the portion of the object that handles the animation, swapping between 3 and 4 legs at a rate decided
        # by self.framecount
        if self.state == "dead":
            if self.direction == "right":
                self.currentframe = 12
            elif self.direction == "left":
                self.currentframe = 13
            elif self.direction == "up":
                self.currentframe = 14
            elif self.direction == "down":
                self.currentframe = 15
        if self.state == "vulnerable":
            if self.duration > 15:
                self.currentframe = 8
                self.duration -= 1
            elif self.duration > 0:
                self.currentframe = 10
                self.duration -= 1
            else:
                self.duration = 60
                self.state = "alive"
                if self.direction == "up":
                    self.currentframe = 4
                elif self.direction == "left":
                    self.currentframe = 2
                elif self.direction == "right":
                    self.currentframe = 0
                elif self.direction == "down":
                    self.currentframe = 6
        if self.frameclock == 1:
            if self.state is not "dead":
                if self.currentframe % 2 == 0:
                    self.currentframe += 1
                else:
                    self.currentframe -= 1
                self.frameclock = self.framecount
        else:
            self.frameclock -= 1
        self.image = self.images[self.currentframe]
        # self.rect.left += self.velocity.x
        # self.rect.top += self.velocity.y
        # print("displaying frame {}".format(self.currentframe))


# class DumbGhost(Ghost):
#     def __init__(self, surface, images, rect, direction, state):
#         super().__init__(surface=surface, images=images, rect=rect, direction=direction, state=state)
#
#     def draw(self):
#         self.surface.blit(self.image, self.rect)
#
#     def update(self):
#         # This is the portion of the object that handles the animation, swapping between 3 and 4 legs at a rate decided
#         # by self.framecount
#         if self.direction == "left":
#             self.rect.left += -5
#         elif self.direction == "right":
#             self.rect.left += 5
#         if self.frameclock == 1:
#             if self.currentframe % 2 == 0:
#                 self.currentframe += 1
#                 self.image = self.images[self.currentframe]
#             else:
#                 self.currentframe -= 1
#                 self.image = self.images[self.currentframe]
#             self.frameclock = self.framecount
#         else:
#             self.frameclock -= 1
#         # print("displaying frame {}".format(self.currentframe))

class Pacman(pg.sprite.Sprite):
    def __init__(self, surface, images, velocity, direction, rect, selfnode, allnodes):
        pg.sprite.Sprite.__init__(self),
        self.surface = surface
        self.velocity = velocity
        self.direction = direction
        self.images = images
        self.currentframe = 0
        self.framecount = 5
        self.selfnode = selfnode
        self.allnodes = allnodes
        self.targetnode = self.allnodes[self.selfnode[0]][self.selfnode[1]]
        self.frameclock = self.framecount
        if self.velocity == Vector(-4, 0):
            self.currentframe = 2
        elif self.velocity == Vector(4, 0):
            self.currentframe = 0
        elif self.velocity == Vector(0, 4):
            self.currentframe = 6
        elif self.velocity == Vector(0, -4):
            self.currentframe = 4
        self.image = self.images[self.currentframe]
        self.rect = rect
        setdistancefrompacman(pacman=self)

    def move(self):
        if self.direction == "up":
            self.targetnode = self.allnodes[self.selfnode[0] - 1][self.selfnode[1]]
            if self.targetnode.traversable and self.rect.centerx == self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx:
                self.velocity = Vector(0, -4)
        elif self.direction == "down":
            self.targetnode = self.allnodes[self.selfnode[0] + 1][self.selfnode[1]]
            if self.targetnode.traversable and self.rect.centerx == self.allnodes[self.selfnode[0]][ self.selfnode[1]].rect.centerx:
                self.velocity = Vector(0, 4)
        elif self.direction == "right":
            self.targetnode = self.allnodes[self.selfnode[0]][self.selfnode[1] + 1]
            if self.targetnode.traversable and self.rect.centery == self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery:
                self.velocity = Vector(4, 0)
        elif self.direction == "left":
            self.targetnode = self.allnodes[self.selfnode[0]][self.selfnode[1] - 1]
            if self.targetnode.traversable and self.rect.centery == self.allnodes[self.selfnode[0]][  self.selfnode[1]].rect.centery:
                self.velocity = Vector(-4, 0)

        # Checking centers to see if self node should be changed?
        if self.velocity == Vector(-4, 0):
            self.targetnode = self.allnodes[self.selfnode[0]][self.selfnode[1] - 1]
            if self.targetnode.traversable or self.rect.centerx > self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx:
                self.rect.centerx += self.velocity.x
                if self.rect.centerx < self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx - 4:
                    self.selfnode = (self.selfnode[0], self.selfnode[1] - 1)
                    setdistancefrompacman(pacman=self)
        elif self.velocity == Vector(4, 0):
            self.targetnode = self.allnodes[self.selfnode[0]][self.selfnode[1] + 1]
            if self.targetnode.traversable or self.rect.centerx < self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx:
                self.rect.centerx += self.velocity.x
                if self.rect.centerx > self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx + 4:
                    self.selfnode = (self.selfnode[0], self.selfnode[1] + 1)
                    setdistancefrompacman(pacman=self)
        elif self.velocity == Vector(0, 4):
            self.targetnode = self.allnodes[self.selfnode[0]+1][self.selfnode[1]]
            if self.targetnode.traversable or self.rect.centery < self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery:
                self.rect.centery += self.velocity.y
                if self.rect.centery > self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery + 4:
                    self.selfnode = (self.selfnode[0] + 1, self.selfnode[1])
                    setdistancefrompacman(pacman=self)
        elif self.velocity == Vector(0, -4):
            self.targetnode = self.allnodes[self.selfnode[0] - 1][self.selfnode[1]]
            if self.targetnode.traversable or self.rect.centery > self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery:
                self.rect.centery += self.velocity.y
                if self.rect.centery < self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery - 4:
                    self.selfnode = (self.selfnode[0] - 1, self.selfnode[1])
                    setdistancefrompacman(pacman=self)
        # print("I'm at:")
        # print(self.selfnode)
        # print("I'm going to:")
        # print(self.targetnode)
        # print("My center is at: {}".format(self.rect.center))

    def update(self):
        self.move()
        if self.velocity == Vector(4, 0) and self.currentframe != 1:
            self.currentframe = 0
        elif self.velocity == Vector(-4, 0) and self.currentframe != 3:
            self.currentframe = 2
        elif self.velocity == Vector(0, -4) and self.currentframe != 5:
            self.currentframe = 4
        elif self.velocity == Vector(0, 4) and self.currentframe != 7:
            self.currentframe = 6
        if self.frameclock == 1:
            if self.currentframe % 2 == 0:
                self.currentframe += 1
            else:
                self.currentframe -= 1
            self.image = self.images[self.currentframe]
            self.frameclock = self.framecount
        else:
            self.frameclock -= 1
        #print("displaying frame {}".format(self.currentframe))

    def draw(self):
        self.surface.blit(self.image, self.rect)


class DumbPacman(Pacman):
    def __init__(self, surface, images, velocity, direction, rect, selfnode, allnodes):
        super().__init__(surface=surface, images=images, velocity=velocity, direction=direction,
                         rect=rect, selfnode=selfnode, allnodes=allnodes)

    def move(self):
        if self.velocity == Vector(0, -4) or self.velocity == Vector(0, 4):
            self.rect.top += self.velocity.y
        elif self.velocity == Vector(4, 0) or self.velocity == Vector(-4, 0):
            self.rect.left += self.velocity.x

    # def draw(self):
    #     self.surface.fill((0, 0, 0))
    #     self.surface.blit(self.image, self.rect)


class staticMember(pg.sprite.Sprite):
    def __init__(self, images, rect):
        super().__init__(self)
        self.images = images
        self.image = images[0]
        self.rect = rect


def gimmesprite(rect, spritesheet, xdesired, ydesired):
    # INPUTS: Rectangle representing desired coordinates and dimensions of image on spritesheet,
    # the pygame image representing the spritesheet itself, and the x and y size the image should be scaled to
    # OUTPUTS: A pygame image that is a subsection of the spritesheet. You'll need ot edit its rectangle to get it
    # to draw on a different portion of the screen
    myrect = rect
    myspritesheet = spritesheet
    myxdesired = xdesired
    myydesired = ydesired
    image = pg.Surface(myrect.size)
    # this is to generate the surface that the formatted image will live in
    image.blit(myspritesheet, (0, 0), myrect)  # this jams the given first argument onto the newly created surface
    image = pg.transform.scale(image, (myxdesired, myydesired))
    return image


class Node:
    # This class exists to keep track of the tiles of the maze. Add new member variables and functions as needed. Right
    # now all it knows how to do is draw itself, using a colored-in rectangle if no image is supplied
    # INPUTS: A pygame surface, rectangle, and image, an rgb tuple for color, whether or not the node is traversable,
    #  and a desired nodesize (this does nothing right now)
    def __init__(self, surface, nodesize, rect, color, traversable, image):
        self.surface = surface
        self.nodesize = nodesize
        self.rect = rect
        self.color = color
        self.traversable = traversable
        self.image = image
        self.distfrompac = 0
        self.updated = False
        self.edgeto = []  # List of nodes that can be traveled to

    def __repr__(self):
        return "Node located at {}, {}. Colored {}. {}Traversable. ".format(self.rect.left, self.rect.top, self.color,
                                                                            "Non" if not self.traversable else "Is")

    def draw(self):
        if not self.image:
            pg.draw.rect(self.surface, self.color, self.rect)
        else:
            self.surface.blit(self.image, self.rect)


# Fills out all nodes edgeto lists
def linknodes(nodes):
    for x in range(28):
        for y in range(31):
            # Out of bounds check
            if y != 0:
                # If current node and adjecent nodes are traversable, adds adjacent nodes to edgeto list
                if nodes[y][x].traversable and nodes[y-1][x].traversable:
                    nodes[y][x].edgeto.append(nodes[y-1][x])
            if y != 30:
                if nodes[y][x].traversable and nodes[y+1][x].traversable:
                    nodes[y][x].edgeto.append(nodes[y+1][x])
            if x != 0:
                if nodes[y][x].traversable and nodes[y][x-1].traversable:
                    nodes[y][x].edgeto.append(nodes[y][x-1])
            if x != 27:
                if nodes[y][x].traversable and nodes[y][x+1].traversable:
                    nodes[y][x].edgeto.append(nodes[y][x+1])


# Recursive driver to set nodes' distances from pacman
def setdistancefrompacman(pacman: Pacman):
    y, x = pacman.selfnode
    node = pacman.allnodes[y][x]
    node.updated = True
    node.distfrompac = 0
    setdistance(node)

    # Reset updated in all nodes
    for ylist in pacman.allnodes:
        for node in ylist:
            node.updated = False


# Recursively sets nodes' distance from pacman
def setdistance(node: Node):
    # For all edges in the node
    for edgenode in node.edgeto:
        # if the node has not been updated
        if (not edgenode.updated) or (edgenode.distfrompac > node.distfrompac):
            edgenode.distfrompac = node.distfrompac + 1
            edgenode.updated = True
            setdistance(edgenode)


def ghostimages(spritesheet):
    blinkyimages = []
    clydeimages = []
    inkyimages = []
    pinkyimages = []
    for i in range(16):
        if i < 8:
            blinkyimages.append(
                gimmesprite(pg.Rect((457 + 16 * i, 65, 14, 14)), spritesheet, xdesired=14, ydesired=14))
            clydeimages.append(
                gimmesprite(pg.Rect((457 + 16 * i, 113, 14, 14)), spritesheet, xdesired=14, ydesired=14))
            inkyimages.append(
                gimmesprite(pg.Rect((457 + 16 * i, 97, 14, 14)), spritesheet, xdesired=14, ydesired=14))
            pinkyimages.append(
                gimmesprite(pg.Rect((457 + 16 * i, 81, 14, 14)), spritesheet, xdesired=14, ydesired=14))
        elif 8 <= i < 12:
            blinkyimages.append(
                gimmesprite(pg.Rect((457 + 16 * (i-8), 65, 14, 14)), spritesheet, xdesired=14, ydesired=14))
            clydeimages.append(
                gimmesprite(pg.Rect((585 + 16 * (i - 8), 65, 14, 14)), spritesheet, xdesired=14, ydesired=14))
            inkyimages.append(
                gimmesprite(pg.Rect((585 + 16 * (i - 8), 65, 14, 14)), spritesheet, xdesired=14, ydesired=14))
            pinkyimages.append(
                gimmesprite(pg.Rect((585 + 16 * (i - 8), 65, 14, 14)), spritesheet, xdesired=14, ydesired=14))
        elif 12 <= i < 16:
            blinkyimages.append(
                gimmesprite(pg.Rect((585 + 16 * (i - 12), 81, 14, 14)), spritesheet, xdesired=14, ydesired=14))
            clydeimages.append(
                gimmesprite(pg.Rect((585 + 16 * (i - 12), 81, 14, 14)), spritesheet, xdesired=14, ydesired=14))
            inkyimages.append(
                gimmesprite(pg.Rect((585 + 16 * (i - 12), 81, 14, 14)), spritesheet, xdesired=14, ydesired=14))
            pinkyimages.append(
                gimmesprite(pg.Rect((585 + 16 * (i - 12), 81, 14, 14)), spritesheet, xdesired=14, ydesired=14))
    myDict = {"blinky": blinkyimages, "clyde": clydeimages, "inky": inkyimages, "pinky": pinkyimages}
    return myDict

def pacmanimages(spritesheet):
    pacmanimages = []
    for i in range(20):
        if 0 <= i < 2:
            pacmanimages.append(gimmesprite(pg.Rect(457 + i*16, 1, 13, 13), spritesheet, 13, 13))
        if 2 <= i < 4:
            pacmanimages.append(gimmesprite(pg.Rect(457 + (i-2)*16, 17, 13, 13), spritesheet, 13, 13))
        if 4 <= i < 6:
            pacmanimages.append(gimmesprite(pg.Rect(457 + (i-4)*16, 33, 13, 13), spritesheet, 13, 13))
        if 6 <= i < 8:
            pacmanimages.append(gimmesprite(pg.Rect(457 + (i-6)*16, 49, 13, 13), spritesheet, 13, 13))
        if 8 <= i:
            pacmanimages.append(gimmesprite(pg.Rect(489 + (i-8)*16, 1, 15, 15), spritesheet, 15, 15))
    return pacmanimages

def fruitimages(spritesheet):
    fruitimages = []
    for i in range(8):
        fruitimages.append(gimmesprite(pg.Rect(489 + 16*i, 49, 14, 14), spritesheet, 14, 14))
    return fruitimages


class Maze:
    # This class actually plays the game, but its arguments are unusued currently.
    def __init__(self, game, pacman, ghosts, score):
        pg.init()
        self.myclock = pg.time.Clock()
        self.screen = pg.display.set_mode((1200, 800))
        self.image = pg.Surface((800, 800))
        self.spritesheet = pg.image.load("spritesheet.png")
        self.pacmanimages = pacmanimages(self.spritesheet)
        self.fruitimages = fruitimages(self.spritesheet)
        self.frame = 36
        self.rect = (0, 0, 800, 800)
        self.game = game
        self.pacmanspeed = 4
        self.pacmanvelocity = self.pacmanspeed * Vector(-1, 0)
        self.pacmandirection = "left"
        self.ghosts = pg.sprite.Group()
        self.ghostimages = ghostimages(self.spritesheet)
        # self.ghosts.add(Ghost("Blinky", blinky, (13 * NODESIZE, 12 * NODESIZE, 14, 14)))
        self.score = score
        self.f = open("maze.txt", 'r')
        self.nodes = []
        self.currentline = ""
        for p in range(31):
            self.nodes.append([])
        self.editnodes = self.nodes
        for j in range(31):
            # self.nodes.append([])
            self.currentline = self.f.read(29)
            self.currentnodes = self.editnodes[j]
            for i in range(len(self.currentline)):
                temprect = pg.Rect(i * NODESIZE, j * NODESIZE, NODESIZE, NODESIZE)
                if self.currentline[i] == "X":
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE,
                                                  rect=temprect, color=(0, 0, 225),
                                                  image=gimmesprite(temprect, self.spritesheet, 8, 8),
                                                  traversable=False))
                elif self.currentline[i] == "O":
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE,
                                                  rect=temprect, color=(0, 0, 0), image=False, traversable=True))
                elif self.currentline[i] == "P":
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE,
                                                  rect=temprect, color=(255, 255, 225), image=False, traversable=True))
                elif self.currentline[i] == "E":
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE,
                                                  rect=temprect, color=(0, 0, 0), image=False, traversable=True))
                elif self.currentline[i] == "G":
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE,
                                                  rect=temprect, color=(255, 255, 255), image=False, traversable=False))
                elif self.currentline[i] == "1":
                    self.blinky = Ghost(surface=self.screen, name='blinky', images=self.ghostimages["blinky"], direction="up",
                                        rect=pg.Rect(i * NODESIZE - NODESIZE/2, j * NODESIZE - NODESIZE/2, 14, 14),
                                        state="fleeing", selfnode=(j, i), allnodes=self.nodes)
                    # ghost1 = gimmesprite(rect=pg.Rect(457, 65, 14, 14), spritesheet=self.spritesheet,
                    #                      xdesired=NODESIZE, ydesired=NODESIZE)
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE, rect=temprect,
                                                  color=(0, 0, 0), image=False, traversable=True))
                elif self.currentline[i] == "2":
                    self.clyde = Ghost(surface=self.screen, name='clyde', images=self.ghostimages["clyde"],
                                       direction="up", rect=pg.Rect(temprect.left-15, temprect.top, 14, 14),
                                       state="fleeing", selfnode=(j, i), allnodes=self.nodes)
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE, rect=temprect,
                                                  color=(0, 0, 0), image=False, traversable=True))
                elif self.currentline[i] == "3":
                    self.inky = Ghost(surface=self.screen, name='inky', images=self.ghostimages["inky"], direction="up",
                                      rect=pg.Rect(temprect.left-7, temprect.top, 14, 14),
                                      state="fleeing", selfnode=(j, i), allnodes=self.nodes)
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE, rect=temprect,
                                                  color=(0, 0, 0), image=False, traversable=True))
                elif self.currentline[i] == "4":
                    self.pinky = Ghost(surface=self.screen, name='pinky', images=self.ghostimages["pinky"],
                                       direction="up", rect=pg.Rect(temprect.left+2, temprect.top, 14, 14),
                                       state="fleeing", selfnode=(j, i), allnodes=self.nodes)
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE, rect=temprect,
                                                  color=(0, 0, 0), image=False, traversable=True))
                elif self.currentline[i] == "@":
                    self.mytop = j
                    self.myleft = i
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE, rect=temprect,
                                                  color=(0, 0, 0), image=False, traversable=True))
            self.nodes[j] = self.currentnodes
            # the nodes are written in row, column format due to being taken in as a row of characters by f.read
            # as a result of this, the node at [row][column] is located at position [y][x]
        self.f.close()
        linknodes(self.nodes)
        #print(self.nodes[0][6].traversable)
        temptemprect = pg.Rect(0, 0, 13, 13)
        temptemprect.centerx = self.nodes[self.mytop][self.myleft].rect.centerx
        temptemprect.centery = self.nodes[self.mytop][self.myleft].rect.centery
        self.pacmannodes = self.nodes
        self.pacman = Pacman(surface=self.screen, images=self.pacmanimages, velocity=self.pacmanvelocity,
                             rect=pg.Rect(temptemprect.left, temptemprect.y, 13, 13), direction=self.pacmandirection,
                             selfnode=(self.mytop, self.myleft), allnodes=self.pacmannodes)
        self.ghosts.add(self.blinky, self.clyde, self.inky, self.pinky)

    def __repr__(self):
        pass

    def draw(self):
        self.game.screen.blit(self.image, self.rect)

    def update(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        sys.exit()
                    elif event.key == pg.K_w or event.key == pg.K_UP:
                        #if self.nodes[self.pacman.selfnode[0]-1][self.pacman.selfnode[1]].traversable:
                        self.pacman.direction = "up"#self.pacmanspeed * Vector(0, -1)
                        # if self.nodes[self.mytop - 1][self.myleft].traversable:
                        #     self.mytop -= 1
                    elif event.key == pg.K_a or event.key == pg.K_LEFT:
                        self.pacman.direction = "left"
                        #self.pacman.velocity = self.pacmanspeed * Vector(-1, 0)
                        # if self.nodes[self.mytop][self.myleft - 1].traversable:
                        #     self.myleft -= 1
                    elif event.key == pg.K_s or event.key == pg.K_DOWN:
                        self.pacman.direction = "down"
                        # self.pacman.velocity = self.pacmanspeed * Vector(0, 1)
                        # if self.nodes[self.mytop + 1][self.myleft].traversable:
                        #     self.mytop += 1
                    elif event.key == pg.K_d or event.key == pg.K_RIGHT:
                        self.pacman.direction = "right"
                        #self.pacman.velocity = self.pacmanspeed * Vector(1, 0)
                        # if self.nodes[self.mytop][self.myleft + 1].traversable:
                        #     self.myleft += 1
            for j in range(len(self.nodes)):
                for node in self.nodes[j]:
                    node.draw()
            # pg.draw.rect(self.screen, self.tempacman.get("color"), (self.myleft * NODESIZE, self.mytop * NODESIZE,
            #                                                         NODESIZE, NODESIZE))
            self.pacman.update()
            self.pacman.draw()
            self.ghosts.update()
            self.ghosts.draw(self.screen)
            pg.display.update()
            print("running")
            self.myclock.tick(33)


class Animator:
    def drawtext(self, text,  x, y):
        textobj = self.font.render(text, 1, (255, 255, 255))
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        self.surface.blit(textobj, textrect)

    def __init__(self, maze):
        self.maze = maze
        self.surface = self.maze.screen
        self.pacmanimages = self.maze.pacmanimages[:]
        for i in range(len(self.pacmanimages)):
            self.pacmanimages[i] = pg.transform.scale(self.pacmanimages[i], (60, 60))
        self.ghostimages = self.maze.ghostimages
        self.ghosts = self.maze.ghosts
        self.font = pg.font.SysFont(None, 48)
        self.animatedwindow = pg.Surface((self.surface.get_width(), self.surface.get_height()/3))
        self.pacman = DumbPacman(surface=self.animatedwindow, images=self.pacmanimages, velocity=Vector(-4, 0),
                                 direction="left", rect=pg.Rect(400, 200, 60, 60), selfnode=(0, 0),
                                 allnodes=self.maze.pacmannodes)
        self.pacman.framecount = 2
        self.blinky = Ghost(surface=self.animatedwindow, images=self.ghostimages["blinky"],
                            rect=pg.Rect(600, 200, 60, 60), direction="left", state="living")
        self.inky = Ghost(surface=self.animatedwindow, images=self.ghostimages["inky"], direction="left",
                          rect=pg.Rect(660, 200, 60, 60),
                          state="living")
        self.pinky = Ghost(surface=self.animatedwindow, images=self.ghostimages["pinky"], direction="left",
                           rect=pg.Rect(720, 200, 60, 60),
                           state="fleeing")
        self.clyde = Ghost(surface=self.animatedwindow, images=self.ghostimages["clyde"], direction="left",
                           rect=pg.Rect(780, 200, 60, 60),
                           state="fleeing")
        self.tempghosts = pg.sprite.Group()
        self.tempghosts.add(self.blinky, self.inky, self.pinky, self.clyde)

    def showghost(self, ghostname, x, y):
        tempblinkyimage = self.ghostimages[ghostname][0]
        tempblinkyimage = pg.transform.scale(tempblinkyimage, (60, 60))
        tempblinkyimagerect = tempblinkyimage.get_rect()
        tempblinkyimagerect.topleft = (x, y)
        pg.time.delay(1000)
        self.surface.blit(tempblinkyimage, tempblinkyimagerect)
        pg.display.update()
        pg.time.delay(1000)
        if ghostname == "blinky":
            Animator.drawtext(self, '-Shadow', x=x + 200, y=y)
            pg.display.update()
            pg.time.delay(1000)
            Animator.drawtext(self, '"Blinky"', x=x + 400, y=y)
        elif ghostname == "pinky":
            Animator.drawtext(self, '-Speedy', x=x + 200, y=y)
            pg.display.update()
            pg.time.delay(1000)
            Animator.drawtext(self, '"Pinky"', x=x + 400, y=y)
        elif ghostname == "inky":
            Animator.drawtext(self, '-Bashful', x=x + 200, y=y)
            pg.display.update()
            pg.time.delay(1000)
            Animator.drawtext(self, '"Inky"', x=x + 400, y=y)
        elif ghostname == "clyde":
            Animator.drawtext(self, '-Pokey', x=x + 200, y=y)
            pg.display.update()
            pg.time.delay(1000)
            Animator.drawtext(self, '"Clyde"', x=x + 400, y=y)
        pg.display.update()

    def animate(self):
        self.surface.fill((0, 0, 0))
        Animator.drawtext(self, "Character / Nickname", x=400, y=0)
        pg.display.update()
        Animator.showghost(self, "blinky", 200, 50)
        Animator.showghost(self, "pinky", 200, 150)
        Animator.showghost(self, "inky", 200, 250)
        Animator.showghost(self, "clyde", 200, 350)
        for i in range(100):
            pg.time.delay(100)
            self.pacman.update()
            self.pacman.surface.fill((0, 0, 0))
            self.pacman.draw()
            self.surface.blit(self.pacman.surface, (0, 400))
            pg.display.update()
        pg.time.delay(3000)
        self.surface.fill((0,0,0))
        pg.display.update()


def main():
    maze = Maze(0, 0, 0, 0)
    # animator = Animator(maze)
    # animator.animate()
    maze.update()


if __name__ == '__main__':
    main()
