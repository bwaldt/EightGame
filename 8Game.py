############################################################
# CIS 521: Homework 3
############################################################

student_name = "Akash Sadshivapeth"

############################################################
# Imports
############################################################

# Include your imports here, if any are used.
import random
import copy

############################################################
# Section 1: Tile Puzzle
############################################################

def create_tile_puzzle(rows, cols):
    list_of_numbers = x = [(i+1) % (rows*cols) for i in range(rows*cols)] #1D list of numbers in a list
    board = [list_of_numbers[i:i+cols] for i in range(0,rows*cols,cols)] #convert 1D to 2D list
    return TilePuzzle(board)

class TilePuzzle(object):
    # Required
    def __init__(self, board):
        self.board = board # initialize board
        self.rows = len(board)-1 #Row Size of board starting from 0
        self.cols = len(board[0])-1 #Column size of board starting from 0

        #Initialize zero position variables
        self.zero_index = 0 
        self.zero_row = 0
        self.zero_col = 0

        #Set the above variables to the current zero position
        self.refresh_zero(board)

        #Keeps track of moves performed, every object knows where it has come from.
        self.moves_performed = [] 

    def get_board(self):
        return self.board #Returns the entire board

    def refresh_zero(self,board):
        self.zero_index = [(i, board.index(0)) for i, board in enumerate(board) if 0 in board] # Position of zero
        self.zero_row = self.zero_index[0][0] # Row position of zero
        self.zero_col = self.zero_index[0][1] # Column position of zero

    def perform_move(self, direction):
        row = self.zero_row
        col = self.zero_col
        flag = False
        if direction == "up" and row != 0:
            self.board[row][col],self.board[row-1][col] = self.board[row-1][col],self.board[row][col]
            flag = True
        if direction == "down" and row != self.rows:
            self.board[row][col],self.board[row+1][col] = self.board[row+1][col],self.board[row][col]
            flag = True
        if direction == "left" and col != 0:
            self.board[row][col],self.board[row][col-1] = self.board[row][col-1],self.board[row][col]
            flag = True
        if direction == "right" and col != self.cols:
            self.board[row][col],self.board[row][col+1] = self.board[row][col+1],self.board[row][col]
            flag = True
        #Update the location of zero after the move is performed
        self.refresh_zero(self.get_board())
        return flag
        

    def scramble(self, num_moves):
        moves = ["up","down","left","right"]
        counter = 0
        while counter<num_moves:
            direction = random.choice(moves)
            if self.perform_move(direction):
                counter += 1


    def is_solved(self):
        test = create_tile_puzzle(self.rows+1,self.cols+1)
        return self.get_board() == test.get_board()

    def copy(self):
        return copy.deepcopy(self)

    #Returns all possible successors of a puzzle
    def successors(self):
        all_successors = []
        moves = ["up","down","left","right"] #Possible moves
        for direction in moves:
            copy = self.copy()
            is_possible = copy.perform_move(direction) #Checks if the move is possible
            if is_possible:
                all_successors.append((direction,copy))
        return all_successors

    #Given two objects, are they eual? This method helps in determining that
    #https://stackoverflow.com/questions/1227121/compare-object-instances-for-equality-by-their-attributes-in-python
    def __eq__(self,other):
        return self.__dict__==other.__dict__

    def set_moves_performed(self,direction):
        self.moves_performed.append(direction)

    def get_moves_performed(self):
        return self.moves_performed

    # Required
    #Breadth first search for now
    #Build on the following BFS Pseudo code
    #https://courses.edx.org/asset-v1:ColumbiaX+CSMM.101x+2T2017+type@asset+block@AI_edx_search_agents_uninformed__3_.pdf
    def find_solutions_iddfs(self):
        #implements frontier as a queue, add elements using append and always remove the first element, FIFO system
        #Every element in frontier is an object of type TilePuzzle
        frontier = []
        frontier.append(self.copy())
        explored = []

        while not frontier==[]:
            state = frontier[0] 
            del frontier[0] #Always remove the first element because of FIFO system
            explored.append(state)

            #Uncomment these print statements if you want to see every move performed
            print("State: ",state.get_board())
            print("Moves: ",state.get_moves_performed())

            if state.is_solved():
                return state.get_moves_performed()

            for direction,neighbor in state.successors():
                if neighbor not in frontier+explored: #The __eq__(self,other) function is needed for this line
                    #print("direction:##",direction,"##child",neighbor.get_board())
                    neighbor.set_moves_performed(direction)
                    frontier.append(neighbor)

        return False

#################Testing################
b1 = [[1,2,5],[3,4,0],[6,7,8]]
p = TilePuzzle(b1)
solutions = p.find_solutions_iddfs() #finds the solution
print(p.get_board())
print(solutions)

