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
    def __init__(self, type = "debuff"):
        super().__init__()

        self.image = pygame.Surface((30, 30), pygame.SRCALPHA)

        self.type = type
        if type == "buff":
            self.image.fill("Blue")
        else:
            self.image.fill("Red")

        self.rect = self.image.get_rect()

        self.spawn()

    def spawn(self):
        # Generate random position for the teleportation object
        self.rect.x = random.randint(0, WIDTH - self.rect.width)
        self.rect.y = random.randint(0, HEIGHT - self.rect.height)

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
    def __init__(self, image_path, x, y, keys, angle = 0, name="Unknown"):
        super().__init__()
        # use pygame.transform.scale in self.image to resize the player
        self.image = pygame.image.load(f"{image_path}/body.png").convert_alpha()
        self.image = pygame.transform.rotate(self.image, angle)
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
        self.keys = keys
        self.rotation_angle = angle # Initial rotation angle
        self.name = name

        # Initial player speed
        self.speed = PLAYER_SPEED

        # Added attributes for buff/debuff effect
        self.effect_timer = 0
        self.original_speed = PLAYER_SPEED

        self.score = 0

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

    def increase_score(self):
        self.score += 1


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("2 Player Tag Game")
        self.clock = pygame.time.Clock()
        self.running = True

        # Create players
        player1_name = input("Enter player 1 name: ")
        player2_name = input("Enter player 2 name: ")
        self.player1 = Player("graphics/player-1", 100, 100, {"left": pygame.K_a, "right": pygame.K_d, "up": pygame.K_w, "down": pygame.K_s }, name=player1_name)
        self.player2 = Player("graphics/player-2", 700, 500, {"left": pygame.K_LEFT, "right": pygame.K_RIGHT, "up": pygame.K_UP, "down": pygame.K_DOWN }, -180, name=player2_name)

        # Create teleportation objects
        self.teleportation_objects = pygame.sprite.Group()
        for i in range(5):
            self.teleportation_objects.add(TeleportationObject())

        # Create effect objects
        self.effect_objects = pygame.sprite.Group(EffectObject("buff"), EffectObject("debuff"))

        # Create sprite groups
        self.all_sprites = pygame.sprite.Group(self.player1, self.player2, self.teleportation_objects, self.effect_objects)

        self.font = pygame.font.Font(None, 36)

        # Added attributes for game features
        self.rounds = 0
        self.current_round = 0
        self.it_player = None
        self.timer = 0
        self.max_rounds = 0
        self.round_winner = None

        # Initialize the game
        self.initialize_game()

    def initialize_game(self):
        # Get the number of rounds from the player
        self.max_rounds = int(input("Enter the number of rounds: "))

        # Set up the initial round
        self.setup_round()

    def setup_round(self):
        # Increment round count
        self.current_round += 1

        # Reset player positions
        self.player1.teleport()
        self.player2.teleport()

        # Randomly select the player who is "it" for this round
        self.it_player = self.player1 if self.player1 != self.it_player else self.player2

        # Set up the timer for this round
        self.timer = 30 * GAME_SPEED  # 30 seconds

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
                self.round_winner = self.it_player
                self.end_round()

            # Update the timer
            self.timer -= 1
            if self.timer == 0:
                # Time's up for this round
                self.round_winner = self.player1 if self.it_player != self.player1 else self.player2
                self.end_round()

            # Draw everything
            self.draw_background()
            self.all_sprites.draw(self.screen)

            # Draw scores and timer
            self.draw_scores()
            self.draw_timer()

            self.draw_current_it()

            pygame.display.flip()

            # Cap the frame rate
            self.clock.tick(GAME_SPEED)

        pygame.quit()
        sys.exit()

    def end_round(self):
        print(f"Round {self.current_round} Over!")

        if self.round_winner:
            print(f"{self.round_winner.name} wins the round!")

            # Update overall scores
            self.round_winner.increase_score()

            # Check if the game is over
            if self.current_round == self.max_rounds:
                print("Game Over!")
                if self.player1.score == self.player2.score:
                    print("It's a tie!")
                else:
                    game_winner = self.player1 if self.player1.score > self.player2.score else self.player2
                    print(f"{game_winner.name} wins the game!")

                self.running = False
            else:
                # Set up the next round
                self.setup_round()

    def draw_background(self):
        # Draw a green background
        self.screen.fill((0, 128, 0))  # Green color

        # Draw lines on the football field
        pygame.draw.rect(self.screen, WHITE, (50, 50, WIDTH - 100, HEIGHT - 100), 2)  # Outer boundary
        pygame.draw.line(self.screen, WHITE, (WIDTH // 2, 50), (WIDTH // 2, HEIGHT - 50), 2)  # Center line
        pygame.draw.circle(self.screen, WHITE, (WIDTH // 2, HEIGHT // 2), 100, 2)  # Center circle

    def draw_scores(self):
        # Display scores on the screen
        player1_score_text = self.font.render(f"{self.player1.name}: {self.player1.score}", True, WHITE)
        player2_score_text = self.font.render(f"{self.player2.name}: {self.player2.score}", True, WHITE)

        self.screen.blit(player1_score_text, (20, 20))
        self.screen.blit(player2_score_text, (WIDTH - player2_score_text.get_width() - 20, 20))

    def draw_timer(self):
        # Display the timer on the screen
        timer_text = self.font.render(f"Time: {self.timer // GAME_SPEED}", True, WHITE)
        self.screen.blit(timer_text, ((WIDTH - timer_text.get_width()) // 2, 20))

    def draw_current_it(self):
        current_it = self.font.render(f"It: {self.it_player.name}", True, WHITE)
        self.screen.blit(current_it, ((WIDTH - current_it.get_width()) // 2, HEIGHT - 40))


if __name__ == "__main__":
    game = Game()
    game.run()
