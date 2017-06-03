
############################################################
# Imports
############################################################

import random
import copy
import sys
import time
import resource

############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    x = [(i + 1) % (rows * cols) for i in range(rows * cols)]
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
        self.moves_performed = []

    def __eq__(self, other):
        return self.__dict__ == other.__dict__

    def get_board(self):
        return self.board

    def perform_move(self, direction):
        col = self.zero_col
        row = self.zero_row
        if direction == "left" and self.zero_col != 0:
            self.board[row][col - 1], self.board[row][col] = self.board[row][col], self.board[row][col - 1]
            self.zero_col -= 1
            return True
        if direction == "right" and self.zero_col != self.cols - 1:
            self.board[row][col + 1], self.board[row][col] = self.board[row][col], self.board[row][col + 1]
            self.zero_col += 1
            return True
        if direction == "up" and self.zero_row != 0:
            self.board[row - 1][col], self.board[row][col] = self.board[row][col], self.board[row - 1][col]
            self.zero_row -= 1
            return True
        if direction == "down" and self.zero_row != self.rows - 1:
            self.board[row + 1][col], self.board[row][col] = self.board[row][col], self.board[row + 1][col]
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

    def is_solved(self):
        test = create_tile_puzzle(self.rows, self.cols)
        return self.get_board() == test.get_board()

    def copy(self):
        return copy.deepcopy(self)

    def successors(self):
        moves = ["up", "down", "right", "left"]
        succesors = []
        for direction in moves:
            copy = self.copy()
            is_possible = copy.perform_move(direction)
            if is_possible:
                succesors.append((direction, copy))
        return succesors

    def set_moves_performed(self, direction):
        self.moves_performed.append(direction)

    def get_moves_performed(self):
        return self.moves_performed

    # Required
    def bfs(self):
        frontier = []
        explored = []
        frontier.append(self.copy())
        while True:
            if len(frontier) == 0:
                return False

            state = frontier.pop(0)  # pop first in queue from list
            explored.append(state)  # add that to explored list

            # print state.get_board()
            # print state.get_moves_performed()

            if state.is_solved():
                print "path_to_goal: " , state.get_moves_performed()
                print "cost_of_path: " , len(state.get_moves_performed())
                print "nodes_expanded: " , len(explored)
                print "search_depth: " , len(state.get_moves_performed())

                return state.get_moves_performed()
            for move, neighbor in state.successors():
                if neighbor not in frontier + explored:
                    neighbor.set_moves_performed(move)
                    frontier.append(neighbor)

start_time = time.time()
input = sys.argv[2]
input = map(int,input.split(","))
board = [input[0:3], input[3:6] , input[6:9] ]

puzzle = TilePuzzle(board)

puzzle.bfs()
print("Running Time: %s" % (time.time() - start_time))


