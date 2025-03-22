import os
import time

from src.sokoban import Chars, Sokoban, movimientos


class SokobanVisualizer(Sokoban):
    def __init__(self, filename):
        super().__init__(filename)

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
        os.system("clear")  # Clear terminal on Unix/Linux/macOS
        # os.system("cls")  # Uncomment this for Windows

        for y, row in enumerate(self.map):
            line = ""
            for x, cell in enumerate(row):
                pos = (x, y)
                if pos == self.player:
                    line += Chars.PLAYER.value
                elif pos in self.boxes:
                    if pos in self.targets:
                        line += Chars.BOX_ON_TARGET.value
                    else:
                        line += Chars.BOX.value
                elif pos in self.targets:
                    line += Chars.TARGET.value
                else:
                    line += cell.value
            print(line)
        print("\n")

    def play_solution(self, solution):
        """Play the solution step by step."""
        self.print_map()
        for move in solution:
            time.sleep(0.2)  # Delay for animation effect
            self.apply_move(move)
            self.print_map()


# Example usage
filename = "levels/lvl1.txt"
game = SokobanVisualizer(filename)
solution = game.search_tree()
print("Total de pasos: ", len(solution))
print("Solución: ", " ".join(solution))
input()
game.play_solution(solution)
