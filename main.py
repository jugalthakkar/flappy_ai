from player import Player
from difficulty import Difficulty


if __name__ == "__main__":
    player = Player(Difficulty.MEDIUM)
    player.start()