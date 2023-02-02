import pygame

from lib.body import Body
from lib.player import Player

MOVEMENT_SPEED = 100
MOVEMENT_ACCELERATION = 2


class Monster(Body):
    TEXTURE = pygame.image.load("assets/sprites/monster.png")

    def __init__(self, collision_layer: pygame.sprite.Group, target: Body, initial_position):
        super().__init__(collision_layer, initial_position)
        self.target = target

    def get_velocity_x(self, delta) -> float:
        return self.velocity.lerp(pygame.Vector2(MOVEMENT_SPEED * self.facing_direction, 0),
                                  MOVEMENT_ACCELERATION * delta).x

    def handle_collisions(self, movement: pygame.Vector2):
        collided_movement = super().handle_collisions(movement.copy())

        if self.rect.colliderect(self.target.rect):
            self.target.kill()

        if collided_movement.x == 0 != movement.x:  # Was moving horizontal and stopped, means we hit a wall
            self.facing_direction *= -1

        return collided_movement
