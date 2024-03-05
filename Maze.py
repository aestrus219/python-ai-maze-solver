import sys

class Node():
    def __init__(self, state, action, parent):
        self.state = state
        self.parent = parent
        self.action = action

class Frontier():
    def __init__(self):
        self.frontier = []
    def add(self, node):
        self.frontier.append(node)
    def contains(self, state):
        return self.frontier.count(state)
    def empty(self):
        return len(self.frontier) == 0
    def remove(self):
        if self.empty():
            raise Exception("Frontier is empty")
        else:
            node = self.frontier[-1]
            self.frontier = self.frontier[:-1]
            return node

class Maze():
    def __init__(self, file):
        with open(file) as f:
            contents = f.read()
        if contents.count('A') != 1:
            raise Exception("Missing initial state A")
        elif contents.count('B') !=1:
            raise Exception("Missing goal state B")
        
        # obtain height and width
        contents = contents.splitlines()
        self.height = len(contents)
        self.width = max(len(line) for line in contents)

        # detecting walls, initial and goal state
        self.walls = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                try:
                    state = contents[i][j]
                    if state == "A":
                        self.initialState = (i,j)
                        row.append(False)
                    elif state == "B":
                        self.goalState = (i,j)
                        row.append(False)
                    elif state == " ":
                        row.append(False)
                    else:
                        row.append(True)
                except IndexError:
                    row.append(False)
            self.walls.append(row)
        self.solution = None    

    def print(self):
        solution = self.solution[1] if self.solution is not None else None
        print()
        for i, row in enumerate(self.walls):
            for j, col in enumerate(row):
                if col:
                    print("█", end="")
                elif (i, j) == self.initialState:
                    print("A", end="")
                elif (i, j) == self.goalState:
                    print("B", end="")
                elif solution is not None and (i, j) in solution:
                    print("*", end="")
                else:
                    print(" ", end="")
            print()
        print()
    
    def neigboringStates(self,state):
        row, col = state
        behaviours = [
            ("up", (row -1, col)),
            ("down", (row +1, col)),
            ("left", (row, col-1)),
            ("right", (row, col+1)),
        ]
        result = []
        for action, (r,c) in behaviours:
            if 0<=r<self.height and 0<=c<self.width and not self.walls[r][c]:
              result.append((action,(r,c)))
        return result
    
    def solve(self):
        initialState = Node(
            state=self.initialState,
            parent=None,
            action=None
        )
        f = Frontier()
        f.add(initialState)

        self.explored = set()

        while True:
            if f.empty():
                raise Exception("There is no solution to this maze")
            node = f.remove()
            if node.state == self.goalState:
                actions = []
                cells = []
                while node.parent is not None:
                    actions.append(node.action)
                    cells.append(node.state)
                    node = node.parent
                actions.reverse()
                cells.reverse()
                self.solution = (actions, cells)
                return
            
            self.explored.add(node.state)

            for action, state in self.neigboringStates(node.state):
                if not f.contains(state) and state not in self.explored:
                    child = Node(
                        state=state,
                        parent=node,
                        action=action
                    )
                    f.add(child)

m = Maze(sys.argv[1])
print("Solving...")
m.solve()
print("Solution:")
m.print()