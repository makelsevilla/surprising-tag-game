import pygame
import sys

# Define constants
WIDTH, HEIGHT = 800, 600
# PLAYER_SIZE = 50 # Optional
PLAYER_SPEED = 5

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

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

    def update(self, keys):


        if keys[self.keys["left"]]:
            self.rect.x -= PLAYER_SPEED
            self.rotate(180)

        if keys[self.keys["right"]]:
            self.rect.x += PLAYER_SPEED
            self.rotate(0)
 
        if keys[self.keys["up"]]:
            self.rect.y -= PLAYER_SPEED
            self.rotate(90)

        if keys[self.keys["down"]]:
            self.rect.y += PLAYER_SPEED
            self.rotate(-90)

        # Ensure the player stays within the screen boundaries
        self.rect.x = max(0, min(self.rect.x, WIDTH - self.rect.width))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - self.rect.height))

    def rotate(self, target_angle):
        angle_diff = target_angle - self.rotation_angle

        self.image = pygame.transform.rotate(self.image, angle_diff)
        self.rect = self.image.get_rect(center=self.rect.center)
        self.rotation_angle = target_angle

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

        # Create sprite groups
        self.all_sprites = pygame.sprite.Group(self.player1, self.player2)

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False

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
            self.clock.tick(60)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
