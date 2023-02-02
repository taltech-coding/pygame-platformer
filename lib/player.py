import pygame

from lib.body import Body, FALL_ACCELERATION, GRAVITY, RIGHT, LEFT

MOVEMENT_SPEED = 120
MOVEMENT_ACCELERATION = 5
JUMP_IMPULSE = 250


def get_user_input() -> pygame.Vector2:
    return pygame.Vector2(
        pygame.key.get_pressed()[pygame.K_d] - pygame.key.get_pressed()[pygame.K_a],
        pygame.key.get_pressed()[pygame.K_w] - pygame.key.get_pressed()[pygame.K_s]
    )


class Player(Body):
    TEXTURE = pygame.image.load("assets/sprites/player.png")

    def get_velocity_x(self, delta) -> float:
        user_input = get_user_input()

        return self.velocity.lerp(pygame.Vector2(MOVEMENT_SPEED * user_input.x, 0),
                                  MOVEMENT_ACCELERATION * delta).x  # TODO REFACTOR METHOD

    def get_velocity_y(self, delta) -> float:
        if self.is_on_floor and pygame.key.get_pressed()[pygame.K_SPACE]:
            self.is_on_floor = False
            return -JUMP_IMPULSE

        return self.velocity.lerp(pygame.Vector2(0, GRAVITY),
                                  FALL_ACCELERATION * delta).y  # TODO SEPRATE APPLY GRAVITY() METHOD

    def update(self, delta, camera_offset):
        super().update(delta, camera_offset)

        user_input = get_user_input()
        if user_input.x != 0:
            self.facing_direction = RIGHT if user_input.x > 0 else LEFT
