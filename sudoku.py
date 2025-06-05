from board import Board
from search import dfs
import argparse

    
class SudokuState:
    state_id = 0

    def __init__(self, board : Board):
        self.board = board
        self.id = SudokuState.state_id
        SudokuState.state_id += 1
    
    def __lt__(self, other):
        return self.id < other.id

class Sudoku():
    def __init__(self, board : Board):
        self.state = SudokuState(board)
        self.initial = self.state

    def is_number_possible(self, board : Board, row : int, col : int, val: int) -> bool:
        """
            This function tries to place a number (val) in the pos [row, col] and returns if it is possible or not
        """ 
        assert 0 <= row < 9, "isPossible: row must be in the range[0, 9["
        assert 0 <= col < 9, "isPossible: col must be in the range[0, 9["
        assert 0 < val <= 9, "isPossible: val must be a number between 1 and 9"

        # check if number is already in the same block
        if val in board.get_block_numbers(row, col): return False

        # check if that row already has the value
        elif val in board.get_row_numbers(row): return False

        # check if value is in the column
        elif val in board.get_column_numbers(col): return False
        
        return True

    def possible_actions(self, state : SudokuState) -> list[tuple[int, int, int]]:
        """
            Returns possible actions from a specific state. Action described as (row, col, val)
        """
        actions = []
        board = state.board

        for i in range(len(board.matrix)):
            for j in range(len(board.matrix[0])):
                if board.get_number(i, j) != 0: continue # already has a number

                possible_numbers = set(range(1, 10))

                possible_numbers.difference_update(
                    set(board.get_block_numbers(i, j)),
                    set(board.get_column_numbers(j)),
                    set(board.get_row_numbers(i))
                )

                

                for candidate in possible_numbers:
                    if self.is_number_possible(board, i, j, candidate): # redundant, but serves as sanity check

                        # if only one candidate return immediately
                        if len(possible_numbers) == 1:
                            return [(i, j, candidate),]
                        actions.append((i, j, candidate),)
        return actions        

    def result_action(self, curr_state : SudokuState, action) -> SudokuState:

        """
            This function returns a sudoku state resulting from performing a certain action
        """

        row = action[0]
        col = action[1]
        candidate = action[2]

        assert isinstance(action, tuple) and len(action) == 3, "Result_action: Action must be described as a tuple of size 3"
        assert isinstance(row, int) and 0 <= row < 9, "Result_action: Action[0] must be an int in range (0, 9["
        assert isinstance(col, int) and 0 <= col < 9, "Result_action: Action[1] must be an int in range (0, 9["
        assert isinstance(candidate, int) and 0 < candidate <= 9, "Result_action: Action[2] must be an int in range (1, 9)"

        assert isinstance(curr_state.board.matrix[row][col], int) and curr_state.board.matrix[row][col] == 0, "Result_action: Action trying to override placed number"
        newMatrix = [[x for x in i] for i in curr_state.board.matrix]
        
        newMatrix[row][col] = candidate
        return SudokuState(Board(newMatrix, curr_state.board.numbersMissing - 1))

    def goal_test(self, state) -> bool:
        """
            Checks if state is completed. Checks if all places have been filled, 
            instead of analyzing rows, cols and blocks
        """
        return state.board.numbersMissing == 0

def get_args():
    parser = argparse.ArgumentParser(description="Sudoku Solver")
    parser.add_argument('-f', '--file', type=str, help='Name of the input file', default="inputs/input1.txt",dest='file_name')


    return parser.parse_args()



if __name__ == "__main__":

    args = get_args()

    board = Board.parse_instance(args.file_name)
    sudoku = Sudoku(board)
    result = dfs(sudoku, True)
    print("Depth reached: " + str(result.path_cost))