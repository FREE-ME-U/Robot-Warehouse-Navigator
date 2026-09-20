from pathlib import Path
import time
import algorithms
import search_problem
import search_result

BASE_DIR = Path(__file__).resolve().parent
MAPS_DIR = BASE_DIR / "maps"

MAPS = {
    "1": MAPS_DIR / "warehouse_easy.json",
    "2": MAPS_DIR / "warehouse_dead_ends.json",
    "3": MAPS_DIR / "warehouse_loop.json",
    "4": MAPS_DIR / "warehouse_multiple_paths.json",
    "5": MAPS_DIR / "warehouse_weighted.json",
    "6": MAPS_DIR / "warehouse_unreachable.json",
    "7": MAPS_DIR / "warehouse_large.json"
}

ALGORITHMS = {
    "1": "Breadth-First Search",
    "2": "Uniform-Cost Search",
    "3": "Depth-First Search",
    "4": "Depth-Limited Search",
    "5": "Iterative Deepening Search",
    "6": "Greedy Best-First Search",
    "7": "A* Search",
    "8": "ALL"
}

def choose_map():
    print("\nChoose a warehouse:\n")
    print("1. Easy")
    print("2. Dead Ends")
    print("3. Loop")
    print("4. Multiple Paths")
    print("5. Weighted")
    print("6. Unreachable")
    print("7. Large")
    while True:
        choice = input("\nMap: ").strip()
        if choice in MAPS:
            return MAPS[choice]
        print("Invalid map.")

def choose_algorithm():
    print("\nChoose an algorithm:\n")
    for key, value in ALGORITHMS.items():
        print(f"{key}. {value}")
    while True:
        choice = input("\nAlgorithm: ").strip()
        if choice in ALGORITHMS:
            return choice
        print("Invalid algorithm.")

def read_integer(message):
    while True:
        try:
            value = int(input(message))
            if value >= 0:
                return value
            print("Value must be >= 0.")
        except ValueError:
            print("Invalid integer.")

def print_grid(problem, path=None):
    grid = [row.copy() for row in problem.grid]
    if path is not None:
        for row, col in path:
            if (row, col) != problem.initial_state and (row, col) != problem.goal_state:
                grid[row][col] = "*"
    width = max(len(str(cell)) for row in grid for cell in row)
    print()
    for row in grid:
        print(" ".join(f"{str(cell):>{width}}" for cell in row))
    print()

def create_path_states(node):
    path = []
    while node is not None:
        path.append(node.state)
        node = node.parent
    path.reverse()
    return path

def create_search_result(raw_result, execution_time):
    if raw_result is None:
        return search_result.SearchResult(False, [], 0, 0, 0, 0, execution_time), None
    node, expanded_nodes, max_frontier_size, generated_nodes = raw_result
    result = search_result.SearchResult(True, [], node.path_cost, expanded_nodes, generated_nodes, max_frontier_size, execution_time)
    result.create_path(node)
    return result, node

def run_algorithm(problem, choice, depth_limit=None, max_depth=None):
    start = time.perf_counter()
    if choice == "1":
        raw_result = algorithms.breadth_first_search(problem)
    elif choice == "2":
        raw_result = algorithms.uniform_cost_search(problem)
    elif choice == "3":
        raw_result = algorithms.depth_first_search(problem)
    elif choice == "4":
        raw_result = algorithms.depth_limited_search(problem, depth_limit)
    elif choice == "5":
        raw_result = algorithms.iterative_deepening_search(problem, max_depth)
    elif choice == "6":
        raw_result = algorithms.greedy_best_first_search(problem)
    elif choice == "7":
        raw_result = algorithms.A_star(problem)
    else:
        raise ValueError("Invalid algorithm")
    execution_time = time.perf_counter() - start
    return create_search_result(raw_result, execution_time)

def print_actions(result):
    if not result.path_actions:
        print("No actions.")
        return
    for i, action in enumerate(result.path_actions, 1):
        print(f"{i}. {action.name}")

def print_states(node):
    for i, state in enumerate(create_path_states(node)):
        print(f"{i}. {state}")

def print_result(problem, algorithm_name, result, node):
    print("\n" + "=" * 60)
    print(algorithm_name)
    print("=" * 60)
    if not result.found:
        print("\nNo solution found.")
        print(f"Execution time: {result.execution_time:.8f} s")
        return
    path = create_path_states(node)
    print("\nPath:")
    print_grid(problem, path)
    print("States:")
    print_states(node)
    print("\nActions:")
    print_actions(result)
    print(f"\nPath length: {len(result.path_actions)}")
    print(f"Path cost: {result.path_cost}")
    print(f"Expanded nodes: {result.expanded_nodes}")
    print(f"Generated nodes: {result.generated_nodes}")
    print(f"Max frontier size: {result.max_frontier_size}")
    print(f"Execution time: {result.execution_time:.8f} s")

def run_single(map_file, choice):
    problem = search_problem.Problem(map_file)
    print("\n" + "=" * 60)
    print(f"WAREHOUSE: {problem.name}")
    print("=" * 60)
    print(f"Initial state: {problem.initial_state}")
    print(f"Goal state: {problem.goal_state}")
    print("\nGrid:")
    print_grid(problem)
    depth_limit = read_integer("\nDepth limit: ") if choice == "4" else None
    max_depth = read_integer("\nMaximum depth: ") if choice == "5" else None
    result, node = run_algorithm(problem, choice, depth_limit, max_depth)
    print_result(problem, ALGORITHMS[choice], result, node)

def run_all(map_file):
    problem = search_problem.Problem(map_file)
    print("\n" + "=" * 70)
    print(f"WAREHOUSE: {problem.name}")
    print("=" * 70)
    print(f"Initial state: {problem.initial_state}")
    print(f"Goal state: {problem.goal_state}")
    print("\nGrid:")
    print_grid(problem)
    depth_limit = read_integer("Depth limit for DLS: ")
    max_depth = read_integer("Maximum depth for Iterative Deepening: ")
    results = []
    for choice in map(str, range(1, 8)):
        problem = search_problem.Problem(map_file)
        print(f"\nRunning {ALGORITHMS[choice]}...")
        result, node = run_algorithm(problem, choice, depth_limit, max_depth)
        results.append((choice, result, node))
    print("\n" + "=" * 112)
    print("ALL ALGORITHMS")
    print("=" * 112)
    print(f"{'Algorithm':<30}{'Found':<8}{'Length':<10}{'Cost':<10}{'Expanded':<12}{'Generated':<12}{'Frontier':<12}{'Time':<15}")
    print("-" * 112)
    for choice, result, node in results:
        length = len(result.path_actions) if result.found else "-"
        cost = result.path_cost if result.found else "-"
        expanded = result.expanded_nodes if result.found else "-"
        generated = result.generated_nodes if result.found else "-"
        frontier = result.max_frontier_size if result.found else "-"
        print(f"{ALGORITHMS[choice]:<30}{str(result.found):<8}{str(length):<10}{str(cost):<10}{str(expanded):<12}{str(generated):<12}{str(frontier):<12}{result.execution_time:<15.8f}")
    print("\n" + "=" * 70)
    print("DETAILED RESULTS")
    print("=" * 70)
    for choice, result, node in results:
        problem = search_problem.Problem(map_file)
        print_result(problem, ALGORITHMS[choice], result, node)

def main():
    map_file = choose_map()
    choice = choose_algorithm()
    if choice == "8":
        run_all(map_file)
    else:
        run_single(map_file, choice)

if __name__ == "__main__":
    main()