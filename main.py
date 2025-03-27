import json
import sys
import time
from os.path import basename

from src.sokoban import Sokoban, heuristica_euclidean, heuristica_manhattan
from src.visualizer import SokobanVisualizer


def main():
    if len(sys.argv) < 3:
        print("Uso: python main.py <archivo> <algoritmo> [heurística]")
        sys.exit()

    file = sys.argv[1]
    algo = sys.argv[2]
    heuristic = sys.argv[3].lower() if len(sys.argv) >= 4 else None

    sokoban = Sokoban(file)

    print(f"Ejecutando algoritmo: {algo}")
    start_time = time.time()

    if algo == "bfs":
        solution = sokoban.bfs()
    elif algo == "dfs":
        solution = sokoban.dfs()
    elif algo in {"greedy", "astar"}:
        if heuristic is None:
            print("Debe especificar una heurística para usar con greedy o astar.")
            print("Ejemplo: python main.py nivel_1.txt greedy manhattan")
            sys.exit(1)

        if heuristic == "manhattan":
            heuristic_fn = heuristica_manhattan
        elif heuristic == "euclidean":
            heuristic_fn = heuristica_euclidean
        else:
            raise ValueError("Heurística no válida")

        use_astar = algo == "astar"
        solution = sokoban.informed_search(heuristic_fn, use_astar)

    else:
        raise ValueError("Algoritmo no válido")

    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
    print(f"Total de pasos: {solution.get("steps")}")
    print(f"Nodos expandidos: {solution.get("expanded_nodes")}")
    print(f"Nodos frontera: {solution.get("frontier_nodes")}")

    with open(f"{basename(file)}_{algo}_{heuristic}.json", "w") as f:
        json.dump(solution, f, indent=2)

    visualizer = SokobanVisualizer(solution)
    visualizer.play_solution()


if __name__ == "__main__":
    main()
