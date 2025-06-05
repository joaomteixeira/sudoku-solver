
import time
class TreeNode:
    """
    Element of a search tree. Contains information about its parent, the actual state of the node,
    the action that resulted in the state and the total cost to reach to this node
    """

    def __init__(self, state, parent = None, action = None, path_cost = 0):
        self.state = state
        self.parent = parent
        self.action = action
        self.path_cost = path_cost
        self.depth = parent.depth + 1 if parent else 0

    def __repr__(self):
        return "<Node {}>".format(self.state)
    
    def __lt__(self, node):
        return self.state < node.state
    
    def create_children(self, sudoku):
        children = []
        for action in sudoku.possible_actions(self.state):
            child_state = sudoku.result_action(self.state, action)
            child_node = TreeNode(child_state, self, action, self.path_cost + 1) 
            children.append(child_node)
        return children
    

def dfs(sudoku, print_boards=False):
    """
    Tries to complete sudoku using DFS.
    Returns None if it is not able to find a solution 
    """

    stack = [TreeNode(sudoku.state),]

    while (stack):
        node = stack.pop()
        if print_boards:
            print("\033[2J\033[H", end="") # clears window
            print(node.state.board)
            time.sleep(0.2)
        if sudoku.goal_test(node.state):
            return node
        stack.extend(node.create_children(sudoku))
    return None    

