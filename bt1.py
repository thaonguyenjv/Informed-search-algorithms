from simpleai.search import SearchProblem, astar
import time

GOAL_STATE = ((1, 2, 3),
              (8, 0, 4),
              (7, 6, 5))
ACTIONS = ['UP', 'DOWN', 'LEFT', 'RIGHT']

class EightPuzzleProblem(SearchProblem):
    def __init__(self, initial_state, heuristic_type=1):
        super().__init__(initial_state)
        self.heuristic_type = heuristic_type
    
    def actions(self, state):
        row, col = [(ix, iy) for ix, row in enumerate(state) for iy, i in enumerate(row) if i == 0][0]
        possible_actions = []
        if row > 0: possible_actions.append('UP')
        if row < 2: possible_actions.append('DOWN')
        if col > 0: possible_actions.append('LEFT')
        if col < 2: possible_actions.append('RIGHT')
        return possible_actions
    
    def result(self, state, action):
        row, col = [(ix, iy) for ix, row in enumerate(state) for iy, i in enumerate(row) if i == 0][0]
        new_state = [list(r) for r in state]
        if action == 'UP': 
            new_row, new_col = row - 1, col
        elif action == 'DOWN': 
            new_row, new_col = row + 1, col
        elif action == 'LEFT': 
            new_row, new_col = row, col - 1
        elif action == 'RIGHT': 
            new_row, new_col = row, col + 1
        
        new_state[row][col], new_state[new_row][new_col] = new_state[new_row][new_col], new_state[row][col]
        return tuple(tuple(r) for r in new_state)
    
    def is_goal(self, state):
        return state == GOAL_STATE
    
    def cost(self, state, action, state2):
        return 1
    
    def heuristic(self, state):
        if self.heuristic_type == 1:
            return self.h1(state)
        else:
            return self.h2(state)
    
    # === Heuristic 1: Số ô sai vị trí ===
    def h1(self, state):
        misplaced = 0
        for i in range(3):
            for j in range(3):
                if state[i][j] != 0 and state[i][j] != GOAL_STATE[i][j]:
                    misplaced += 1
        return misplaced
    
    # === Heuristic 2: Manhattan distance ===
    def h2(self, state):
        distance = 0
        for i in range(3):
            for j in range(3):
                value = state[i][j]
                if value != 0:
                    goal_i, goal_j = [(x, y) for x, row in enumerate(GOAL_STATE) for y, val in enumerate(row) if val == value][0]
                    distance += abs(i - goal_i) + abs(j - goal_j)
        return distance
def print_state(state):
    for row in state:
        print(' '.join(str(i) if i != 0 else ' ' for i in row))
    print()
def main():
    # Trạng thái ví dụ
    initial_state = ((8, 2, 3),
                     (7, 6, 4),
                     (1, 0, 5))
    # Chạy với heuristic h1
    print("=== A* với Heuristic 1 (Số ô sai vị trí) ===")
    problem1 = EightPuzzleProblem(initial_state, heuristic_type=1)
    start = time.time()
    result1 = astar(problem1, graph_search=True)
    end = time.time()
    print("Steps:", len(result1.path()) - 1)
    print("Time:", round(end - start, 4), "s")
    
    # Chạy với heuristic h2
    print("\n=== A* với Heuristic 2 (Manhattan distance) ===")
    problem2 = EightPuzzleProblem(initial_state, heuristic_type=2)
    start = time.time()
    result2 = astar(problem2, graph_search=True)
    end = time.time()
    print("Steps:", len(result2.path()) - 1)
    print("Time:", round(end - start, 4), "s")

    print("\n=== Đường đi với h2 ===")
    for action, state in result2.path():
        print("Action:", action)
        print_state(state)

if __name__ == '__main__':
    main()