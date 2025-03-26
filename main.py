import json
import sys
import time

from src.sokoban import heuristica_euclidean, heuristica_manhattan
from src.visualizer import SokobanVisualizer


def main():
    if len(sys.argv) < 3:
        print("Uso: python main.py <archivo> <algoritmo> [heurística]")
        sys.exit()

    file = sys.argv[1]
    algo = sys.argv[2]
    heuristic = sys.argv[3].lower() if len(sys.argv) >= 4 else None

    game = SokobanVisualizer(file)

    print(f"Ejecutando algoritmo: {algo}")
    start_time = time.time()

    if algo == "bfs":
        solution = game.bfs()
    elif algo == "dfs":
        solution = game.dfs()
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
        solution = game.informed_search(heuristic_fn, use_astar)

    else:
        raise ValueError("Algoritmo no válido")

    end_time = time.time()
    execution_time = end_time - start_time

    print(f"Tiempo de ejecución: {execution_time:.4f} segundos")
    print(f"Total de pasos: {len(solution)}")
    print(f"Solución: {json.dumps(solution, indent=2)}")

    game.play_solution(solution)


if __name__ == "__main__":
    main()
