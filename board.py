class Board:
    def __init__(self, matrix, numbersMissing):
        assert len(matrix) == 9 and len(matrix[0]) == 9, "Sudoku board must be 3x3"

        self.matrix = matrix
        self.numbersMissing = numbersMissing


    def get_number(self, row : int, col : int) -> int:
        assert 0 <= row < 9, "GetNumber: row must be in the range[0, 9["
        assert 0 <= col < 9, "GetNumber: col must be in the range[0, 9["

        return self.matrix[row][col]
    
    def get_block_numbers(self, row : int, col: int) -> list:
        assert 0 <= row < 9, "GetBlockNumbers: row must be in the range[0, 9["
        assert 0 <= col < 9, "GetBlockNumbers: col must be in the range[0, 9["

        nums = []

        start_row = (row // 3) * 3
        start_col = (col // 3) * 3

        for y in range(start_row, start_row + 3):
            for x in range(start_col, start_col + 3):
                nums.append(self.matrix[y][x])

        return nums
    
    def get_row_numbers(self, row : int) -> list:
        return self.matrix[row]

    def get_column_numbers(self, col : int) -> list:
        return [self.matrix[y][col] for y in range(len(self.matrix))]


    def __repr__(self):
        board = ''

        for row in range(len(self.matrix)):
            if row % 3 == 0 and row != 0:
                board += ('- - - - - - - - - - - - \n')

            for column in range(len(self.matrix[0])):
                board += ' '
                if column % 3 == 0 and column != 0:
                    board += '| '
                num = self.matrix[row][column]
                if num == -1:
                    board += '?'
                else:
                    board += str(num)
                
            board += '\n'
        return board

    @staticmethod
    def parse_instance(filename : str):
        """
        Receives a file as input and returns an instance of Board
        """
        count = 0
        matrix = []
        with open(filename, 'r') as f:
            for line in f:
                row = []
                for number in line.split():
                    row.append(int(number))
                    if int(number) == 0:
                        count += 1
                matrix.append(row)
        return Board(matrix, count)
    
