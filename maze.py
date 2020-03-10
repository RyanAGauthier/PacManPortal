import pygame as pg
import sys
from vector import Vector
from random import randrange


NODESIZE = 8
FPS = 33


class Ghost(pg.sprite.Sprite):
    # This is the class that represents the ghosts, there will be four individual instances in total
    # The class inherits from sprite so that we can later use sprite.groupcollide() between pacman and each ghost
    # Each ghost can draw and update itself, currently it just needs to implement the state parameter, which is intended
    # to tell the ghost whether it is fleeing, respawning, just eyeballs, etc

    def __init__(self, surface, images, rect, direction, state, status, name=None, selfnode=None, allnodes=None):
        pg.sprite.Sprite.__init__(self)
        self.surface = surface
        self.name = name
        self.images = images
        self.currentframe = 0
        self.duration = FPS * 10
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
        self.status = status
        self.framecount = FPS // 3  # This dictates how many game frames should pass between different images
        self.frameclock = self.framecount

    def changedirection(self, newdirection):
        self.direction = newdirection

    def changestatus(self, newstatus):
        self.status = newstatus
        if self.status == "alive":
            pass
        elif self.status == "vulnerable":
            self.duration = 10 * FPS
        elif self.status == "dead":
            pass

    def changestate(self, newstate):
        self.state = newstate
        if self.state == "shopping":
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
        if self.state == 'fleeing' or self.status == 'vulnerable':
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

        leftneigh = 27 if self.selfnode[1] == 0 else self.selfnode[1] - 1
        rightneigh = 0 if self.selfnode[1] == 27 else self.selfnode[1] + 1

        if self.targetnode == self.allnodes[self.selfnode[0] - 1][self.selfnode[1]]:
            self.changedirection('up')
            if self.targetnode.traversable and self.rect.centerx == \
                    self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx:
                self.velocity = Vector(0, -2)
        elif self.targetnode == self.allnodes[self.selfnode[0] + 1][self.selfnode[1]]:
            self.changedirection('down')
            if self.targetnode.traversable and self.rect.centerx == \
                    self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx:
                self.velocity = Vector(0, 2)
        elif self.targetnode == self.allnodes[self.selfnode[0]][rightneigh]:
            self.changedirection('right')
            if self.targetnode.traversable and self.rect.centery == \
                    self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery:
                self.velocity = Vector(2, 0)
        elif self.targetnode == self.allnodes[self.selfnode[0]][leftneigh]:
            self.changedirection('left')
            if self.targetnode.traversable and self.rect.centery == \
                    self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery:
                self.velocity = Vector(-2, 0)

        # Checking centers to see if self node should be changed?
        if self.velocity == Vector(-2, 0):
            # self.targetnode = self.allnodes[self.selfnode[0]][self.selfnode[1] - 1]
            if self.targetnode.traversable or self.rect.centerx > \
                    self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx:
                self.rect.centerx += self.velocity.x
                if self.rect.centerx < self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx - 4:
                    if self.selfnode[1] != 0:
                        self.selfnode = (self.selfnode[0], self.selfnode[1] - 1)
                    else:
                        self.selfnode = (self.selfnode[0], 27)
                        self.rect.centerx = NODESIZE * 27
        elif self.velocity == Vector(2, 0):
            # self.targetnode = self.allnodes[self.selfnode[0]][self.selfnode[1] + 1]
            if self.targetnode.traversable or self.rect.centerx < \
                    self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx:
                self.rect.centerx += self.velocity.x
                if self.rect.centerx > self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx + 4:
                    if self.selfnode[1] != 27:
                        self.selfnode = (self.selfnode[0], self.selfnode[1] + 1)
                    else:
                        self.selfnode = (self.selfnode[0], 0)
                        self.rect.centerx = 0
        elif self.velocity == Vector(0, 2):
            # self.targetnode = self.allnodes[self.selfnode[0]+1][self.selfnode[1]]
            if self.targetnode.traversable or self.rect.centery < \
                    self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery:
                self.rect.centery += self.velocity.y
                if self.rect.centery > self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery + 4:
                    self.selfnode = (self.selfnode[0] + 1, self.selfnode[1])
        elif self.velocity == Vector(0, -2):
            # self.targetnode = self.allnodes[self.selfnode[0] - 1][self.selfnode[1]]
            if self.targetnode.traversable or self.rect.centery > \
                    self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery:
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

    def getimage(self):
        # Changes current frame to make sense relative to the state of the ghost object
        if self.status == "alive":
            # Makes the ghost face the direction it's travelling in
            if self.direction == "up":
                # self.velocity = self.speed * (0, -1)
                if self.currentframe != 5:
                    self.currentframe = 4
            elif self.direction == "down":
                # self.velocity = self.speed * (0, 1)
                if self.currentframe != 7:
                    self.currentframe = 6
            elif self.direction == "left":
                # self.velocity = self.speed * (-1, 0)
                if self.currentframe != 3:
                    self.currentframe = 2
            elif self.direction == "right":
                # self.velocity = self.speed * (1, 0)
                if self.currentframe != 1:
                    self.currentframe = 0
        if self.status == "dead":
            # Makes the eyeballs of the ghost face the direction it's travelling in
            if self.direction == "right":
                self.currentframe = 12
            elif self.direction == "left":
                self.currentframe = 13
            elif self.direction == "up":
                self.currentframe = 14
            elif self.direction == "down":
                self.currentframe = 15
        elif self.status == "vulnerable":
            # Handles the blue -> white ghost coloring transition and removes vulnerability when the duration is up
            if self.duration > 3 * FPS:
                if self.currentframe != 9:
                    self.currentframe = 8
                self.duration -= 1
            elif self.duration > 0:
                if self.duration % (3 * FPS // 4) > ((3 * FPS // 4)//2):
                    if self.currentframe != 11:
                        self.currentframe = 10
                else:
                    if self.currentframe != 9:
                        self.currentframe = 8
                self.duration -= 1
            else:
                self.duration = 10 * FPS
                self.status = "alive"
                if self.direction == "up":
                    self.currentframe = 4
                elif self.direction == "left":
                    self.currentframe = 2
                elif self.direction == "right":
                    self.currentframe = 0
                elif self.direction == "down":
                    self.currentframe = 6
        if self.frameclock == 1:
            if self.status != "dead":
                if self.currentframe % 2 == 0:
                    self.currentframe += 1
                else:
                    self.currentframe -= 1
                self.frameclock = self.framecount
        else:
            self.frameclock -= 1
        self.image = self.images[self.currentframe]

    def update(self):

        if self.name == 'blinky':
            # Blinky is always chasing
            self.changestate('chasing')

        self.targetnode = self.get_target()
        self.move()
        self.getimage()
        print("displaying frame {}".format(self.currentframe))


class DumbGhost(Ghost):
    def __init__(self, surface, name, images, rect, direction, state, status):
        super().__init__(surface=surface, name=name, images=images, rect=rect, direction=direction,
                         state=state, status=status, selfnode=0, allnodes=0)

    def draw(self):
        self.surface.blit(self.image, self.rect)

    def move(self):
        pass

    def update(self):
        # This is the portion of the object that handles the animation, swapping between 3 and 4 legs at a rate decided
        # by self.framecount
        self.getimage()
        if self.direction == "left":
            self.rect.left += -5
        elif self.direction == "right":
            self.rect.left += 4
        # print("displaying frame {}".format(self.currentframe))


class Pacman(pg.sprite.Sprite):
    def __init__(self, surface, images, velocity, direction, rect, selfnode, allnodes, maze):
        pg.sprite.Sprite.__init__(self)
        self.maze = maze
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
            if self.targetnode.traversable and self.rect.centerx == \
                    self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx:
                self.velocity = Vector(0, -4)
        elif self.direction == "down":
            self.targetnode = self.allnodes[self.selfnode[0] + 1][self.selfnode[1]]
            if self.targetnode.traversable and self.rect.centerx == \
                    self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx:
                self.velocity = Vector(0, 4)
        elif self.direction == "right":
            if self.selfnode[1] != 27:
                self.targetnode = self.allnodes[self.selfnode[0]][self.selfnode[1] + 1]
            else:
                self.targetnode = self.allnodes[self.selfnode[0]][0]
            if self.targetnode.traversable and self.rect.centery == \
                    self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery:
                self.velocity = Vector(4, 0)
        elif self.direction == "left":
            if self.selfnode[1] != 0:
                self.targetnode = self.allnodes[self.selfnode[0]][self.selfnode[1] - 1]
            else:
                self.targetnode = self.allnodes[self.selfnode[0]][27]
            if self.targetnode.traversable and self.rect.centery == \
                    self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery:
                self.velocity = Vector(-4, 0)

        # Checking centers to see if self node should be changed?
        if self.velocity == Vector(-4, 0):
            if self.selfnode[1] != 0:
                self.targetnode = self.allnodes[self.selfnode[0]][self.selfnode[1] - 1]
            else:
                self.targetnode = self.allnodes[self.selfnode[0]][27]
            if self.targetnode.traversable or self.rect.centerx > \
                    self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx:
                self.rect.centerx += self.velocity.x
                if self.rect.centerx < self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx - 4:
                    if self.selfnode[1] != 0:
                        self.selfnode = (self.selfnode[0], self.selfnode[1] - 1)
                    else:
                        self.selfnode = (self.selfnode[0], 27)
                        self.rect.centerx = NODESIZE * 27
                    setdistancefrompacman(pacman=self)
        elif self.velocity == Vector(4, 0):
            if self.selfnode[1] != 27:
                self.targetnode = self.allnodes[self.selfnode[0]][self.selfnode[1] + 1]
            else:
                self.targetnode = self.allnodes[self.selfnode[0]][0]
            if self.targetnode.traversable or self.rect.centerx < \
                    self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx:
                self.rect.centerx += self.velocity.x
                if self.rect.centerx > self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx + 4:
                    if self.selfnode[1] != 27:
                        self.selfnode = (self.selfnode[0], self.selfnode[1] + 1)
                    else:
                        self.selfnode = (self.selfnode[0], 0)
                        self.rect.centerx = 0
                    setdistancefrompacman(pacman=self)
        elif self.velocity == Vector(0, 4):
            self.targetnode = self.allnodes[self.selfnode[0]+1][self.selfnode[1]]
            if self.targetnode.traversable or self.rect.centery < \
                    self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery:
                self.rect.centery += self.velocity.y
                if self.rect.centery > self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery + 4:
                    self.selfnode = (self.selfnode[0] + 1, self.selfnode[1])
                    setdistancefrompacman(pacman=self)
        elif self.velocity == Vector(0, -4):
            self.targetnode = self.allnodes[self.selfnode[0] - 1][self.selfnode[1]]
            if self.targetnode.traversable or self.rect.centery > \
                    self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery:
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
        # print("displaying frame {}".format(self.currentframe))

    def die(self):
        for i in range(12):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        sys.exit()
            self.image = self.images[i+8]
            self.draw()
            tempscreen = pg.transform.scale2x(self.surface)
            self.maze.surface.blit(tempscreen, (50, 50))
            pg.display.update()
            pg.time.delay(100)
        for i in range(10):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        sys.exit()
            pg.time.delay(100)

    def draw(self):
        self.surface.blit(self.image, self.rect)


class DumbPacman(Pacman):
    def __init__(self, surface, images, velocity, direction, rect, selfnode, allnodes):
        super().__init__(surface=surface, images=images, velocity=velocity, direction=direction,
                         rect=rect, selfnode=selfnode, allnodes=allnodes, maze=0)

    def move(self):
        if self.direction == "left":
            self.rect.left -= 4
        elif self.direction == "right":
            self.rect.left += 8

    # def draw(self):
    #     self.surface.fill((0, 0, 0))
    #     self.surface.blit(self.image, self.rect)


class StaticObject(pg.sprite.Sprite):
    def __init__(self, surface, image, rect, pointvalue, animated=False):
        pg.sprite.Sprite.__init__(self)
        self.surface = surface
        self.image = image
        self.currentframe = 0
        self.rect = rect
        self.pointvalue = pointvalue
        self.animated = animated  # If animated, flicker twice a second default. This will probably just be power pills
        self.framecount = FPS // 2
        self.frameclock = self.framecount

    def update(self):
        if self.animated:
            if self.frameclock == 1:
                if self.currentframe % 2 == 0:
                    self.currentframe += 1
                else:
                    self.currentframe -= 1
                self.frameclock = self.framecount
            else:
                self.frameclock -= 1
            # self.image = self.images[self.currentframe]

    def draw(self):
        self.surface.blit(self.image, self.rect)


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

    if nodes[14][0].traversable and nodes[14][27].traversable:
        nodes[14][0].edgeto.append(nodes[14][27])
        nodes[14][27].edgeto.append(nodes[14][0])


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
                gimmesprite(pg.Rect((457 + 16 * i, 65, 14, 14)), spritesheet, xdesired=14, ydesired=14))
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
    mydict = {"blinky": blinkyimages, "clyde": clydeimages, "inky": inkyimages, "pinky": pinkyimages}
    return mydict


