# Robot Warehouse Navigator

Robot Warehouse Navigator is a Python project that applies classical Artificial Intelligence search algorithms to a warehouse navigation problem.

A robot moves inside a grid-based warehouse from an initial position `S` to a goal position `G`, while avoiding obstacles and considering movement costs.

The project allows different search algorithms to solve the same problem and compares their behavior and performance.

## Features

- Grid-based warehouse environment
- Start and goal positions
- Obstacles
- Weighted cells
- Path reconstruction
- Path visualization
- Execution statistics
- Comparison between multiple search algorithms
- JSON-based warehouse maps
- Interactive command-line interface

## Search Algorithms

The following search algorithms are implemented:

- Breadth-First Search (BFS)
- Uniform-Cost Search (UCS)
- Depth-First Search (DFS)
- Depth-Limited Search (DLS)
- Iterative Deepening Search (IDS)
- Greedy Best-First Search
- A* Search

Greedy Best-First Search and A* use Manhattan distance as their heuristic.

## Search Problem

The warehouse navigation task is modeled as a classical search problem.

Each problem contains:

- **State space:** all valid robot positions in the warehouse
- **Initial state:** the starting position of the robot
- **Goal state:** the destination of the robot
- **Actions:** `UP`, `DOWN`, `LEFT`, `RIGHT`
- **Transition function:** determines the new robot position after an action
- **Action-precondition function:** determines which movements are valid
- **Action-cost function:** determines the cost of entering a cell

A search node stores:

- State
- Parent node
- Action
- Path cost
- Depth

This allows the final path to be reconstructed after reaching the goal.

## Warehouse Representation

Warehouses are stored as JSON files inside the `maps` directory.

Example:

```json
{
  "name": "warehouse_example",
  "grid": [
    ["S", "1", "1", "#"],
    ["1", "#", "1", "1"],
    ["1", "1", "2", "1"],
    ["#", "1", "1", "G"]
  ]
}
```

The symbols have the following meaning:

| Symbol | Meaning |
|---|---|
| `S` | Start position |
| `G` | Goal position |
| `#` | Obstacle |
| `1`, `2`, `3`, ... | Cost of entering the cell |
| `*` | Cell belonging to the solution path |

## Available Maps

The project currently contains several test environments:

- Easy
- Dead Ends
- Loop
- Multiple Paths
- Weighted
- Unreachable
- Large

These maps are designed to test different properties of the search algorithms.

## Project Structure

```text
Robot-Warehouse-Navigator/
│
├── main.py
├── algorithms.py
├── search_problem.py
├── search_result.py
├── README.md
│
└── maps/
    ├── warehouse_easy.json
    ├── warehouse_dead_ends.json
    ├── warehouse_loop.json
    ├── warehouse_multiple_paths.json
    ├── warehouse_weighted.json
    ├── warehouse_unreachable.json
    └── warehouse_large.json
```

### `main.py`

Provides the command-line interface, executes the selected search algorithm and displays the results.

### `algorithms.py`

Contains the `Node` representation and all search algorithm implementations.

### `search_problem.py`

Defines the warehouse search problem, including states, actions, transitions, obstacles and movement costs.

### `search_result.py`

Stores the result of a search, including the reconstructed path and performance statistics.

### `maps/`

Contains the warehouse configurations in JSON format.

## Requirements

The project requires Python 3.10 or later.

No external libraries are required.

The project uses only Python standard-library modules such as:

```text
collections
dataclasses
enum
heapq
itertools
json
pathlib
time
```

## Running the Project

Clone the repository:

```bash
git clone https://github.com/FREE-ME-U/Robot-Warehouse-Navigator.git
```

Enter the project directory:

```bash
cd Robot-Warehouse-Navigator
```

Run the program:

```bash
python main.py
```

The program will first ask you to select a warehouse:

```text
Robot Warehouse Navigator

1. Easy
2. Dead Ends
3. Loop
4. Multiple Paths
5. Weighted
6. Unreachable
7. Large
```

Then select a search algorithm:

```text
1. BFS
2. UCS
3. DFS
4. DLS
5. IDS
6. Greedy
7. A*
8. ALL
```

Selecting `ALL` executes every algorithm on the same warehouse.

## Example Output

A solution path is displayed directly on the warehouse grid:

```text
S * * * # 1 1 1
1 # 1 * # 1 # 1
1 # 1 * * * * 1
1 # # # # 1 * 1
1 1 1 1 # 1 * G
```

The `*` symbols represent the cells traversed by the robot.

For each algorithm, the program reports statistics such as:

```text
Length: 16
Cost: 16
Expanded: 42
Generated: 105
Max frontier: 9
Time: 0.7691 ms
```

When `ALL` is selected, a final comparison table is displayed:

```text
Algorithm Found   Length   Cost    Expanded  Generated  Frontier  Time(ms)
----------------------------------------------------------------------------
BFS       Yes     16       16      62        150        9         1.2883
UCS       Yes     16       16      66        160        9         1.2588
DFS       Yes     24       24      24        57         11        0.4659
DLS       Yes     24       24      28        70         13        0.6098
Greedy    Yes     16       16      16        42         10        0.3410
A*        Yes     16       16      42        105        9         0.7691
```

The exact values depend on the selected map and the order in which states are explored.

## Performance Metrics

The project compares the algorithms using the following metrics.

### Path Length

Number of actions required to reach the goal.

### Path Cost

Total cost of all movements in the solution.

### Expanded Nodes

Number of nodes whose successors were explored.

### Generated Nodes

Number of successor nodes generated during the search.

### Maximum Frontier Size

Maximum number of nodes stored in the frontier during the search.

### Execution Time

Time required by the algorithm to perform the search.

## Heuristic

Greedy Best-First Search and A* use Manhattan distance:

```text
h(n) = |row_current - row_goal| + |column_current - column_goal|
```

This heuristic estimates the number of horizontal and vertical movements required to reach the goal.

## BFS vs UCS

On maps where every movement has the same cost, BFS and UCS can produce the same optimal path.

On weighted maps, however, the shortest path in number of steps is not necessarily the cheapest path.

UCS considers the total path cost, while BFS primarily considers search depth.

## Greedy Search vs A*

Greedy Best-First Search selects nodes according to:

```text
f(n) = h(n)
```

It focuses on states that appear closest to the goal.

A* combines the cost already paid with the estimated remaining cost:

```text
f(n) = g(n) + h(n)
```

where:

- `g(n)` is the path cost from the initial state to `n`
- `h(n)` is the heuristic estimate from `n` to the goal

## Purpose

This project was developed as a practical exercise for studying classical Artificial Intelligence search techniques.

Its main purpose is to connect theoretical concepts such as:

- State spaces
- Search trees
- Node expansion
- Frontier management
- Repeated-state detection
- Uninformed search
- Informed search
- Heuristics
- Path cost
- Completeness
- Optimality
- Time complexity
- Space complexity

with an actual Python implementation.

## Possible Future Improvements

Possible extensions include:

- Additional heuristics
- Diagonal movements
- Multiple goals
- Dynamic obstacles
- Randomly generated warehouses
- Graphical visualization
- Step-by-step search animation
- Benchmark export to CSV
- Automated tests
- Larger warehouse environments
- Additional search algorithms

## Author

**Azer Oueslati**

Computer Science student at Sapienza University of Rome.

## License

This project is intended for educational purposes.