import json
from enum import Enum


class Problem:

    def __init__(self, file):
        self.name, self.grid = Problem.create_grid(file)
        self.rows = len(self.grid)
        self.cols = len(self.grid[0])
        self.initial_state , self.goal_state, self.obstacles= self.search_for_init_goal_obstacles_int()

    @staticmethod
    def create_grid(file):
        with open(file , 'r') as f:
            data= json.load(f)
        return data['name'] , data['grid']

    def search_for_init_goal_obstacles_int(self):
        obstacles = set()
        for i in range(self.rows):
            for j in range(self.cols):
                if self.grid[i][j]=='S':
                    S=(i,j)
                elif self.grid[i][j]=='G':
                    G=(i,j)
                elif self.grid[i][j]=='#':
                    obstacles.add((i,j))
                else:
                    self.grid[i][j]=int(self.grid[i][j])

        return S, G , obstacles

    def transition_function(self,state , action):
        if (row:=state[0] + action.value[0]) < 0 or (col:=state[1] + action.value[1]) < 0 :
            return None
        elif row > self.rows-1 or col > self.cols-1:
            return None
        elif (row,col) in self.obstacles:
            return None
        else:
            return row,col
    def action_cost_function(self, state1, action ):
        state2=self.transition_function(state1, action)
        if state2 is None:
            return None
        elif self.grid[state2[0]][state2[1]] == 'G' or self.grid[state2[0]][state2[1]] == 'S':
            return 1
        else:
            return self.grid[state2[0]][state2[1]]
    def action_precondition_function(self, state):
        allowed_actions=set()
        for action in Action:
            if self.transition_function(state, action) is not None:
                allowed_actions.add(action)
        return allowed_actions

class Action(Enum):
    UP=(-1,0)
    DOWN=(1,0)
    LEFT=(0,-1)
    RIGHT=(0,1)
