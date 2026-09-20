import heapq
from collections import deque
from dataclasses import dataclass
from itertools import count
import search_problem
@dataclass
class Node:
    state: tuple[int, int]
    parent: 'Node | None'
    action: search_problem.Action | None
    path_cost: int
    depth: int

    def node_expansion(self, problem ):
        state1 = self.state
        for action in problem.action_precondition_function(state1):
            state2=problem.transition_function(state1, action)
            cost= self.path_cost + problem.action_cost_function(state1, action)
            yield Node(state2, self , action , cost, self.depth+1)

def breadth_first_search(problem):
    node=Node(problem.initial_state,None , None,0 , 0)
    if problem.goal_state== node.state:
        return node , 0 ,0 ,0
    frontier= deque([node])
    reached= set()
    reached.add(node.state)
    expanded_nodes =0
    generated_nodes =0
    sizes_frontier= []
    while frontier:
        sizes_frontier.append(len(frontier))
        node=frontier.popleft()
        expanded_nodes += 1
        for child in node.node_expansion(problem):
            generated_nodes+=1
            state = child.state
            if problem.goal_state == state:
                return child, expanded_nodes , max(sizes_frontier), generated_nodes
            if state not in reached:
                reached.add(state)
                frontier.append(child)
    return None

def uniform_cost_search(problem):
    node=Node(problem.initial_state,None , None,0, 0)
    frontier= []
    counter= count()
    heapq.heappush(frontier,(node.path_cost,next(counter),node))
    reached= {node.state : node}
    expanded_nodes = 0
    generated_nodes =0
    sizes_frontier = []
    while frontier:
        sizes_frontier.append(len(frontier))
        _,_,node= heapq.heappop(frontier)
        if reached[node.state] is not node:
            continue
        if problem.goal_state == node.state:
            return node, expanded_nodes , max(sizes_frontier), generated_nodes
        expanded_nodes += 1
        for child in node.node_expansion(problem):
            generated_nodes+=1
            state = child.state
            if state not in reached or child.path_cost < reached[state].path_cost:
                reached[state] = child
                heapq.heappush(frontier,(child.path_cost,next(counter),child))
    return None

def depth_first_search(problem):
    node = Node(problem.initial_state, None, None, 0,0)
    if problem.goal_state == node.state:
        return node,0,0,0
    frontier = deque([node])
    reached = {node.state}
    expanded_nodes = 0
    generated_nodes =0
    sizes_frontier = []
    while frontier:
        sizes_frontier.append(len(frontier))
        node = frontier.pop()
        expanded_nodes += 1
        for child in node.node_expansion(problem):
            generated_nodes+=1
            state = child.state
            if problem.goal_state == state:
                return child, expanded_nodes , max(sizes_frontier), generated_nodes
            if state not in reached:
                reached.add(state)
                frontier.append(child)
    return None

def greedy_best_first_search(problem):
    node=Node(problem.initial_state,None , None,0,0)
    frontier= []
    counter= count()
    heapq.heappush(frontier,(manhattan_distance(node.state,problem.goal_state),next(counter),node))
    reached= {node.state : node}
    expanded_nodes = 0
    generated_nodes =0
    sizes_frontier = []
    while frontier:
        sizes_frontier.append(len(frontier))
        _,_,node= heapq.heappop(frontier)
        if reached[node.state] is not node:
            continue
        if problem.goal_state == node.state:
            return node, expanded_nodes , max(sizes_frontier), generated_nodes
        expanded_nodes += 1
        for child in node.node_expansion(problem):
            generated_nodes += 1
            state = child.state
            if state not in reached or child.path_cost < reached[state].path_cost:
                reached[state] = child
                heapq.heappush(frontier,(manhattan_distance(child.state,problem.goal_state),
                                         next(counter),child))
    return None

def A_star(problem):
    node=Node(problem.initial_state,None , None,0,0)
    frontier= []
    counter= count()
    heapq.heappush(frontier,(manhattan_distance(node.state,problem.goal_state)+
                             node.path_cost,next(counter),node))
    reached= {node.state : node}
    expanded_nodes =0
    generated_nodes =0
    sizes_frontier = []
    while frontier:
        sizes_frontier.append(len(frontier))
        _,_,node= heapq.heappop(frontier)
        if reached[node.state] is not node:
            continue
        if problem.goal_state == node.state:
            return node, expanded_nodes , max(sizes_frontier), generated_nodes
        expanded_nodes += 1
        for child in node.node_expansion(problem):
            state = child.state
            generated_nodes += 1
            if state not in reached or child.path_cost < reached[state].path_cost:
                reached[state] = child
                heapq.heappush(frontier,(manhattan_distance(child.state,problem.goal_state) +
                                         child.path_cost,next(counter),child))
    return None

def depth_limited_search(problem, limit):
    node = Node(problem.initial_state,None,None,0,0)
    frontier = deque([node])
    reached = {node.state: node.depth}
    generated_nodes =0
    expanded_nodes = 0
    sizes_frontier = []
    while frontier:
        sizes_frontier.append(len(frontier))
        node = frontier.pop()

        if node.state == problem.goal_state:
            return node, expanded_nodes , max(sizes_frontier), generated_nodes
        if node.depth >= limit:
            continue
        expanded_nodes += 1
        for child in node.node_expansion(problem):
            generated_nodes += 1
            state = child.state
            if (state not in reached or child.depth < reached[state]):
                reached[state] = child.depth
                frontier.append(child)
    return None

def iterative_deepening_search(problem, max_depth):
    for limit in range(max_depth + 1):
        result = depth_limited_search(problem, limit)
        return result
    return None

def manhattan_distance(state, goal):
    row1, col1 = state
    row2, col2 = goal
    return abs(row1 - row2) + abs(col1 - col2)


