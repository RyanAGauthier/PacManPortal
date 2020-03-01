import pygame as pg

# Rects of all necessary sprites in the sprite sheet
spriteDict = {
    'pacman': {
        'up': {
            0: pg.Rect((489, 0, 14, 14)),
            1: pg.Rect((457, 32, 14, 14)),
            2: pg.Rect((473, 32, 14, 14))
        },
        'down': {
            0: pg.Rect((489, 0, 14, 14)),
            1: pg.Rect((457, 48, 14, 14)),
            2: pg.Rect((473, 48, 14, 14))
        },
        'left': {
            0: pg.Rect((489, 0, 14, 14)),
            1: pg.Rect((457, 16, 14, 14)),
            2: pg.Rect((473, 16, 14, 14))
        },
        'right': {
            0: pg.Rect((489, 0, 14, 14)),
            1: pg.Rect((457, 0, 14, 14)),
            2: pg.Rect((473, 0, 14, 14))
        }
    },
}

mazetiles = pg.Rect((226, 0, 216, 248))

# Class has the spritesheet
class SpriteManager:
    def __init__(self):
        self.spritesheet = pg.image.load("resources/spritesheet.png")

    # Returns requested sprite, with given dimensions
    def get_sprite(self, sprite_name, index, xdesired=(14*3), ydesired=(14*3)):
        # INPUTS: Rectangle representing desired coordinates and dimensions of image on spritesheet,
        # the pygame image representing the spritesheet itself, and the x and y size the image should be scaled to
        # OUTPUTS: A pygame image that is a subsection of the spritesheet. You'll need ot edit its rectangle to get it
        # to draw on a different portion of the screen
        myrect = rect#pg.Rect((457, 65, 14, 14))
        myxdesired = xdesired
        myydesired = ydesired
        image = pg.Surface(myrect.size)
        # this is to generate the surface that the formatted image will live in
        image.blit(self.spritesheet, (0, 0), spriteDict[sprite_name][index])  # this jams the given first argument onto the newly created surface
        image = pg.transform.scale(image, (myxdesired, myydesired))
        return image


