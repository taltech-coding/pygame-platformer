import pygame

from lib.body import Body
from lib.player import Player

GRID_SIZE = 16


class CollisionBox(pygame.sprite.Sprite):
    TEXTURE = pygame.image.load("assets/sprites/wall.png")

    def __init__(self, position):
        super().__init__()

        self.image = self.TEXTURE
        self.rect = self.image.get_rect().move(*position)
        self.position = pygame.Vector2(*position)

    def touch(self, _body: Body):
        pass


class FinishFlag(CollisionBox):
    TEXTURE = pygame.image.load("assets/sprites/finish.png")

    def touch(self, body: Body):
        if isinstance(body, Player):
            print('Game finished, hurray!')  # Todo implement game completed scene transition


class Spikes(CollisionBox):
    TEXTURE = pygame.image.load("assets/sprites/spikes.png")

    def touch(self, body: Body):
        body.kill()



