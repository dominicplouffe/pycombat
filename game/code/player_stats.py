from power_ups import PowerUps


class PlayerStats:
    def __init__(self) -> None:
        self.coins = 0
        self.power_ups = PowerUps()

    def add_coins(self, amount: int) -> None:
        self.coins += amount
