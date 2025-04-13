from power_ups import PowerUps
import pickle


class PlayerStats:
    def __init__(self) -> None:
        self.coins = 0
        self.bullets = 3
        self.path = 3
        self.power_ups = PowerUps()

    def add_coins(self, amount: int) -> None:
        self.coins += amount
        save_player_stats(self)

    def add_bullets(self, amount: int) -> None:
        self.bullets += amount
        save_player_stats(self)

    def remove_bullets(self, amount: int) -> None:
        self.bullets -= amount
        if self.bullets < 0:
            self.bullets = 0
        save_player_stats(self)

    def add_path(self, amount: int) -> None:
        self.path += amount
        save_player_stats(self)

    def remove_path(self, amount: int) -> None:
        self.path -= amount
        if self.path < 0:
            self.path = 0
        save_player_stats(self)


def save_player_stats(player_stats: PlayerStats) -> None:
    with open("player_stats.pkl", "wb") as f:
        pickle.dump(player_stats, f)


def load_player_stats() -> PlayerStats:
    ps = PlayerStats()
    try:
        with open("player_stats.pkl", "rb") as f:
            loaded_stats = pickle.load(f)
            ps.coins = loaded_stats.coins
            ps.bullets = loaded_stats.bullets
            ps.path = loaded_stats.path
            return ps
    except FileNotFoundError:
        return ps
