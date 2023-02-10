import time
import numpy as np

# *** ******************* ***
# *** PROBLEM DESCRIPTION ***
# *** ******************* ***

# This code implements a Python version of the "Tic-Tac-Toe" minigame which exploits the "MiniMax" Algorithm for PvP Games.
# In this code we play pretending to be the "MIN" player ('X') and against the Algorithm itself, which acts like the "MAX" player ('O').

# The objective of the game is to fill one among the rows, the columns, the principal diagonal and the secondary diagonal with our symbol: if the Algorithm succeds in this task, it wins and we lose.
# If instead both of us fail, nobody wins.

# Each state of the game is evalued via the "MiniMax" approach in which:
    # - A terminal state in which we win has value == -1.
    # - A terminal state in which the Algorithm wins has value == 1.
    # - A terminal state in which nobody wins has value == 0.

# A "non-terminal" state is evalued depending on who has to move:
    # - If it's our turn (MIN state), the current state is evalued with the Minimum value among the values of the successor states.
    # - If it's the Algorithm's turn (MAX state), the current state is evalued with the Maximum value among the values of the successor states.


class Game:
    def __init__(self):
        self.initialize_game()


    def initialize_game(self):
        # Setup of the Empty Board
        self.current_state = [['.','.','.'],
                              ['.','.','.'],
                              ['.','.','.']]
        # First Player to Move
        self.player_turn = 'X'


    def draw_board(self):
        for i in range(0,3):
            for j in range(0,3):
                print("{}|".format(self.current_state[i][j]), end="")
            print()
        print()
    
# FUNCTION: checks if the chosen move is valid
    def is_valid(self, px, py):

        # 1st Negative Case: we can't place a symbol out of the board -> board.shape == (3,3)
        if not((0 <= px <= 2) or (0 <= py <= 2)):
            return False

        # 2nd Negative Case: we can't place a symbol in a cell which is already occupied by a valid symbol ('X' or 'O')
        elif self.current_state[px][py] != '.':
            return False
        
        else:
            return True

# FUNCTION: checks if the game is not over, otherwise if the current state is a victory state or a tie state.
    def is_end(self):

        # Victory on a Column
        for i in range(0,3):
            if self.current_state[0][i] != '.':
                if self.current_state[0][i] == self.current_state[1][i] and self.current_state[1][i] == self.current_state[2][i]:
                    return self.current_state[0][i]

        # Victory on a Row
        for i in range(0,3):
            if self.current_state[i] == ['X','X','X']:
                return 'X'
            elif self.current_state[i] == ['O','O','O']:
                return 'O'

        # Victory on the Principal Diagonal
        if self.current_state[0][0] != '.':
            if self.current_state[0][0] == self.current_state[1][1] and self.current_state[1][1] == self.current_state[2][2]:
                return self.current_state[0][0]

        # Victory on the Secondary Diagonal
        if self.current_state[2][0] != '.':
            if self.current_state[2][0] == self.current_state[1][1] and self.current_state[1][1] == self.current_state[0][2]:
                return self.current_state[2][0]

        # No Victory: is the Game over?
        for i in range(0,3):
            for j in range(0,3):
                if self.current_state[i][j] == '.':
                    return None

        # No Victory && the Game is over...Tie!
        return "Tie"


# FUNCTION: evaluates all the possible moves for the Player and suggests the best one.
    def min(self):
        minv = np.inf
        # Possible values for "minv"
            # -1: Player wins!
            # 0: Tie
            # 1: Player loses...
        
        qx = None
        qy = None

        result = self.is_end()

        if result == 'X':   # If the Player has won...
            return (-1, 0, 0)
        if result == 'O':   # If the Algorithm has won...
            return (1, 0, 0)
        if result == 'Tie': # If nobody has won...
            return (0, 0, 0)
        
        # Otherwise, if the Game is not in a "Terminal State", "min()" has to generate the children of current state. It implies the analysis of all the possible moves.
        # For each possible move chosen by MIN (Player), we arrive in a MAX state (AI's Turn): for this reason, we have to execute "max()" on all the children of the current state.
        for i in range(0,3):
            for j in range(0,3):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'X'
                    (m, max_i, max_j) = self.max()

                    if m < minv:
                        minv = m
                        qx = i
                        qy = j
                    self.current_state[i][j] = '.'
        
        return (minv, qx, qy)


# FUNCTION: evaluates all the possible moves for the AI and returns the best one.
    def max(self):
        maxv = -np.inf
        # Possible values for "max"
            # -1: AI loses...
            # 0: Tie
            # 1: AI wins!
        
        px = None
        py = None

        result = self.is_end()

        if result == 'X':   # If AI has lost...
            return (-1, 0, 0)
        if result == 'Tie': # If nobody has won...
            return (0, 0, 0)
        if result == 'O':   # If the AI has won...
            return (1, 0, 0)
        
        # Otherwise, if the Game is not in a "Terminal State", "max()" has to generate the children of current state. It implies the analysis of all the possible moves.
        # For each possible move chosen by MAX (AI), we arrive in a MIN state (Player's Turn): for this reason, we have to execute "min()" on all the children of the current state.
        for i in range(0,3):
            for j in range(0,3):
                if self.current_state[i][j] == '.':
                    self.current_state[i][j] = 'O'
                    (m, min_i, min_j) = self.min()

                    if m > maxv:
                        maxv = m
                        px = i
                        py = j
                    self.current_state[i][j] = '.'
        
        return (maxv, px, py)


# FUNCTION: executes the Game.
    def minimax_play(self):
        while True:
            # Dump of the Current State
            self.draw_board()
            # ...is the Game Over?
            self.result = self.is_end()

            # Yes, the Game is Over
            if self.result != None:
                if self.result == 'X':
                    print("Player Wins!")
                elif self.result == 'O':
                    print("The Algorithm has won on the Player...")
                elif self.result == 'Tie':
                    print("Tie, nobody won!")
                return

            # No, the Game is not Over
            else:

                # Player's Turn!
                if self.player_turn == 'X':
                    while True:
                        #start = time.time()
                        (m, qx, qy) = self.min()
                        #end = time.time()

                        #print('Evaluation time: {}s'.format(round(end - start, 7)))
                        print("Player's Turn: choose your move!")
                        print('Recommended Move: X = {}, Y = {}'.format(qx, qy))

                        px = int(input('Row Index (0, 1 or 2): '))
                        py = int(input('Column Index (0, 1 or 2): '))

                        if self.is_valid(px, py):
                            self.current_state[px][py] = 'X'
                            self.player_turn = 'O'
                            print()
                            break
                        else:
                            print('The move you chose is not valid. Try again\n')
                
                # AI's Turn!
                else:
                    print("AI's Turn...\n")
                    (m, px, py) = self.max()
                    self.current_state[px][py] = 'O'
                    self.player_turn = 'X'
                

# *** **** ***
# *** MAIN ***
# *** **** ***

g = Game()
g.minimax_play()