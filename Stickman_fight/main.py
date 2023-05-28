import pygame
import sys
from stickman import StickMan
from settings import Settings
from ground import Ground


class StickManFight:
    """Overall class to manage game assets and behaviour."""

    def __init__(self):
        """Initialize the game, and create game resources."""
        pygame.init()

        # Screen variables
        self.screen_height, self.screen_width = 720, 1200
        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        pygame.display.set_caption("StickMan Fight")

        # Instances
        self.stickman = StickMan()
        self.settings = Settings()

        # Sprites
        self.sprites = pygame.sprite.Group()
        self.sprites.add(self.stickman)
        self.platforms = pygame.sprite.Group()
        self.ground = Ground(0, self.screen_height-40, self.screen_width, 40)
        self.platforms.add(self.ground)
        self.sprites.add(self.ground)

        self.clock = pygame.time.Clock()

    def run_game(self):
        """The main loop of the game."""
        while True:
            self.clock.tick(self.settings.fps)
            self.check_events()
            self.stickman.update()
            self.check_collisions()
            self.stickman.check_key_downs()
            self.stickman.idle()

            self.update_screen()

    def check_events(self):
        """Keep track of pressed keys."""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not self.stickman.falling and not self.stickman.jumping:
                    self.stickman.jump()
            self.stickman.check_key_ups(event)

    def check_collisions(self):
        """Handle collisions between sprites"""
        ground_hit = pygame.sprite.spritecollide(self.stickman, self.platforms, False)
        if ground_hit:
            self.stickman.rect.bottom = ground_hit[0].rect.top + 7
            self.stickman.vel = 0
            self.stickman.falling = False
            self.stickman.standing = True

    def update_screen(self):
        self.screen.fill((230, 230, 230))
        self.sprites.draw(self.screen)

        pygame.display.flip()


if __name__ == '__main__':
    # Make a game instance, and run the game.
    ai = StickManFight()
    ai.run_game()
