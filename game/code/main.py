import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from level import Level


class Game():
    def __init__(self):
        pygame.init()
        self.display_surface = pygame.display.set_mode(
            (WINDOW_WIDTH, WINDOW_HEIGHT)
        )
        pygame.display.set_caption('PyCombat')
        self.clock = pygame.time.Clock()
        self.level = Level()

    def run(self):
        running = True
        while running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            self.level.update(dt)
            pygame.display.flip()
        pygame.quit()


if __name__ == '__main__':
    game = Game()
    game.run()
