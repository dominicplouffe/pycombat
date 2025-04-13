import pygame


class PowerUpChoices:
    BULLET = "bullet"
    PATH = "path"
    PATH_PLUS = "path"
    ICE = "ice"
    ICE_PLUS = "ice_plus"


class PowerUps:
    def __init__(self) -> None:
        self.timer_power_ups = []

    def add_path_power_up(self) -> None:
        self.timer_power_ups.append(
            {
                "type": PowerUpChoices.PATH,
                "timer": pygame.time.get_ticks() + 10000,
                "cost": 5,
                "active": False,
            }
        )

    def add_path_plus_power_up(self) -> None:
        self.timer_power_ups.append(
            {
                "type": PowerUpChoices.PATH_PLUS,
                "timer": pygame.time.get_ticks() + 100000,
                "cost": 15,
            }
        )

    def add_ice_power_up(self) -> None:
        self.timer_power_ups.append(
            {
                "type": PowerUpChoices.ICE,
                "timer": pygame.time.get_ticks() + 10000,
                "cost": 5,
            }
        )

    def add_ice_plus_power_up(self) -> None:
        self.timer_power_ups.append(
            {
                "type": PowerUpChoices.ICE_PLUS,
                "timer": pygame.time.get_ticks() + 100000,
                "cost": 15,
            }
        )

    def has_power_up(self, power_up_type: PowerUpChoices) -> bool:
        for power_up in self.timer_power_ups:
            if power_up["type"] == power_up_type:
                return True
        return False

    def remove_power_up(self, power_up_type: PowerUpChoices) -> None:
        for power_up in self.timer_power_ups:
            if power_up["type"] == power_up_type:
                self.power_ups.remove(power_up)
                break

    def clear_power_ups(self) -> None:
        self.timer_power_ups = []

    def update(self) -> None:
        for power_up in self.timer_power_ups:
            if power_up["timer"] < pygame.time.get_ticks():
                self.timer_power_ups.remove(power_up)
                break
