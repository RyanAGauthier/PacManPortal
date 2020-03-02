import pygame as pg
import sys
from vector import Vector
NODESIZE = 8


class Ghost(pg.sprite.Sprite):
    # This is the class that represents the ghosts, there will be four individual instances in total
    # The class inherits from sprite so that we can later use sprite.groupcollide() between pacman and each ghost
    # Each ghost can draw and update itself, currently it just needs to implement the state parameter, which is intended
    # to tell the ghost whether it is fleeing, respawning, just eyeballs, etc
    def __init__(self, surface, images, rect, direction, state):
        pg.sprite.Sprite.__init__(self)
        self.surface = surface
        self.images = images
        self.currentframe = 0
        self.image = images[self.currentframe]
        self.rect = rect
        self.direction = direction
        self.state = state
        self.framecount = 11  # This dictates how many game frames should pass between different images
        self.frameclock = self.framecount

    def changedirection(self, newdirection):
        self.direction = newdirection
        if newdirection == "up":
            self.currentframe = 4
            self.image = self.images[self.currentframe]
        elif newdirection == "down":
            self.currentframe = 6
            self.image = self.images[self.currentframe]
        elif newdirection == "left":
            self.currentframe = 2
            self.image = self.images[self.currentframe]
        elif newdirection == "right":
            self.currentframe = 0
            self.image = self.images[self.currentframe]

    def changestate(self, newstate):
        self.state = newstate
        if self.state == "vulnerable":
            pass
        elif self.state == "dead":
            pass
        elif self.state == "shopping":
            pass
        elif self.state == "chasing":
            pass

    def draw(self):
        self.surface.blit(self.image, self.rect)

    def update(self):
        # This is the portion of the object that handles the animation, swapping between 3 and 4 legs at a rate decided
        # by self.framecount
        if self.frameclock == 1:
            if self.currentframe % 2 == 0:
                self.currentframe += 1
                self.image = self.images[self.currentframe]
            else:
                self.currentframe -= 1
                self.image = self.images[self.currentframe]
            self.frameclock = self.framecount
        else:
            self.frameclock -= 1
        #print("displaying frame {}".format(self.currentframe))


