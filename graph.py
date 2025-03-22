import pygame as pg

from src.sokoban import Sokoban, movimientos

bg = (255, 255, 255)
wall = (0, 0, 0)
player = (0, 255, 0)
box = (0, 0, 255)
target = (255, 0, 0)
box_target = (255, 255, 0)


class SokobanVisualizer(Sokoban):
    def __init__(self, filename):
        super().__init__(filename)

        pg.init()
        self.screen = pg.display.set_mode((600, 600))
        self.clock = pg.time.Clock()

    def apply_move(self, move):
        """Apply a move to update player and boxes."""
        dx, dy = movimientos[move]
        new_player = (self.player[0] + dx, self.player[1] + dy)

        if new_player in self.boxes:
            new_box = (new_player[0] + dx, new_player[1] + dy)
            self.boxes.remove(new_player)
            self.boxes.add(new_box)

        self.player = new_player

    def print_map(self):
        """Prints the current state of the map."""
        self.screen.fill(bg)
        height_size = 600 // len(self.map)
        width_size = 600 // len(self.map[0])

        for y, row in enumerate(self.map):
            for x, cell in enumerate(row):
                pos = (x, y)
                rect = pg.Rect(x * width_size, y * height_size, width_size, height_size)
                if pos == self.player:
                    pg.draw.rect(self.screen, player, rect)
                elif pos in self.boxes:
                    if pos in self.targets:
                        pg.draw.rect(self.screen, box_target, rect)
                    else:
                        pg.draw.rect(self.screen, box, rect)
                elif pos in self.targets:
                    pg.draw.rect(self.screen, target, rect)
                elif cell == "#":
                    pg.draw.rect(self.screen, wall, rect)

        pg.display.flip()

    def play_solution(self, solution):
        """Play the solution step by step."""
        self.print_map()
        for move in solution:
            self.clock.tick(5)
            self.apply_move(move)
            self.print_map()


# Example usage
filename = "levels/lvl8.txt"
game = SokobanVisualizer(filename)
solution = game.search_tree()
print("Total de pasos: ", len(solution))
print("Solución: ", " ".join(solution))
game.play_solution(solution)
