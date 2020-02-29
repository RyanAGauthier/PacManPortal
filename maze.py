import pygame as pg
import sys

NODESIZE = 24


def gimmesprite(rect, spritesheet, xdesired, ydesired):
    # INPUTS: Rectangle representing desired coordinates and dimensions of image on spritesheet,
    # the pygame image representing the spritesheet itself, and the x and y size the image should be scaled to
    # OUTPUTS: A pygame image that is a subsection of the spritesheet. You'll need ot edit its rectangle to get it
    # to draw on a different portion of the screen
    myrect = rect#pg.Rect((457, 65, 14, 14))
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
    # now all it knows how to do is draw itself, using a colored in rectangle if no image is supplied
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


class Maze:
    # This class actually plays the game, but its arguments are unusued currently.
    def __init__(self, game, pacman, ghosts, score):
        pg.init()
        self.screen = pg.display.set_mode((1200, 800))
        self.image = pg.Surface((800, 800))
        self.spritesheet = pg.image.load("spritesheet.png")
        self.frame = 3
        self.rect = (0, 0, 800, 800)
        self.game = game
        self.pacman = pacman
        self.ghosts = ghosts
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
                                                  rect=temprect, color=(0, 0, 225), image=False, traversable=False))
                    # {"rect": pg.Rect(i * NODESIZE, j * NODESIZE, NODESIZE, NODESIZE),
                    #                          "color": (0, 0, 255), "image": False, "traversable": False})
                elif self.currentline[i] == "O":
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE,
                                                  rect=temprect, color=(0, 255, 0), image=False, traversable=True))
                    # {"rect": pg.Rect(i * NODESIZE, j * NODESIZE, NODESIZE, NODESIZE),
                    #                       "color": (0, 255, 0), "image": False, "traversable": True})
                elif self.currentline[i] == "P":
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE,
                                                  rect=temprect, color=(255, 255, 225), image=False, traversable=True))
                    # {"rect": pg.Rect(i * NODESIZE, j * NODESIZE, NODESIZE, NODESIZE),
                    #                       "color": (255, 255, 255), "image": False, "traversable": True})
                elif self.currentline[i] == "E":
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE,
                                                  rect=temprect, color=(0, 0, 0), image=False, traversable=True))
                    # {"rect": pg.Rect(i * NODESIZE, j * NODESIZE, NODESIZE, NODESIZE),
                    #                       "color": (0, 0, 0), "image": False, "traversable": True})
                elif self.currentline[i] == "G":
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE,
                                                  rect=temprect, color=(255, 0, 0), image=False, traversable=True))
                    # {"rect": pg.Rect(i * NODESIZE, j * NODESIZE, NODESIZE, NODESIZE),
                    #                       "color": (255, 0, 0), "image": False, "traversable": True})
                elif self.currentline[i] == "1":
                    ghost1 = gimmesprite(rect=pg.Rect(457, 65, 14, 14), spritesheet=self.spritesheet,
                                xdesired=NODESIZE, ydesired=NODESIZE)
                    self.currentnodes.append(Node(surface=self.screen, nodesize=NODESIZE, rect=temprect,
                                                  color=(0, 0, 0), image=ghost1, traversable=False))
            self.nodes[j] = self.currentnodes
            # the nodes are written in row, column format due to being taken in as a row of characters by f.read
            # as a result of this, the node at [row][column] is located at position [y][x]
        print(self.nodes[0][25]) #Just checking something
        self.f.close()
        self.myleft = 13
        self.mytop = 23
        self.tempacman = {"color": (255, 255, 0), "rect": (self.myleft * NODESIZE, self.mytop * NODESIZE,
                                                           NODESIZE, NODESIZE)}
        # for j in range(len(self.nodes)):

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
                        if self.nodes[self.mytop - 1][self.myleft].traversable:
                            self.mytop -= 1
                    elif event.key == pg.K_a or event.key == pg.K_LEFT:
                        if self.nodes[self.mytop][self.myleft - 1].traversable:
                            self.myleft -= 1
                    elif event.key == pg.K_s or event.key == pg.K_DOWN:
                        if self.nodes[self.mytop + 1][self.myleft].traversable:
                            self.mytop += 1
                    elif event.key == pg.K_d or event.key == pg.K_RIGHT:
                        if self.nodes[self.mytop][self.myleft + 1].traversable:
                            self.myleft += 1
            for j in range(len(self.nodes)):
                for node in self.nodes[j]:
                    node.draw()
            self.nodes[self.mytop][self.myleft].color = (255, 255, 255)
            pg.draw.rect(self.screen, self.tempacman.get("color"), (self.myleft * NODESIZE, self.mytop * NODESIZE,
                                                                    NODESIZE, NODESIZE))
            tempghost1 = pg.Rect((457, 65, 14, 14))
            tempghost2 = pg.Rect((457, 81, 14, 14))
            if self.frame == 3:
                tempghost1 = pg.Rect((457, 65, 14, 14))
                tempghost2 = pg.Rect((457, 81, 14, 14))
                self.frame = 4
            elif self.frame == 4:
                tempghost1 = pg.Rect((473, 65, 14, 14))
                tempghost2 = pg.Rect((473, 81, 14, 14))
                self.frame = 3
            image1 = gimmesprite(rect=tempghost1, spritesheet=self.spritesheet, xdesired=14, ydesired=14)
            image1.blit(self.spritesheet, (0, 0), tempghost1)
            image1 = pg.transform.scale(image1, (14*3, 14*3))
            self.screen.blit(image1, (800, 0))
            image2 = pg.Surface(tempghost2.size)
            image2.blit(self.spritesheet, (0, 0), tempghost2)
            image2 = pg.transform.scale(image2, (14 * 3, 14 * 3))
            self.screen.blit(image2, (800, 80))
            pg.display.update()
            print("running")
            pg.time.delay(200)



def main():
    maze = Maze(0, 0, 0, 0)
    maze.update()


if __name__ == '__main__':
    main()
