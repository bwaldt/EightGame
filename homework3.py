############################################################
# CIS 521: Homework 3
############################################################

student_name = "Type your full name here."

############################################################
# Imports
############################################################

import random
import copy
import time
import Queue as Q



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
        self.moves_performed = []

    def __eq__(self,other):
        return self.__dict__==other.__dict__

    def __iter__(self):
        return TilePuzzle(self.board)

    def __getitem__(self, item):
        return TilePuzzle(self.board)

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

    def is_solved(self):
        test = create_tile_puzzle(self.rows,self.cols)
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
                succesors.append((direction,copy))
        return succesors

    def set_moves_performed(self,direction):
        self.moves_performed.append(direction)

    def get_moves_performed(self):
        return self.moves_performed

    # Required
    def find_solutions_iddfs(self):
        frontier = []
        explored = []
        actions = []
        frontier.append(self.copy())
        while True:
            if len(frontier) == 0:
                return False

            state = frontier.pop(0) #pop first in queue from list
            explored.append(state) #add that to explored list

            #print state.get_board()
            #print state.get_moves_performed()

            if state.is_solved():
                print state.get_board()
                return state.get_moves_performed()
            for move, neighbor in state.successors():
                if neighbor not in frontier + explored:
                    neighbor.set_moves_performed(move)
                    frontier.append(neighbor)



    def herustic(self):
        herMisplaced = 0
        state = self.get_board()
        solution = create_tile_puzzle(3,3)
        solution = solution.get_board()
        for i in range(9):
            if i <= 2:
                if state[0][i] != solution[0][i]:
                    herMisplaced += 1
            if i >= 3 and i <= 5:
                if state[1][i % 3] != solution[1][i % 3]:
                    herMisplaced += 1
            if i > 5:
                if state[2][i % 3] != solution[2][i % 3]:
                    herMisplaced += 1
        return herMisplaced


    def find_solution_a_star(self):
        frontier = Q.PriorityQueue()
        explored = []
        actions = []
        h = self.herustic()
        frontier.put((h,self.copy()))
        while True:
            if frontier.empty():
                return False

            state = frontier.get()#pop first in queue, queue is tuple of { h(n) + g(n) , Board }
            state = state[1] # only take board object, ignore cost
            explored.append(state) #add that to explored list

            #print state.get_board()
            #print state.get_moves_performed()

            if state.is_solved():
                print state.get_moves_performed()
                return state.get_moves_performed()
            for move, neighbor in state.successors():
                if neighbor not in explored:
                    neighbor.set_moves_performed(move)
                    h = neighbor.herustic()
                    moves = neighbor.get_moves_performed()
                    moves = len(moves)
                    frontier.put((h+moves,neighbor))






#b1 = [[1, 2, 3], [4, 5, 0], [7, 8, 6]]
#p = TilePuzzle(b1)

#print p.find_solution_a_star()