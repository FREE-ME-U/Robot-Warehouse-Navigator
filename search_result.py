from dataclasses import dataclass


@dataclass
class SearchResult:
    found: bool
    path_actions: list
    path_cost: int
    expanded_nodes: int
    generated_nodes: int
    max_frontier_size: int
    execution_time: float

    def create_path(self, node):
        if node is None:
            return
        self.create_path(node.parent)
        if node.action is not None:
            self.path_actions.append(node.action)
