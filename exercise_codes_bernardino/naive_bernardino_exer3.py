# Extent and Purpose of AI Use:
# How much AI did you use in your work? None
# Which parts of your work involved the use of AI tools? None
# Responsible use justification:
# Explain how you used AI responsibly and ethically in completing the task. N/A

# sources: 
# https://www.geeksforgeeks.org/python/python-program-to-convert-a-list-to-string/
# https://stackoverflow.com/questions/12897374/get-unique-values-from-a-list-in-python
# https://stackoverflow.com/questions/14895599/insert-an-element-at-a-specific-index-in-a-list-and-return-the-updated-list
# https://stackoverflow.com/questions/34753872/how-do-i-display-the-index-of-a-list-element-in-python

# https://stackoverflow.com/questions/2294493/how-to-get-the-position-of-a-character-in-python
# https://www.w3schools.com/python/ref_func_abs.asp

import math, time
# make a class for the board state
class BoardState:
    def __init__(self, dimension = 3):
        # board 
        self.dimension = dimension
        self.board = [ ["_", "_", "_"],
                       ["_", "_", "_"],
                       ["_", "_", "_"]
                     ]
        
        # game state
        self.moves = 0
        self.max_moves = dimension * dimension  # To determine when to call it a draw
        
        self.node_count = 0

    # function to display our game board
    def display_board(self):
        for i in range(self.dimension):
            for j in range(self.dimension):
                print(f"{self.board[i][j]}", end=" ")  # end with a space
            print()  # newline
    
    def apply_move(self, row, col, is_x):
        if is_x:
            self.board[row][col] = "X" 
        else:
            self.board[row][col] = "O"
        self.moves += 1

    def undo_move(self, row, col):
        self.board[row][col] = "_"
        self.moves -= 1

    # this will check the winner quietly, returning the winning symbol or nothing
    def get_winner(self):
        # check rows
        for row in range(self.dimension):
            if self.board[row][0] != "_" and self.board[row][0] == self.board[row][1] == self.board[row][2]:
                return self.board[row][0]
        # check columns
        for col in range(self.dimension):
            if self.board[0][col] != "_" and self.board[0][col] == self.board[1][col] == self.board[2][col]:
                return self.board[0][col]
        # check diagonals
        if self.board[0][0] != "_" and self.board[0][0] == self.board[1][1] == self.board[2][2]:
            return self.board[0][0]
        if self.board[0][2] != "_" and self.board[0][2] == self.board[1][1] == self.board[2][0]:
            return self.board[0][2]
        return None
    
    # this will announce the winner
    def check_winner(self):
        winner = self.get_winner()
        if winner:
            print(f"Player {winner} wins!")
            return True
        return False    # false if draw
    
    # minmax algorithm to compite best move
    def minmax(self):
        self.node_count += 1

        # Check if the game is over
        winner = self.get_winner()
        if winner is not None or self.moves == 9:
            if winner == "X":
                return 1
            elif winner == "O":
                return -1
            else:
                return 0          

        if self.moves % 2 == 0:   # turn of X
            best_score = -math.inf              # start at -inf so the initial score always gets selected
            for i in range(self.dimension):
                for j in range(self.dimension):
                    if self.board[i][j] == "_": # if empty
                        self.apply_move(i, j, True) # apply a move
                        score = self.minmax()  # recurse to get all children of that move and get a score
                        self.undo_move(i, j)    # undo the move to make way for other moves
                        best_score = max(best_score, score) # get the max since we are maximizing
            return best_score  
        else:   # turn of O
            best_score = math.inf                 
            for i in range(self.dimension):
                for j in range(self.dimension):
                    if self.board[i][j] == "_":
                        self.apply_move(i, j, False)
                        score = self.minmax() 
                        self.undo_move(i, j)
                        best_score = min(best_score, score) # get the min since we are minimizing
            return best_score
        

# main game loop
# if they pass 
def start_game(AI_is_x):
    state = BoardState()

    while True:
        # ai's turn
        if state.moves % 2 == 0 and AI_is_x:
            best_score = -math.inf
            row, col = None, None
            for i in range(state.dimension):
                for j in range(state.dimension):
                    if state.board[i][j] == "_": 
                        state.apply_move(i, j, AI_is_x) # try placing AI's symbol
                        score = state.minmax()  # compute score for the next turn
                        state.undo_move(i, j)   # undo immediately
                        if score > best_score:  # check if it's better than previous
                            best_score = score
                            row, col = i, j
            state.apply_move(row, col, AI_is_x)
        elif state.moves % 2 != 0 and not AI_is_x:
            best_score = +math.inf
            row, col = None, None
            for i in range(state.dimension):
                for j in range(state.dimension):
                    if state.board[i][j] == "_": 
                        state.apply_move(i, j, AI_is_x) # try placing AI's symbol
                        score = state.minmax()  # compute score for the next turn
                        state.undo_move(i, j)   # undo immediately
                        if score < best_score:  # check if it's better than previous
                            best_score = score
                            row, col = i, j
            state.apply_move(row, col, AI_is_x)
        else:
        # human's turn
            choice = int(input("Enter a position[1 to 9]: "))
            if choice not in range(1, 10):
                print("Only pick between 1 to 9!")
                continue

            row = (choice - 1) // state.dimension
            col = (choice - 1) % state.dimension

            if state.board[row][col] != "_":
                print("Spot is already taken!")
                continue
            state.apply_move(row, col, not AI_is_x)

        state.display_board()

        # check winner or draw
        if state.check_winner():
            break
        if state.moves == state.max_moves:
            print("It's a draw!")
            break

while True:
    user_choice = input("Do you want to go first [yes or no]: ").strip().lower()

    if user_choice == "yes":
        AI_goes_first = False
        break
    elif user_choice == "no":
        AI_goes_first = True
        break
    else:
        print("Invalid input. Please type 'yes' or 'no'.\n")

start_game(AI_goes_first)

# testing on a blank board
state = BoardState()
start = time.time()
score = state.minmax()
end = time.time()
print("Naive Minimax:")
print("Nodes explored:", state.node_count)
print("Execution time:", end - start, "seconds")