class Pacman(pg.sprite.Sprite):
    def __init__(self, surface, images, velocity, rect, selfnode, allnodes):
        pg.sprite.Sprite.__init__(self),
        self.surface = surface
        self.velocity = velocity
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

    def move(self):
        if self.velocity == Vector(-4, 0):
            self.targetnode = self.allnodes[self.selfnode[0]][self.selfnode[1] - 1]
            if self.targetnode.traversable or self.rect.centerx > self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx:
                self.rect.centerx += self.velocity.x
                if self.rect.centerx < self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx - 4:
                    self.selfnode = (self.selfnode[0], self.selfnode[1] - 1)
        elif self.velocity == Vector(4, 0):
            self.targetnode = self.allnodes[self.selfnode[0]][self.selfnode[1] + 1]
            if self.targetnode.traversable or self.rect.centerx < self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx:
                self.rect.centerx += self.velocity.x
                if self.rect.centerx > self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centerx + 4:
                    self.selfnode = (self.selfnode[0], self.selfnode[1] + 1)
        elif self.velocity == Vector(0, 4):
            self.targetnode = self.allnodes[self.selfnode[0]+1][self.selfnode[1]]
            if self.targetnode.traversable or self.rect.centery < self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery:
                self.rect.centery += self.velocity.y
                if self.rect.centery > self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery + 4:
                    self.selfnode = (self.selfnode[0] + 1, self.selfnode[1])
        elif self.velocity == Vector(0, -4):
            self.targetnode = self.allnodes[self.selfnode[0] - 1][self.selfnode[1]]
            if self.targetnode.traversable or self.rect.centery > self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery:
                self.rect.centery += self.velocity.y
                if self.rect.centery < self.allnodes[self.selfnode[0]][self.selfnode[1]].rect.centery - 4:
                    self.selfnode = (self.selfnode[0] - 1, self.selfnode[1])
        print("I'm at:")
        print(self.selfnode)
        print("I'm going to:")
        print(self.targetnode)
        print(self.targetnode.traversable)

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
        print("displaying frame {}".format(self.currentframe))

    def draw(self):
        self.surface.blit(self.image, self.rect)


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

    def __repr__(self):
        return "Node located at {}, {}. Colored {}. {}Traversable. ".format(self.rect.left, self.rect.top, self.color,
                                                                            "Non" if not self.traversable else "Is")

    def draw(self):
        if not self.image:
            pg.draw.rect(self.surface, self.color, self.rect)
        else:
            self.surface.blit(self.image, self.rect)


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
                                                  rect=temprect, color=(0, 255, 0), image=False, traversable=True))
                elif self.currentline[i] == "P":
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE,
                                                  rect=temprect, color=(255, 255, 225), image=False, traversable=True))
                elif self.currentline[i] == "E":
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE,
                                                  rect=temprect, color=(0, 0, 0), image=False, traversable=True))
                elif self.currentline[i] == "G":
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE,
                                                  rect=temprect, color=(255, 255, 255), image=False, traversable=True))
                elif self.currentline[i] == "1":
                    self.blinky = Ghost(surface=self.screen, images=self.ghostimages["blinky"], direction="up",
                                        rect=pg.Rect(i * NODESIZE - NODESIZE/2, j * NODESIZE - NODESIZE/2, 14, 14),
                                        state="fleeing")
                    # ghost1 = gimmesprite(rect=pg.Rect(457, 65, 14, 14), spritesheet=self.spritesheet,
                    #                      xdesired=NODESIZE, ydesired=NODESIZE)
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE, rect=temprect,
                                                  color=(0, 0, 0), image=False, traversable=True))
                elif self.currentline[i] == "2":
                    self.clyde = Ghost(surface=self.screen, images=self.ghostimages["clyde"], direction="up",
                                       rect=pg.Rect(temprect.left-15, temprect.top, 14, 14), state="fleeing")
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE, rect=temprect,
                                                  color=(0, 0, 0), image=False, traversable=True))
                elif self.currentline[i] == "3":
                    self.inky = Ghost(surface=self.screen, images=self.ghostimages["inky"], direction="up",
                                      rect=pg.Rect(temprect.left-7, temprect.top, 14, 14),
                                      state="fleeing")
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE, rect=temprect,
                                                  color=(0, 0, 0), image=False, traversable=True))
                elif self.currentline[i] == "4":
                    self.pinky = Ghost(surface=self.screen, images=self.ghostimages["pinky"], direction="up",
                                       rect=pg.Rect(temprect.left+2, temprect.top, 14, 14), state="fleeing")
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
        print(self.nodes[0][6].traversable)
        temptemprect = pg.Rect(0, 0, 12, 13)
        temptemprect.centerx = self.nodes[self.mytop][self.myleft].rect.centerx
        temptemprect.centery = self.nodes[self.mytop][self.myleft].rect.centery
        self.pacmannodes = self.nodes
        self.pacman = Pacman(surface=self.screen, images=self.pacmanimages, velocity=self.pacmanvelocity,
                             rect=pg.Rect(temptemprect.left, temptemprect.y, 13, 13),
                             selfnode=(self.mytop, self.myleft), allnodes=self.pacmannodes)
        self.ghosts.add(self.blinky, self.clyde, self.inky, self.pinky)
        self.tempacman = {"color": (255, 255, 0), "rect": (self.myleft * NODESIZE, self.mytop * NODESIZE,
                                                           NODESIZE, NODESIZE)}

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
                        self.pacman.velocity = self.pacmanspeed * Vector(0, -1)
                        # if self.nodes[self.mytop - 1][self.myleft].traversable:
                        #     self.mytop -= 1
                    elif event.key == pg.K_a or event.key == pg.K_LEFT:
                        self.pacman.velocity = self.pacmanspeed * Vector(-1, 0)
                        # if self.nodes[self.mytop][self.myleft - 1].traversable:
                        #     self.myleft -= 1
                    elif event.key == pg.K_s or event.key == pg.K_DOWN:
                        self.pacman.velocity = self.pacmanspeed * Vector(0, 1)
                        # if self.nodes[self.mytop + 1][self.myleft].traversable:
                        #     self.mytop += 1
                    elif event.key == pg.K_d or event.key == pg.K_RIGHT:
                        self.pacman.velocity = self.pacmanspeed * Vector(1, 0)
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


def main():
    maze = Maze(0, 0, 0, 0)
    maze.update()


if __name__ == '__main__':
    main()
