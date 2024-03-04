import sys
import uuid
import pygame
from config import WINDOW_WIDTH, WINDOW_HEIGHT
from level import Level
from title import Title
from client.game_client import TCPClientThread


class Game:
    def __init__(self) -> None:
        pygame.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("PyCombat")
        self.clock = pygame.time.Clock()
        self.level = None
        self.title = Title()
        self.game_state = "title"
        self.client = TCPClientThread()
        self.client.start()
        self.client_name = str(uuid.uuid4())
        self.lobby_name = "mylobby"

    def run(self) -> None:
        running = True
        while running:
            dt = self.clock.tick() / 1000
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            if self.game_state == "title":
                self.title.update(event, self.change_state)
            elif self.game_state == "playing":
                self.level.update(dt)
            pygame.display.flip()
        self.client.stop()
        self.client.join()
        pygame.quit()
        sys.exit()

    def change_state(self, state: str) -> None:
        self.game_state = state
        if state == "vs_computer":
            self.level = Level(self.client, vs_computer=True)
            self.game_state = "playing"
        elif state == "vs_human":
            self.client.send_message(f"join {self.lobby_name} {self.client_name}")
            self.level = Level(
                self.client,
                lobby_name=self.lobby_name,
                username=self.client_name,
                vs_computer=False,
                vs_network=True,
            )
            self.game_state = "playing"


if __name__ == "__main__":
    game = Game()
    game.run()
