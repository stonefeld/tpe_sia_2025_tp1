import sys

from src.visualizer import SokobanVisualizer


def main():
    file = sys.argv[1]
    algo = sys.argv[2]

    game = SokobanVisualizer(file)
    if algo == "bfs":
        solution = game.bfs()
    # elif algo == "dfs":
    #     solution = game.dfs()
    # elif algo == "greedy":
    #     solution = game.greedy()
    # elif algo == "a_star":
    #     solution = game.a_star()
    else:
        raise ValueError("Algoritmo no válido")

    print("Total de pasos: ", len(solution))
    print("Solución: ", " ".join(solution))

    game.play_solution(solution)


if __name__ == "__main__":
    main()
