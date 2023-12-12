import pygame
import sys
import random
import itertools

# Define constants
WIDTH, HEIGHT = 800, 600
PLAYER_SPEED = 3
GAME_SPEED = 60 #fps

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class EffectObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)

        self.setTypeThenSpawn()

    def spawn(self):
        # Generate random position for the teleportation object
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)

    def setTypeThenSpawn(self):
        # set the type randomly
        self.type = random.choice(["buff", "debuff"])
        if self.type == "buff":
            self.image.fill("Blue")
            self.rect = self.image.get_rect()
        else:
            self.image.fill("Red")
            self.rect = self.image.get_rect()

        self.spawn()

class TeleportationObject(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()

        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)
        self.image.fill((0, 0, 0, 0))  # Fully transparent surface
        self.rect = self.image.get_rect()
        self.spawn()

    def spawn(self):
        # Generate random position for the teleportation object
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)

class Player(pygame.sprite.Sprite):
    # keys {left, right, up, down}
    def __init__(self, image_path, x, y, keys, angle = 0):
        super().__init__()
        # use pygame.transform.scale in self.image to resize the player
        self.image = pygame.image.load(f"{image_path}/body.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.keys = keys
        self.rotation_angle = angle # Initial rotation angle

        # Initial player speed
        self.speed = PLAYER_SPEED

        # Added attributes for buff/debuff effect
        self.effect_timer = 0
        self.original_speed = PLAYER_SPEED


    def update(self, keys):
        target_rotation_angle = None

        if keys[self.keys["left"]]:
            self.rect.x -= self.speed
            # self.rotate(180)
            target_rotation_angle = 180

        if keys[self.keys["right"]]:
            self.rect.x += self.speed
            target_rotation_angle = 0
 
        if keys[self.keys["up"]]:
            self.rect.y -= self.speed
            target_rotation_angle = 90

        if keys[self.keys["down"]]:
            self.rect.y += self.speed
            target_rotation_angle = -90

        if target_rotation_angle is not None:
            self.rotate(target_rotation_angle)

        # Ensure the player stays within the screen boundaries
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

        # Check if the player is currently under the effect of buff/debuff
        if self.effect_timer > 0:
            self.effect_timer -= 1
            if self.effect_timer == 0:
                # Revert the effect after the timer expires
                self.speed = self.original_speed


    def rotate(self, target_angle):
        angle_diff = target_angle - self.rotation_angle
        self.image = pygame.transform.rotate(self.image, angle_diff)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rotation_angle = target_angle

    def teleport(self):
        # Teleport the player to a random position on the screen
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)

    def applyEffect(self, type):
        if type == "debuff":
            self.speed = self.speed / 2
        else:
            self.speed = self.speed * 2

            
        # Set the timer for the effect duration (2 seconds)
        self.effect_timer = 2 * GAME_SPEED

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2 Player Tag Game")
        self.clock = pygame.time.Clock()
        self.running = True

        # Create players
        self.player1 = Player("graphics/player-1", 100, 100, {"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s })
        self.player2 = Player("graphics/player-2", 700, 500, {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN }, -180)

        # Create teleportation objects
        self.teleportation_objects = pygame.sprite.Group()
        for i in range(5):
            self.teleportation_objects.add(TeleportationObject())

        # Create effect objects
        self.effect_objects = pygame.sprite.Group(EffectObject(), EffectObject())

        # Create sprite groups
        self.all_sprites = pygame.sprite.Group(self.player1, self.player2, self.teleportation_objects, self.effect_objects)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

        # Check for collisions between players and teleportation objects
        for player, teleportation_object, effect_object in itertools.product([self.player1, self.player2], self.teleportation_objects, self.effect_objects):
            if pygame.sprite.collide_rect(player, teleportation_object):
                player.teleport()
                teleportation_object.spawn()

            if pygame.sprite.collide_rect(player, effect_object):
                player = random.choice([self.player1, self.player2])
                player.applyEffect(effect_object.type)
                effect_object.spawn()

            
    def run(self):
        while self.running:
            self.handle_events()

            # Get keys pressed
            keys = pygame.key.get_pressed()

            # Update player positions
            self.all_sprites.update(keys)

            # Check for collision between players
            if pygame.sprite.collide_rect(self.player1, self.player2):
                print("Player 1 caught Player 2! Game Over.")
                self.running = False

            # Draw everything
            self.screen.fill(WHITE)
            self.all_sprites.draw(self.screen)
            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(GAME_SPEED)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
