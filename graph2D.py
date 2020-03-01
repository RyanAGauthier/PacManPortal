from settings import Settings
import pygame


class Node2D:
    def __init__(self, data, x=0, y=0):
        self.coor = (x, y)
        self.data = data
        self.connected = []


class Edge:
    def __init__(self, nodea: Node2D, nodeb: Node2D):
        self.nodeA = nodea
        self.nodeB = nodeb


class Graph2D:
    def __init__(self, mazefile: str = None):
        self.settings = Settings()
        self.xNum = int(self.settings.screen_width / 20)
        self.yNum = int(self.settings.screen_height / 20)
        self.nodes = []
        self.edges = []

        if mazefile is not None:
            self.setTiles(mazefile)

    def setTiles(self, file: str):
        with open(file) as f:
            y = 0
            for line in f:
                line = line.strip('\n')
                for x in range(len(line)):
                    self.nodes.append(Node2D(line[x], x, y))
                y += 1



    def drawNodes(self, screen):
        for x in range(self.xNum):
            for y in range(self.yNum):
                pygame.draw.circle(screen, (0, 0, 0), (x*20 + 10, y*20 + 10), 4)

    def getPos(self, x, y):
        return (x*20 + 10, y*20 + 10)

    def getX(self, x):
        return x*20 + 10

    def getY(self, y):
        return y*20 + 10
