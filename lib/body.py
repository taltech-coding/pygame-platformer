import pygame

LEFT, RIGHT = -1, 1
GRAVITY = 200
FALL_ACCELERATION = 2.5


class Body(pygame.sprite.Sprite):
    TEXTURE = None  # Placeholder, define a texture for the body!

    def __init__(self,
                 collision_layer: pygame.sprite.Group,
                 initial_position=(0, 0),
                 initial_facing_direction=RIGHT):
        super().__init__()

        self.image = self.TEXTURE
        self.rect = self.image.get_rect()
        self.camera_offset = pygame.Vector2(0, 0)

        self.collision_layer = collision_layer

        self.position = pygame.Vector2(*initial_position)
        self.velocity = pygame.Vector2(0, 0)
        self.rect.x, self.rect.y = self.position

        self.is_on_floor = False

        self.__facing_direction = None  # Simplify FD logic
        self.facing_direction = initial_facing_direction

    @property
    def facing_direction(self) -> LEFT | RIGHT:
        return self.__facing_direction

    @facing_direction.setter
    def facing_direction(self, direction: LEFT | RIGHT):
        self.image = pygame.transform.flip(self.TEXTURE, direction != RIGHT, False)
        self.__facing_direction = direction

    def update(self, delta, camera_offset):
        self.velocity = pygame.Vector2(self.get_velocity_x(delta), self.get_velocity_y(delta))
        self.camera_offset = camera_offset
        self.move_and_collide(delta)

    def get_velocity_x(self, _delta) -> float:
        return 0

    def get_velocity_y(self, delta) -> float:
        return self.velocity.lerp(pygame.Vector2(0, GRAVITY),
                                  FALL_ACCELERATION * delta).y  # todo acceleration by delta time

    def move_and_collide(self, delta):
        movement = self.handle_collisions(self.velocity * delta)

        self.position += movement
        self.rect.x, self.rect.y = self.position + self.camera_offset

    def handle_collisions(self, movement: pygame.Vector2):
        colliders = self.collision_layer.sprites()

        my_rect_x = pygame.Rect(self.position + pygame.Vector2(movement.x, 0), self.rect.size)

        collider_id = my_rect_x.collidelist(colliders)
        if collider_id != -1:
            self.velocity.x = 0
            movement.x = 0
            colliders[collider_id].touch(self)

        my_rect_y = pygame.Rect(self.position + pygame.Vector2(0, movement.y), self.rect.size)
        collider_id = my_rect_y.collidelist(colliders)

        self.is_on_floor = collider_id != -1 and movement.y > 0  # simplify

        if collider_id != -1:
            self.velocity.y = 0
            movement.y = 0
            colliders[collider_id].touch(self)

        return movement
