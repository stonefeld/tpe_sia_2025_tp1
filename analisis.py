import json
import time

import matplotlib.pyplot as plt
import numpy as np

from src.sokoban import Sokoban, heuristica_euclidean, heuristica_manhattan

def run_solver(file_path, algorithm, heuristic=None, runs=50):
    """Run the Sokoban solver multiple times and return execution times and solution lengths."""
    times = []
    solution_lengths = []
    expanded_nodes = []
    frontier_nodes = []

    for _ in range(runs):
        game = Sokoban(file_path)

        start_time = time.time()

        if algorithm == "bfs":
            solution = game.bfs()
        elif algorithm == "dfs":
            solution = game.dfs()
        elif algorithm in ["greedy", "astar"]:
            if heuristic == "manhattan":
                heuristic_fn = heuristica_manhattan
            elif heuristic == "euclidean":
                heuristic_fn = heuristica_euclidean
            else:
                raise ValueError("Invalid heuristic")

            use_astar = algorithm == "astar"
            solution = game.informed_search(heuristic_fn, use_astar)
        else:
            raise ValueError("Invalid algorithm")

        end_time = time.time()
        execution_time = end_time - start_time

        times.append(execution_time)
        solution_lengths.append(len(solution["path"]) if isinstance(solution, dict) else len(solution))
        expanded_nodes.append(solution.get("expanded_nodes", 0))
        frontier_nodes.append(solution.get("frontier_nodes", 0))

    return {
        "times": times,
        "lengths": solution_lengths,
        "avg_time": np.mean(times),
        "std_time": np.std(times),
        "avg_length": np.mean(solution_lengths),
        "std_length": np.std(solution_lengths),
        "avg_expanded": np.mean(expanded_nodes),
        "avg_frontier": np.mean(frontier_nodes),
    }

def plot_results(results, metric="time"):
    """Plot results for the given metric with standard deviation if available."""
    levels = list(results.keys())
    algorithms = list(results[levels[0]].keys())

    fig, ax = plt.subplots(figsize=(12, 8))
    bar_width = 0.15
    index = np.arange(len(levels))

    # Selección de métrica
    metric_key = {
        "time": ("avg_time", "std_time", "Execution Time (seconds)", "sokoban_time_comparison.png"),
        "length": ("avg_length", "std_length", "Solution Length (steps)", "sokoban_length_comparison.png"),
        "expanded": ("avg_expanded", None, "Expanded Nodes", "sokoban_expanded_nodes_comparison.png"),
        "frontier": ("avg_frontier", None, "Frontier Nodes", "sokoban_frontier_nodes_comparison.png"),
    }

    if metric not in metric_key:
        raise ValueError(f"Métrica no válida: {metric}")

    avg_key, std_key, ylabel, filename = metric_key[metric]

    for i, algo in enumerate(algorithms):
        values = [results[level][algo].get(avg_key, 0) for level in levels]
        errors = [results[level][algo].get(std_key, 0) for level in levels] if std_key else None

        position = index + (i - len(algorithms) / 2 + 0.5) * bar_width
        ax.bar(position, values, bar_width, label=algo, yerr=errors, capsize=5 if errors else 0)

    ax.set_xlabel("Levels")
    ax.set_ylabel(ylabel)
    ax.set_title(f"{ylabel} by Algorithm and Level")
    ax.set_xticks(index)
    ax.set_xticklabels(levels)
    ax.legend()

    plt.tight_layout()
    plt.savefig(filename)
    plt.close()

def main():
    level_files = ["levels/lvl1.txt", "levels/lvl2.txt", "levels/lvl3.txt"]

    algorithms = [
        {"name": "bfs", "heuristic": None},
        {"name": "dfs", "heuristic": None},
        {"name": "greedy", "heuristic": "manhattan"},
        {"name": "greedy", "heuristic": "euclidean"},
        {"name": "astar", "heuristic": "manhattan"},
        {"name": "astar", "heuristic": "euclidean"},
    ]

    results = {}

    for level_file in level_files:
        level_name = level_file.split("/")[-1]
        results[level_name] = {}

        for algo in algorithms:
            algo_name = algo["name"]
            heuristic = algo["heuristic"]

            key = algo_name if heuristic is None else f"{algo_name}_{heuristic}"
            print(f"Running {key} on {level_name}...")

            results[level_name][key] = run_solver(level_file, algo_name, heuristic)

            print(f"  Average time: {results[level_name][key]['avg_time']:.4f}s")
            print(f"  Average length: {results[level_name][key]['avg_length']:.2f} steps")

    with open("sokoban_results.json", "w") as f:
        json.dump(results, f, indent=2)

    plot_results(results, "time")
    plot_results(results, "length")
    plot_results(results, "expanded")
    plot_results(results, "frontier")

    fig, ax = plt.subplots(figsize=(15, 10))
    ax.axis("off")

    table_data = []
    headers = ["Level", "Algorithm", "Avg Time (s)", "Std Time", "Avg Length", "Std Length", "Avg Expanded", "Avg Frontier"]

    for level in results:
        for algo in results[level]:
            r = results[level][algo]
            table_data.append([
                level, algo,
                f"{r['avg_time']:.4f}", f"{r['std_time']:.4f}",
                f"{r['avg_length']:.2f}", f"{r['std_length']:.2f}",
                f"{r.get('avg_expanded', 0):.2f}", f"{r.get('avg_frontier', 0):.2f}"
            ])

    table = ax.table(cellText=table_data, colLabels=headers, cellLoc="center", loc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1.2, 2)

    plt.title("Sokoban Algorithm Performance Comparison", fontsize=16)
    plt.tight_layout()
    plt.savefig("sokoban_performance_table.png")

    print("\nAnálisis completo! Los resultados se guardaron en:")
    for level in results:
        print(f"- sokoban_time_comparison_{level}.png")
    print("- sokoban_time_comparison_combined.png")
    print("- sokoban_length_comparison.png")
    print("- sokoban_expanded_nodes_comparison.png")
    print("- sokoban_frontier_nodes_comparison.png")
    print("- sokoban_performance_table.png")
    print("- sokoban_results.json")

if __name__ == "__main__":
    main()