def pacmanimages(spritesheet):
    temppacmanimages = []
    for i in range(20):
        if 0 <= i < 2:
            temppacmanimages.append(gimmesprite(pg.Rect(457 + i*16, 1, 13, 13), spritesheet, 13, 13))
        if 2 <= i < 4:
            temppacmanimages.append(gimmesprite(pg.Rect(457 + (i-2)*16, 17, 13, 13), spritesheet, 13, 13))
        if 4 <= i < 6:
            temppacmanimages.append(gimmesprite(pg.Rect(457 + (i-4)*16, 33, 13, 13), spritesheet, 13, 13))
        if 6 <= i < 8:
            temppacmanimages.append(gimmesprite(pg.Rect(457 + (i-6)*16, 49, 13, 13), spritesheet, 13, 13))
        if 8 <= i:
            temppacmanimages.append(gimmesprite(pg.Rect(489 + (i-8)*16, 1, 15, 15), spritesheet, 15, 15))
    return temppacmanimages


def fruitimages(spritesheet):
    tempfruitimages = []
    for i in range(8):
        tempfruitimages.append(gimmesprite(pg.Rect(489 + 16*i, 49, 14, 14), spritesheet, 14, 14))
    return tempfruitimages


def pointimages(spritesheet):
    temppointimages = []
    for i in range(12):
        if i < 3:
            temppointimages.append(gimmesprite(pg.Rect(456 + 16 * i, 133, 15, 7), spritesheet, 15, 7))
        elif i == 3:
            temppointimages.append(gimmesprite(pg.Rect(456 + 16 * i, 133, 16, 7), spritesheet, 16, 7))
        elif 4 <= i < 8:
            temppointimages.append(gimmesprite(pg.Rect(456 + 16 * (i-4), 148, 15, 7), spritesheet, 15, 7))
        elif i == 8:
            temppointimages.append(gimmesprite(pg.Rect(456 + 16 * (i - 4), 148, 18, 7), spritesheet, 18, 7))
        elif 9 <= i < 12:
            temppointimages.append(gimmesprite(pg.Rect(518, 164 + 16 * (i-9), 20, 7), spritesheet, 20, 7))
    return temppointimages


