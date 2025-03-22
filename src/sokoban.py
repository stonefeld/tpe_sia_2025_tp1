from enum import Enum

movimientos = {
    "UP": (-1, 0),
    "DOWN": (1, 0),
    "LEFT": (0, -1),
    "RIGHT": (0, 1),
}


class Chars(str, Enum):
    WALL = "#"
    EMPTY = " "
    BOX = "$"
    TARGET = "."
    PLAYER = "@"
    BOX_ON_TARGET = "*"
    PLAYER_ON_TARGET = "+"


class Sokoban:
    def __init__(self, filename):
        self.map, self.player, self.boxes, self.targets = self.load_level(filename)

    def load_level(self, filename):
        map = []
        player = None
        boxes = set()
        targets = set()

        with open(filename, "r") as f:
            for y, line in enumerate(f):
                map.append([])

                for x, char in enumerate(line.rstrip("\n")):
                    if char == Chars.WALL.value:
                        map[y].append(Chars.WALL)
                    else:
                        map[y].append(Chars.EMPTY)
                        if char == Chars.PLAYER.value:
                            player = (x, y)
                        elif char == Chars.BOX.value:
                            boxes.add((x, y))
                        elif char == Chars.TARGET.value:
                            targets.add((x, y))

        return map, player, boxes, targets

