import json
import time

import matplotlib.pyplot as plt
import numpy as np

from src.sokoban import Sokoban, heuristica_euclidean, heuristica_manhattan


def run_solver(file_path, algorithm, heuristic=None, runs=50):
    """Run the Sokoban solver multiple times and return execution times and solution lengths."""
    times = []
    solution_lengths = []

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

    return {
        "times": times,
        "lengths": solution_lengths,
        "avg_time": np.mean(times),
        "std_time": np.std(times),
        "avg_length": np.mean(solution_lengths),
        "std_length": np.std(solution_lengths),
    }


def plot_results(results, metric="time"):
    """Plot results for the given metric with standard deviation."""
    levels = list(results.keys())
    algorithms = list(results[levels[0]].keys())

    if metric == "time":
        # For time metric, create a separate plot for each level
        for level in levels:
            fig, ax = plt.subplots(figsize=(10, 6))

            # Bar positions
            bar_width = 0.7
            index = np.arange(len(algorithms))

            # Get values and error bars for this level
            values = [results[level][algo]["avg_time"] for algo in algorithms]
            errors = [results[level][algo]["std_time"] for algo in algorithms]

            ax.bar(index, values, bar_width, yerr=errors, capsize=5)

            ax.set_xlabel("Algorithms")
            ax.set_ylabel("Execution Time (seconds)")
            ax.set_title(f"Average Execution Time for Level {level} (with Standard Deviation)")
            ax.set_xticks(index)
            ax.set_xticklabels(algorithms, rotation=45, ha="right")
            ax.grid(axis="y", linestyle="--", alpha=0.7)

            plt.tight_layout()
            plt.savefig(f"sokoban_time_comparison_{level}.png")
            plt.close()

        # Also create a combined plot
        fig, ax = plt.subplots(figsize=(12, 8))
        bar_width = 0.15
        index = np.arange(len(levels))

        for i, algo in enumerate(algorithms):
            values = [results[level][algo]["avg_time"] for level in levels]
            errors = [results[level][algo]["std_time"] for level in levels]

            position = index + (i - len(algorithms) / 2 + 0.5) * bar_width
            ax.bar(position, values, bar_width, label=algo, yerr=errors, capsize=5)

        ax.set_xlabel("Levels")
        ax.set_ylabel("Execution Time (seconds)")
        ax.set_title(f"Average Execution Time by Algorithm and Level (with Standard Deviation)")
        ax.set_xticks(index)
        ax.set_xticklabels(levels)
        ax.legend()

        plt.tight_layout()
        plt.savefig(f"sokoban_time_comparison_combined.png")
        plt.close()
    else:  # length
        # For solution length, keep a single plot as before
        fig, ax = plt.subplots(figsize=(12, 8))
        bar_width = 0.15
        index = np.arange(len(levels))

        for i, algo in enumerate(algorithms):
            values = [results[level][algo]["avg_length"] for level in levels]
            errors = [results[level][algo]["std_length"] for level in levels]

            position = index + (i - len(algorithms) / 2 + 0.5) * bar_width
            ax.bar(position, values, bar_width, label=algo, yerr=errors, capsize=5)

        ax.set_xlabel("Levels")
        ax.set_ylabel("Solution Length (steps)")
        ax.set_title(f"Average Solution Length by Algorithm and Level (with Standard Deviation)")
        ax.set_xticks(index)
        ax.set_xticklabels(levels)
        ax.legend()

        plt.tight_layout()
        plt.savefig(f"sokoban_length_comparison.png")
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

            # Create a unique key for each algorithm-heuristic combination
            key = algo_name if heuristic is None else f"{algo_name}_{heuristic}"
            print(f"Running {key} on {level_name}...")

            results[level_name][key] = run_solver(level_file, algo_name, heuristic)

            print(f"  Average time: {results[level_name][key]['avg_time']:.4f}s")
            print(f"  Average length: {results[level_name][key]['avg_length']:.2f} steps")

    # Save raw results to JSON for future reference
    with open("sokoban_results.json", "w") as f:
        json.dump(results, f, indent=2)

    # Plot execution time comparison
    plot_results(results, "time")

    # Plot solution length comparison
    plot_results(results, "length")

    # Create a comprehensive table visualization
    fig, ax = plt.subplots(figsize=(15, 10))
    ax.axis("off")

    table_data = []
    headers = ["Level", "Algorithm", "Avg Time (s)", "Std Time", "Avg Length", "Std Length"]

    for level in results:
        for algo in results[level]:
            r = results[level][algo]
            table_data.append([level, algo, f"{r['avg_time']:.4f}", f"{r['std_time']:.4f}", f"{r['avg_length']:.2f}", f"{r['std_length']:.2f}"])

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
    print("- sokoban_performance_table.png")
    print("- sokoban_results.json")


if __name__ == "__main__":
    main()
