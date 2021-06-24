import logging as log

class Profile:
    def __init__(self, player):
        self.player = player # Discord Member Object

    def set_data(self, player_name: str, type: str, amount: int):
        if type == 'xp':