class Maze:
    # This class actually plays the game, but its arguments are unusued currently.
    def __init__(self, game, score=0):
        pg.init()
        self.myclock = pg.time.Clock()
        self.screen = pg.Surface((400, 400))
        self.image = pg.Surface((1200, 800))
        self.surface = pg.display.set_mode((1200, 800))
        # sounds courtesy of https://www.classicgaming.cc/classics/pac-man/sounds
        self.pacmaneating = 'pacman_chomp.ogg'
        self.sounds = [{'eat_ghost': 'eat_ghost.ogg', 'munch_1': 'munch_1.ogg', 'munch_2': 'munch_2.ogg',
                        'eatpowerpellet': 'power_pellet.ogg', 'eatfruit': 'pacman_eatfruit.ogg',
                        'gamestart': 'game_start.ogg', 'pacmandeath': 'pacman_death.ogg',
                        'ghostkilled': 'retreating.ogg', 'pacman_eat': 'pacman_chomp.ogg'}]
        self.audio = Audio(self.sounds, self.pacmaneating, playing=False)
        # self.audio.playing = True
        self.spritesheet = pg.image.load("spritesheet.png")
        self.pacmanimages = pacmanimages(self.spritesheet)
        self.fruitimages = fruitimages(self.spritesheet)
        self.pointimages = pointimages(self.spritesheet)
        self.binaryindex = 0
        # self.miscimages = miscimages(self.spritesheet)
        self.frame = 36
        self.rect = (0, 0, 800, 800)
        self.game = game
        self.pacmanspeed = 4
        self.pacmanvelocity = self.pacmanspeed * Vector(-1, 0)
        self.pacmandirection = "left"
        self.ghosts = pg.sprite.Group()
        self.ghostimages = ghostimages(self.spritesheet)
        self.score = score
        self.highscores = [0, 0, 0]
        self.powerpellets = pg.sprite.Group()
        self.pellets = pg.sprite.Group()
        self.fruit = pg.sprite.Group()
        self.fruitspawned = False
        self.pelletsleft = 0
        self.level = 0
        self.lives = 3
        self.font = pg.font.SysFont(None, 28)
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
                    temptemprect = pg.Rect(0, 0, 2, 2)
                    temptemprect.centerx = temprect.centerx
                    temptemprect.centery = temprect.centery
                    pellet = StaticObject(surface=self.screen,
                                          image=gimmesprite(pg.Rect(11, 11, 2, 2), self.spritesheet, 2, 2),
                                          rect=temptemprect, pointvalue=10)
                    pellet.add(self.pellets)
                    self.pelletsleft += 1
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE,
                                                  rect=temprect, color=(0, 0, 0), image=False, traversable=True))
                elif self.currentline[i] == "P":
                    powerpellet = StaticObject(surface=self.screen,
                                               image=gimmesprite(pg.Rect(8, 23*8, 8, 8), self.spritesheet, 8, 8),
                                               rect=temprect, pointvalue=50)
                    self.pelletsleft += 1
                    powerpellet.add(self.powerpellets)
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE,
                                                  rect=temprect, color=(0, 0, 0), image=False, traversable=True))
                elif self.currentline[i] == "E":
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE,
                                                  rect=temprect, color=(0, 0, 0), image=False, traversable=True))
                elif self.currentline[i] == "G":
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE,
                                                  rect=temprect, color=(255, 255, 255), image=False, traversable=False))
                elif self.currentline[i] == "1":
                    self.blinky = Ghost(surface=self.screen, name='blinky',
                                        images=self.ghostimages["blinky"], direction="up",
                                        rect=pg.Rect(i * NODESIZE - NODESIZE/2, j * NODESIZE - NODESIZE/2, 14, 14),
                                        state="chasing", status="alive", selfnode=(j, i), allnodes=self.nodes)
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE, rect=temprect,
                                                  color=(0, 0, 0), image=False, traversable=True))
                elif self.currentline[i] == "2":
                    self.clyde = Ghost(surface=self.screen, name='clyde', images=self.ghostimages["clyde"],
                                       direction="up", rect=pg.Rect(temprect.left - 15, temprect.top, 14, 14),
                                       state="fleeing", status="alive", selfnode=(j, i), allnodes=self.nodes)
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE, rect=temprect,
                                                  color=(0, 0, 0), image=False, traversable=True))
                elif self.currentline[i] == "3":
                    self.inky = Ghost(surface=self.screen, name="inky", images=self.ghostimages["inky"],
                                      direction="up", rect=pg.Rect(temprect.left-7, temprect.top, 14, 14),
                                      state="fleeing", status="alive", selfnode=(j, i), allnodes=self.nodes)
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE, rect=temprect,
                                                  color=(0, 0, 0), image=False, traversable=True))
                elif self.currentline[i] == "4":
                    self.pinky = Ghost(surface=self.screen, name='pinky', images=self.ghostimages["pinky"],
                                       direction="up", rect=pg.Rect(temprect.left+2, temprect.top, 14, 14),
                                       state="fleeing", status="alive", selfnode=(j, i), allnodes=self.nodes)
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

        temptemprect = pg.Rect(0, 0, 13, 13)
        temptemprect.center = self.nodes[self.mytop][self.myleft].rect.center
        self.pacmannodes = self.nodes
        self.pacman = Pacman(surface=self.screen, images=self.pacmanimages, velocity=self.pacmanvelocity,
                             rect=pg.Rect(temptemprect.left, temptemprect.top, 13, 13), direction=self.pacmandirection,
                             selfnode=(self.mytop, self.myleft), allnodes=self.pacmannodes, maze=self)
        self.ghosts.add(self.blinky, self.clyde, self.inky, self.pinky)
        self.audio.playing = True

    def drawtext(self, text, x, y):
        textobj = self.font.render(text, 1, (255, 255, 255))
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        self.screen.blit(textobj, textrect)

    def restart(self, partial=False, level=0):
        self.level = level
        if partial:  # redraw pacman and the ghosts at their spawns
            for sound in self.audio.sounds.keys():
                self.audio.sounds[sound].stop()
            temptemprect = pg.Rect(0, 0, 13, 13)
            temptemprect.center = self.nodes[23][13].rect.center
            self.pacman.rect = temptemprect
            self.pacman.velocity = self.pacmanspeed * Vector(-4, 0)
            self.pacman.direction = 'left'
            self.pacman.selfnode = (23, 13)
            self.pacman.image = self.pacman.images[2]
            self.ghosts.empty()
            self.blinky = Ghost(surface=self.screen, name='blinky', images=self.ghostimages["blinky"], direction="up",
                                rect=pg.Rect(14 * NODESIZE - NODESIZE / 2, 11 * NODESIZE - NODESIZE / 2, 14, 14),
                                state="chasing", status="alive", selfnode=(11, 14), allnodes=self.nodes)
            self.clyde = Ghost(surface=self.screen, name='clyde', images=self.ghostimages["clyde"], direction="up",
                               rect=pg.Rect(13 * NODESIZE - 15, 14 * NODESIZE, 14, 14),
                               state="fleeing", status="alive", selfnode=(14, 13), allnodes=self.nodes)
            self.inky = Ghost(surface=self.screen, name='inky', images=self.ghostimages["inky"], direction="up",
                              rect=pg.Rect(14 * NODESIZE - 7, 14 * NODESIZE, NODESIZE, NODESIZE),
                              state="fleeing", status="alive", selfnode=(14, 14), allnodes=self.nodes)
            self.pinky = Ghost(surface=self.screen, name='pinky', images=self.ghostimages["pinky"], direction="up",
                               rect=pg.Rect(15 * NODESIZE + 2, 14 * NODESIZE, NODESIZE, NODESIZE),
                               state="fleeing", status="alive", selfnode=(14, 15), allnodes=self.nodes)
            self.ghosts.add(self.blinky, self.clyde, self.inky, self.pinky)
            self.screen.fill((0, 0, 0))
            for j in range(len(self.nodes)):
                for node in self.nodes[j]:
                    node.draw()
            self.fruit.draw(self.screen)
            self.pellets.draw(self.screen)
            self.powerpellets.draw(self.screen)
            self.pacman.draw()
            self.ghosts.draw(self.screen)
            temprect = pg.Rect(int(13.5 * NODESIZE), 17 * NODESIZE, 8, 8)
            textobj = self.font.render("Ready?", 1, (255, 255, 255))
            textrect = textobj.get_rect()
            textrect.center = temprect.center
            self.screen.blit(textobj, textrect)
            tempscreen = pg.transform.scale2x(self.screen)
            self.surface.blit(tempscreen, (50, 50))
            pg.display.update()
        else:  # Remake everything, but keep score the same. This mainly exists once a level is completed.
            for sound in self.audio.sounds.keys():
                self.audio.sounds[sound].stop()
            self.fruitspawned = False
            self.pelletsleft = 0
            self.ghosts.empty()
            self.pellets.empty()
            self.powerpellets.empty()
            self.fruit.empty()
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
                        temptemprect = pg.Rect(0, 0, 2, 2)
                        temptemprect.centerx = temprect.centerx
                        temptemprect.centery = temprect.centery
                        pellet = StaticObject(surface=self.screen,
                                              image=gimmesprite(pg.Rect(11, 11, 2, 2), self.spritesheet, 2, 2),
                                              rect=temptemprect, pointvalue=10)
                        pellet.add(self.pellets)
                        self.pelletsleft += 1
                        self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE,
                                                      rect=temprect, color=(0, 0, 0), image=False, traversable=True))
                    elif self.currentline[i] == "P":
                        powerpellet = StaticObject(surface=self.screen,
                                                   image=gimmesprite(pg.Rect(8, 23 * 8, 8, 8), self.spritesheet, 8, 8),
                                                   rect=temprect, pointvalue=50)
                        self.pelletsleft += 1
                        powerpellet.add(self.powerpellets)
                        self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE,
                                                      rect=temprect, color=(0, 0, 0), image=False, traversable=True))
                    elif self.currentline[i] == "E":
                        self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE,
                                                      rect=temprect, color=(0, 0, 0), image=False, traversable=True))
                    elif self.currentline[i] == "G":
                        self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE,
                                                      rect=temprect, color=(255, 255, 255), image=False,
                                                      traversable=True))
                    elif self.currentline[i] == "1":
                        self.blinky = Ghost(surface=self.screen, name='blinky', images=self.ghostimages["blinky"],
                                            direction="up",
                                            rect=pg.Rect(i * NODESIZE - NODESIZE / 2, j * NODESIZE - NODESIZE / 2, 14,
                                                         14),
                                            state="chasing", status="alive", selfnode=(j, i), allnodes=self.nodes)
                        self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE, rect=temprect,
                                                      color=(0, 0, 0), image=False, traversable=True))
                    elif self.currentline[i] == "2":
                        self.clyde = Ghost(surface=self.screen, name='clyde', images=self.ghostimages["clyde"],
                                           direction="up", rect=pg.Rect(temprect.left - 15, temprect.top, 14, 14),
                                           state="fleeing", status="alive", selfnode=(j, i), allnodes=self.nodes)
                        self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE, rect=temprect,
                                                      color=(0, 0, 0), image=False, traversable=True))
                    elif self.currentline[i] == "3":
                        self.inky = Ghost(surface=self.screen, name="inky", images=self.ghostimages["inky"],
                                          direction="up",
                                          rect=pg.Rect(temprect.left - 7, temprect.top, 14, 14),
                                          state="fleeing", status="alive", selfnode=(j, i), allnodes=self.nodes)
                        self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE, rect=temprect,
                                                      color=(0, 0, 0), image=False, traversable=True))
                    elif self.currentline[i] == "4":
                        self.pinky = Ghost(surface=self.screen, name='pinky', images=self.ghostimages["pinky"],
                                           direction="up", rect=pg.Rect(temprect.left + 2, temprect.top, 14, 14),
                                           state="fleeing", status="alive", selfnode=(j, i), allnodes=self.nodes)
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
            temptemprect = pg.Rect(0, 0, 13, 13)
            temptemprect.center = self.nodes[self.mytop][self.myleft].rect.center
            self.pacmannodes = self.nodes
            self.pacman = Pacman(surface=self.screen, images=self.pacmanimages, velocity=self.pacmanvelocity,
                                 rect=pg.Rect(temptemprect.left, temptemprect.top, 13, 13),
                                 direction=self.pacmandirection,
                                 selfnode=(self.mytop, self.myleft), allnodes=self.pacmannodes, maze=self)
            self.ghosts.add(self.blinky, self.clyde, self.inky, self.pinky)
            self.screen.fill((0, 0, 0))
            for j in range(len(self.nodes)):
                for node in self.nodes[j]:
                    node.draw()
            self.fruit.draw(self.screen)
            self.pellets.draw(self.screen)
            self.powerpellets.draw(self.screen)
            self.pacman.draw()
            self.ghosts.draw(self.screen)
            temprect = pg.Rect(int(13.5 * NODESIZE), 17 * NODESIZE, 8, 8)
            textobj = self.font.render("Ready?", 1, (255, 255, 255))
            textrect = textobj.get_rect()
            textrect.center = temprect.center
            self.screen.blit(textobj, textrect)
            tempscreen = pg.transform.scale2x(self.screen)
            self.surface.blit(tempscreen, (50, 50))
            pg.display.update()
        self.audio.playing = True
        self.audio.play_sound('gamestart')
        for i in range(45):
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        sys.exit()
            pg.time.delay(100)

    def gameover(self):
        for sound in self.audio.sounds.keys():
            self.audio.sounds[sound].stop()
        if self.score > self.highscores[0]:
            tempscores = self.highscores[:]
            self.highscores[0] = self.score
            self.highscores[1] = tempscores[0]
            self.highscores[2] = tempscores[1]
        elif self.highscores[0] > self.score > self.highscores[1]:
            tempscores = self.highscores[:]
            self.highscores[1] = self.score
            self.highscores[2] = tempscores[1]
        elif self.highscores[1] > self.score > self.highscores[2]:
            self.highscores[2] = self.score
    # File I/O help courtesy of glial's response at
    # https://www.reddit.com/r/learnpython/comments/2emugh/how_do_i_delete_lines_in_a_text_file/
        infile = open('maze.txt', 'r').readlines()
        with open('maze.txt', 'w') as outfile:
            for index, line in enumerate(infile):
                if index != 31 and index != 32 and index != 33:
                    outfile.write(line)
                elif index == 31:
                    outfile.write(str(self.highscores[0]) + "\n")
                elif index == 32:
                    outfile.write(str(self.highscores[1]) + "\n")
                elif index == 33:
                    outfile.write(str(self.highscores[2]) + "\n")
        temprect = pg.Rect(int(13.5 * NODESIZE), 17 * NODESIZE, 8, 8)
        textobj = self.font.render("GAME OVER", 1, (255, 255, 255))
        textrect = textobj.get_rect()
        textrect.center = temprect.center
        self.screen.blit(textobj, textrect)
        tempscreen = pg.transform.scale2x(self.screen)
        self.surface.blit(tempscreen, (50, 50))
        pg.display.update()
        pg.time.delay(3000)
        sys.exit()

    def __repr__(self):
        pass

    def checkcollisions(self):
        temp = pg.sprite.spritecollideany(sprite=self.pacman, group=self.ghosts)
        if temp and temp.status == 'vulnerable':
            self.audio.play_sound('eat_ghost')
            temp.changestatus('dead')
        elif temp and temp.status == 'alive':
            self.audio.play_sound('pacmandeath')
            self.lives -= 1
            self.pacman.die()
            if self.lives == 0:
                self.gameover()
            self.restart(partial=True)
        temp = pg.sprite.spritecollideany(sprite=self.pacman, group=self.pellets)
        if temp:
            tempsounds = ['munch_1', 'munch_2']
            self.audio.play_sound(tempsounds[self.binaryindex])
            if self.binaryindex == 1:
                self.binaryindex = 0
            else:
                self.binaryindex = 1
            self.score += temp.pointvalue
            self.pelletsleft -= 1
            self.pellets.remove(temp)
        temp = pg.sprite.spritecollide(sprite=self.pacman, group=self.powerpellets, dokill=True)
        if temp:
            self.pelletsleft -= 1
            self.audio.sounds['eatpowerpellet'].stop()
            self.audio.play_sound('eatpowerpellet', args=True, loops=-1, maxtime=10000)
            ghostlist = [self.blinky, self.clyde, self.inky, self.pinky]
            for i in ghostlist:
                if i.status != 'dead':
                    i.changestatus('vulnerable')
                    i.duration = 10 * FPS
        temp = pg.sprite.spritecollideany(sprite=self.pacman, group=self.fruit)
        if temp:
            self.audio.play_sound('eatfruit')
            self.score += temp.pointvalue
            self.fruit.remove(temp)
        if self.pelletsleft < 200 and not self.fruitspawned:
            print("ADDED FRUIT!")
            temprect = pg.Rect(0, 0, 14, 14)
            temprect.centerx = self.nodes[17][13].rect.centerx
            temprect.centery = self.nodes[17][13].rect.centery
            fruit = StaticObject(surface=self.screen, image=self.fruitimages[self.level],
                                 rect=temprect, pointvalue=1000 * (self.level+1))
            fruit.add(self.fruit)
            self.fruitspawned = True
        if self.pelletsleft == 0 and not self.fruit:
            self.level += 1
            if self.level < 8:
                self.restart()
            else:
                self.gameover()

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
                        self.pacman.direction = "up"
                    elif event.key == pg.K_a or event.key == pg.K_LEFT:
                        self.pacman.direction = "left"
                    elif event.key == pg.K_s or event.key == pg.K_DOWN:
                        self.pacman.direction = "down"
                    elif event.key == pg.K_d or event.key == pg.K_RIGHT:
                        self.pacman.direction = "right"
                    elif event.key == pg.K_r:
                        self.restart()
                    elif event.key == pg.K_g:
                        self.gameover()
                    elif event.key == pg.K_l:
                        self.level = 7
            for j in range(len(self.nodes)):
                for node in self.nodes[j]:
                    node.draw()
            self.fruit.draw(self.screen)
            self.pellets.draw(self.screen)
            self.powerpellets.draw(self.screen)
            self.pacman.update()
            self.pacman.draw()
            self.ghosts.update()
            self.ghosts.draw(self.screen)
            self.checkcollisions()
            tempscreen = pg.transform.scale2x(self.screen)
            self.surface.blit(tempscreen, (50, 50))
            self.drawhud()
            print(self.pelletsleft)
            pg.display.update()
            print("Score = {}".format(self.score))
            print("running")
            self.myclock.tick(FPS)

    def drawhud(self):
        pg.draw.rect(self.surface, (0, 0, 0), pg.Rect(0, 0, self.surface.get_width(), 50))
        textobj = self.font.render(str(self.score), 1, (255, 255, 255))
        textobj = pg.transform.scale2x(textobj)
        textrect = textobj.get_rect()
        textrect.topright = (self.surface.get_width() // 2 - 100, 0)
        self.surface.blit(textobj, textrect)
        tempimages = self.pacman.images[:]
        tempimages[1] = pg.transform.scale(tempimages[1], (50, 50))
        for i in range(self.lives):
            self.surface.blit(tempimages[1], (i * 60, 0))
        for i in range(self.level):
            self.surface.blit(pg.transform.scale(self.fruitimages[i], (50, 50)),
                              (50 * i, 550))


class Audio:   # sound(s) and background music
    def __init__(self, sounds, background_src, playing):
        pg.mixer.init()
        self.sounds = {}
        for sound in sounds:
            for k, v in sound.items():
                self.sounds[k] = pg.mixer.Sound(v)
        self.background_src = background_src

        self.playing = playing
        pg.mixer.music.load(self.background_src)
        if self.playing:
            pg.mixer.music.play(-1, 0.0)

    def play_sound(self, sound, args=False, loops=0, maxtime=0):
        if self.playing and sound in self.sounds.keys():
            if args:
                self.sounds[sound].play(loops=loops, maxtime=maxtime)
            else:
                self.sounds[sound].play()

    def toggle(self):
        self.playing = not self.playing
        pg.mixer.music.play(-1, 0.0) if self.playing else pg.mixer.music.stop()

    def game_over(self, game):
        pg.playing = False
        pg.mixer.music.stop()
        self.play_sound(game.GAME_OVER_SOUND)


class Animator:

    def drawtext(self, text, x, y):
        textobj = self.font.render(text, 1, (255, 255, 255))
        textrect = textobj.get_rect()
        textrect.topleft = (x, y)
        self.surface.blit(textobj, textrect)

    def __init__(self, maze):
        self.maze = maze
        self.surface = self.maze.surface
        self.animating = True
        self.counter = 0
        self.currentline = ""
        self.pacmancredit = "credit.ogg"
        self.sounds = [{'eat_ghost': 'eat_ghost.ogg',
                        'eatpowerpellet': 'power_pellet.ogg',
                        'gamestart': 'game_start.ogg', 'munch_1': 'munch_1.ogg', 'munch_2': 'munch_2.ogg'}]
        self.audio = Audio(self.sounds, self.pacmancredit, playing=False)
        self.audio.playing = True
        self.pacmanimages = self.maze.pacmanimages[:]
        for i in range(len(self.pacmanimages)):
            self.pacmanimages[i] = pg.transform.scale(self.pacmanimages[i], (60, 60))
        self.ghostimages = {"blinky": self.maze.ghostimages["blinky"][:], "clyde": self.maze.ghostimages["clyde"][:],
                            "inky": self.maze.ghostimages["inky"][:], "pinky": self.maze.ghostimages["pinky"][:]}
        for i in range(len(self.ghostimages["blinky"])):
            self.ghostimages["blinky"][i] = pg.transform.scale(self.ghostimages["blinky"][i], (60, 60))
            self.ghostimages["clyde"][i] = pg.transform.scale(self.ghostimages["clyde"][i], (60, 60))
            self.ghostimages["inky"][i] = pg.transform.scale(self.ghostimages["inky"][i], (60, 60))
            self.ghostimages["pinky"][i] = pg.transform.scale(self.ghostimages["pinky"][i], (60, 60))
        self.pointimages = self.maze.pointimages[:]
        for i in range(len(self.pointimages)):
            self.pointimages[i] = pg.transform.scale(self.pointimages[i], (60, 20))
        self.font = pg.font.SysFont(None, 48)
        self.animatedwindow = pg.Surface((self.surface.get_width(), self.surface.get_height() // 3))
        self.powerpellets = pg.sprite.Group()
        powerpellet = StaticObject(surface=self.animatedwindow,
                                   image=gimmesprite(pg.Rect(8, 23 * 8, 8, 8), self.maze.spritesheet, 30, 30),
                                   rect=pg.Rect(200, 215, 30, 30), pointvalue=0)
        powerpellet.add(self.powerpellets)
        self.pacman = DumbPacman(surface=self.animatedwindow, images=self.pacmanimages, velocity=Vector(-4, 0),
                                 direction="left", rect=pg.Rect(400, 200, 60, 60), selfnode=(0, 0),
                                 allnodes=self.maze.pacmannodes)
        self.pacman.framecount = 2
        self.blinky = DumbGhost(surface=self.animatedwindow, name="blinky", images=self.ghostimages["blinky"],
                                rect=pg.Rect(600, 200, 60, 60), direction="left", state="chasing", status="alive")
        self.inky = DumbGhost(surface=self.animatedwindow, name="inky", images=self.ghostimages["inky"],
                              direction="left", rect=pg.Rect(660, 200, 60, 60), state="chasing", status="alive")
        self.pinky = DumbGhost(surface=self.animatedwindow, name="pinky", images=self.ghostimages["pinky"],
                               direction="left", rect=pg.Rect(720, 200, 60, 60), state="chasing", status="alive")
        self.clyde = DumbGhost(surface=self.animatedwindow, name="clyde", images=self.ghostimages["clyde"],
                               direction="left", rect=pg.Rect(780, 200, 60, 60), state="chasing", status="alive")
        self.tempghosts = pg.sprite.Group()
        self.tempghosts.add(self.blinky, self.inky, self.pinky, self.clyde)

    def showghost(self, ghostname, x, y):
        tempblinkyimage = self.ghostimages[ghostname][0]
        tempblinkyimage = pg.transform.scale(tempblinkyimage, (60, 60))
        tempblinkyimagerect = tempblinkyimage.get_rect()
        tempblinkyimagerect.topleft = (x, y)
        if self.animating:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        sys.exit()
                    if event.key == pg.K_SPACE:
                        self.animating = False
            if self.animating:
                pg.time.delay(500)
                self.surface.blit(tempblinkyimage, tempblinkyimagerect)
                pg.display.update()
                pg.time.delay(500)
                if ghostname == "blinky":
                    Animator.drawtext(self, '-Shadow', x=x + 200, y=y)
                    pg.display.update()
                    pg.time.delay(500)
                    Animator.drawtext(self, '"Blinky"', x=x + 400, y=y)
                elif ghostname == "pinky":
                    Animator.drawtext(self, '-Speedy', x=x + 200, y=y)
                    pg.display.update()
                    pg.time.delay(500)
                    Animator.drawtext(self, '"Pinky"', x=x + 400, y=y)
                elif ghostname == "inky":
                    Animator.drawtext(self, '-Bashful', x=x + 200, y=y)
                    pg.display.update()
                    pg.time.delay(500)
                    Animator.drawtext(self, '"Inky"', x=x + 400, y=y)
                elif ghostname == "clyde":
                    Animator.drawtext(self, '-Pokey', x=x + 200, y=y)
                    pg.display.update()
                    pg.time.delay(500)
                    Animator.drawtext(self, '"Clyde"', x=x + 400, y=y)
            pg.display.update()

    def menu(self):
        textplay = self.font.render("Play", 1, (255, 255, 255))
        playrect = textplay.get_rect()
        playrect.topleft = (self.surface.get_width()//2 - playrect.width//2,
                            self.surface.get_height()//2 - playrect.height//2 - 100)
        self.surface.blit(textplay, playrect)
        textscore = self.font.render("High Scores", 1, (255, 255, 255))
        scorerect = textscore.get_rect()
        scorerect.topleft = (self.surface.get_width() // 2 - scorerect.width//2,
                             self.surface.get_height()//2 - scorerect.height//2)
        self.surface.blit(textscore, scorerect)
        menuimage = pg.image.load('logo.PNG')
        menurect = menuimage.get_rect()
        menurect.centerx = scorerect.centerx
        menurect.top = 100
        self.surface.blit(menuimage, menurect)
        pg.display.update()
        playing = True
        while playing:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    sys.exit()
                if event.type == pg.MOUSEMOTION:
                    if playrect.collidepoint(event.pos):
                        temprect = pg.Rect(0, 0, playrect.width + 15, playrect.height + 15)
                        temprect.center = playrect.center
                        pg.draw.rect(self.surface, (255, 255, 255), temprect)
                        temprect.width = playrect.width + 10
                        temprect.height = playrect.height + 10
                        temprect.center = playrect.center
                        pg.draw.rect(self.surface, (0, 0, 0), temprect)
                        self.surface.blit(textplay, playrect)
                        pg.display.update()
                    if not playrect.collidepoint(event.pos):
                        temprect = pg.Rect(0, 0, playrect.width + 15, playrect.height + 15)
                        temprect.center = playrect.center
                        pg.draw.rect(self.surface, (0, 0, 0), temprect)
                        self.surface.blit(textplay, playrect)
                        pg.display.update()
                    if scorerect.collidepoint(event.pos):
                        temprect = pg.Rect(0, 0, scorerect.width + 15, scorerect.height + 15)
                        temprect.center = scorerect.center
                        pg.draw.rect(self.surface, (255, 255, 255), temprect)
                        temprect.width = scorerect.width + 10
                        temprect.height = scorerect.height + 10
                        temprect.center = scorerect.center
                        pg.draw.rect(self.surface, (0, 0, 0), temprect)
                        self.surface.blit(textscore, scorerect)
                        pg.display.update()
                    if not scorerect.collidepoint(event.pos):
                        temprect = pg.Rect(0, 0, scorerect.width + 15, scorerect.height + 15)
                        temprect.center = scorerect.center
                        pg.draw.rect(self.surface, (0, 0, 0), temprect)
                        self.surface.blit(textscore, scorerect)
                        pg.display.update()
                if event.type == pg.MOUSEBUTTONDOWN:
                    if playrect.collidepoint(event.pos):
                        playing = False
                    if scorerect.collidepoint(event.pos):  # Display high scores from file
                        score1 = ""
                        score2 = ""
                        score3 = ""
                        tempfile = open("maze.txt", 'r')
                        for j in range(31):
                            self.currentline = tempfile.read(29)
                        self.currentline = tempfile.read(1)  # Get first characters of line
                        while self.currentline != "\n":
                            score1 = score1 + self.currentline
                            self.currentline = tempfile.read(1)
                        self.currentline = tempfile.read(1)  # Increment past newline char
                        while self.currentline != "\n":
                            score2 = score2 + self.currentline
                            self.currentline = tempfile.read(1)
                        self.currentline = tempfile.read(1)
                        while self.currentline != "\n":
                            score3 = score3 + self.currentline
                            self.currentline = tempfile.read(1)
                        tempfile.close()
                        self.drawtext(score1, 600, 500)
                        self.drawtext(score2, 600, 600)
                        self.drawtext(score3, 600, 700)
                        self.maze.highscores = [int(score1), int(score2), int(score3)]
                        pg.display.update()
                        # textscore = self.font.render("High Scores", 1, (255, 255, 255))
                        # scorerect = textscore.get_rect()
                        # scorerect.topleft = (self.surface.get_width() // 2 - scorerect.width // 2,
                        #                      self.surface.get_height() // 2 - scorerect.height // 2)
                        # self.surface.blit(textscore, scorerect)
                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_ESCAPE:
                        sys.exit()
        self.surface.fill((0, 0, 0))
        for j in range(len(self.maze.nodes)):
            for node in self.maze.nodes[j]:
                node.draw()
        self.maze.pellets.draw(self.maze.screen)
        self.maze.powerpellets.draw(self.maze.screen)
        self.maze.pacman.draw()
        self.maze.ghosts.draw(self.maze.screen)
        temprect = pg.Rect(int(13.5 * NODESIZE), 17 * NODESIZE, 8, 8)
        textobj = self.font.render("Ready?", 1, (255, 255, 255))
        textrect = textobj.get_rect()
        textrect.center = temprect.center
        self.maze.screen.blit(textobj, textrect)
        tempscreen = pg.transform.scale2x(self.maze.screen)
        # pg.transform.scale(self.maze.screen, (800, 800))
        self.maze.surface.blit(tempscreen, (50, 50))
        pg.display.update()
        self.audio.playing = True
        self.audio.play_sound('gamestart')
        pg.time.delay(4500)

    def animate(self):
        self.surface.fill((0, 0, 0))
        # for i in range(len(self.maze.pointimages)):
        #     self.surface.blit(self.maze.pointimages[i], pg.Rect(20*i, 0, 20, 20))
        # pg.display.update()
        # pg.time.delay(10000)
        Animator.drawtext(self, "Character / Nickname", x=400, y=0)
        pg.display.update()
        if self.animating:
            Animator.showghost(self, "blinky", 200, 50)
            Animator.showghost(self, "pinky", 200, 150)
            Animator.showghost(self, "inky", 200, 250)
            Animator.showghost(self, "clyde", 200, 350)
        # animating = True
        for i in range(125):
            if self.animating:
                if self.audio.background_src is not 'power_pellet.ogg':
                    if i % 2 == 0 and not pg.mixer.get_busy():
                        self.audio.play_sound("munch_1")
                    elif i % 2 == 1 and not pg.mixer.get_busy:
                        self.audio.play_sound("munch_2")
                for event in pg.event.get():
                    if event.type == pg.QUIT:
                        sys.exit()
                    if event.type == pg.KEYDOWN:
                        if event.key == pg.K_ESCAPE:
                            sys.exit()
                        if event.key == pg.K_SPACE:
                            self.animating = False
                pg.time.delay(100)
                self.pacman.surface.fill((0, 0, 0))
                self.pacman.update()
                self.pacman.draw()
                temp = pg.sprite.spritecollideany(sprite=self.pacman, group=self.tempghosts)
                if temp:
                    self.tempghosts.remove(temp)
                    self.audio.play_sound("eat_ghost")
                    self.pacman.surface.blit(self.pointimages[self.counter], temp.rect)
                    self.counter += 1
                    self.tempghosts.draw(self.pacman.surface)
                    self.surface.blit(self.pacman.surface, (0, 450))
                    pg.display.update()
                    pg.time.delay(200)
                self.tempghosts.update()
                self.tempghosts.draw(self.pacman.surface)
                self.powerpellets.update()
                self.powerpellets.draw(self.pacman.surface)
                if pg.sprite.spritecollide(sprite=self.pacman, group=self.powerpellets, dokill=True):
                    self.audio.background_src = 'power_pellet.ogg'  # self.sounds[0]['eatpowerpellet']
                    self.audio.playing = False
                    self.audio.toggle()
                    self.pacman.velocity = Vector(4, 0)
                    self.pacman.direction = 'right'
                    self.blinky.changedirection('right')
                    self.blinky.changestatus('vulnerable')
                    self.clyde.changedirection('right')
                    self.clyde.changestatus('vulnerable')
                    self.inky.changedirection('right')
                    self.inky.changestatus('vulnerable')
                    self.pinky.changedirection('right')
                    self.pinky.changestatus('vulnerable')
                self.surface.blit(self.pacman.surface, (0, 450))
                pg.display.update()
        self.audio.toggle()
        pg.time.delay(1000)
        self.surface.fill((0, 0, 0))
        pg.display.update()
        pg.time.delay(1000)
        self.menu()


def main():
    maze = Maze(game=0, score=0)
    animator = Animator(maze)
    animator.animate()
    maze.update()


if __name__ == '__main__':
    main()
