############################################################
# CIS 521: Homework 3
############################################################

student_name = "Type your full name here."

############################################################
# Imports
############################################################

import random



############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    x = [ (i + 1) % (rows*cols) for i in range(rows * cols)]
    s = [x[i:i + cols] for i in range(0, len(x), cols)]
    return TilePuzzle(s)

class TilePuzzle(object):
    
    # Required
    def __init__(self, board):
        self.board = board
        self.rows = len(board)
        self.cols = len(board[0])
        self.zero = [(i, board.index(0)) for i, board in enumerate(board) if 0 in board]
        self.zero_row = self.zero[0][0]
        self.zero_col = self.zero[0][1]

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        col = self.zero_col
        row = self.zero_row
        if direction == "left" and self.zero_col != 0:
            self.board[row][col-1], self.board[row][col] = self.board[row][col], self.board[row][col-1]
            self.zero_col -= 1
            return True
        if direction == "right" and self.zero_col != self.cols-1:
            self.board[row][col+1], self.board[row][col] = self.board[row][col], self.board[row][col+1]
            self.zero_col += 1
            return True
        if direction == "up" and self.zero_row != 0:
            self.board[row-1][col], self.board[row][col] = self.board[row][col], self.board[row-1][col]
            self.zero_row -= 1
            return True
        if direction == "down" and self.zero_row != self.rows-1:
            self.board[row+1][col], self.board[row][col] = self.board[row][col], self.board[row+1][col]
            self.zero_row += 1
            return True
        else:
            return False

    def scramble(self, num_moves):
        input = ["up", "down", "right", "left"]
        moves = 0
        while moves < num_moves:
            if self.perform_move(random.choice(input)) == True:
                moves += 1
        print moves
    def is_solved(self):
        test = create_tile_puzzle(self.rows,self.cols)
        print self.get_board() == test.get_board()



    def copy(self):
        return self

    def successors(self):
        input = ["up", "down", "right", "left"]
        ans = ()
        for y in input:
            p2 = self.copy()
            p2.perform_move(y)
            ans = (y , p2.get_board() )
            print ans

    # Required
    def find_solutions_iddfs(self):
        pass

    # Required
    def find_solution_a_star(self):
        pass


p = create_tile_puzzle(3, 3)
p.successors()

