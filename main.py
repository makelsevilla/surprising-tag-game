import pygame
import sys

# Define constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 20
PLAYER_SPEED = 5

# Define colors
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Player(pygame.sprite.Sprite):
    # keys [left, right, up, down]
    def __init__(self, color, x, y, keys):
        super().__init__()
        self.image = pygame.Surface((PLAYER_SIZE, PLAYER_SIZE))
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.keys = keys

    def update(self, keys):
        if keys[self.keys[0]]:
            self.rect.x -= PLAYER_SPEED
        if keys[self.keys[1]]:
            self.rect.x += PLAYER_SPEED
        if keys[self.keys[2]]:
            self.rect.y -= PLAYER_SPEED
        if keys[self.keys[3]]:
            self.rect.y += PLAYER_SPEED

        # Ensure the player stays within the screen boundaries
        self.rect.x = max(0, min(self.rect.x, WIDTH - PLAYER_SIZE))
        self.rect.y = max(0, min(self.rect.y, HEIGHT - PLAYER_SIZE))

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2 Player Tag Game")
        self.clock = pygame.time.Clock()
        self.running = True

        # Create players
        self.player1 = Player(RED, 100, 100, [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s])
        self.player2 = Player(BLUE, 700, 500, [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN])

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
            self.clock.tick(40)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()
