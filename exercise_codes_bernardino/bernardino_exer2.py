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

import time
#placeholder for board
board_list = []
board = ""

# read the file line by line
with open ("puzzle06.txt") as file:
    for line in file:           # read line by line
        row = line.strip()      # remove whitespaces
        board_list.append(row)       # add the rows to the board
        
board = "".join(board_list)
board = board.replace(";", "")

print(board)

# a prettier display of the board
def display_board(board):
    print(f"{board[0]} | {board[1]} | {board[2]}")
    print(f"{board[3]} | {board[4]} | {board[5]}")
    print(f"{board[6]} | {board[7]} | {board[8]}")

# display_board()

# function to help find the gap
def find_gap(board):
    if '0' in board:
        return board.index('0')
    return -1
# print(f"gap: {find_gap()}")

# function to find the finished state
def finished_state(board):
    return board == '123456780'

# function to get all possible moves
def get_possible_moves(board):
    # find out where the gap is
    gap_idx = find_gap(board)
    moves = []

    # 0 | 1 | 2
    # 3 | 4 | 5
    # 6 | 7 | 8
   
    # check if the gap can be moved up based from the col and row
    if gap_idx not in (0, 1, 2):  # gap not in top row
        moves.append('w')
        
    # check if the gap can be moved down based from the col and row
    if gap_idx not in (6, 7, 8):  # gap not in bottom row
        moves.append('x')   

    # check if the gap can be moved right based from the col and row
    if gap_idx not in (0, 3, 6):  # gap not in left column
        moves.append('a')

    # check if the gap can be moved left based from the col and row
    if gap_idx not in (2, 5, 8):  # gap not in right column
        moves.append('d')
        
    return moves
    
# print(get_possible_moves(board))
   
# function to apply move, modified table gets returned
def apply_move(board, direction):
    gap_idx = find_gap(board)
    
    board_list = list(board)	# convert to list so it will be mutable
    # print(board_list)
    # ['1', '0', '2', '3', '4', '5', '6', '7', '8']
    
    row = gap_idx // 3		# get the row using integer division 
    col = gap_idx % 3		# get the col using modulo
    # print(row)
    # print(col)
    
    if direction == 'w':
        if row > 0:         # gap not in top row
            swap_idx = gap_idx - 3
        else:
            return board  # invalid move
        
    elif direction == 'x':
        if row < 2:       # gap not in bottom row
            swap_idx = gap_idx + 3
        else:
            return board  # invalid move
        
    elif direction == 'd':
        if col < 2:        # gap not in right column
            swap_idx = gap_idx + 1
        else:
            return board  # invalid move
               
    elif direction == 'a':
        if col > 0:         # gap not in left column
            swap_idx = gap_idx - 1
        else:
            return board  # invalid move
    else:
        return board  # invalid direction
   
    # swap the tile with the gap
    board_list[gap_idx] = board_list[swap_idx]
    board_list[swap_idx] = '0'
    return ''.join(board_list)  # Convert back to string
    
# print(apply_move(board, 'x'))
	
# function to solve the puzzle by BFS

def solve_bfs(initial_state):
    print("in bfs")
    visited = set()	# unique set of boards for the visited boards
    # visited = set(initial_state) will return {1, 2, 3, 4, 5, 6, 7, 8, 9, 0}
    queue = [(initial_state, [])]	# the stack will be a list of tuples (board, path)
    # visited.add(initial_state)  # mark initial state as visited

    # continue until the stack runs out
    while queue:
        # pop the first element (FIFO) and deconstruct the tuple into two variables
        current_board, path = queue.pop(0)

        if current_board in visited:
            continue
        visited.add(current_board)  # mark as expanded
    	
    	# check if the path is already complete
        if finished_state(current_board):
            return path, visited
        
        # explore all possible moves from current state
        for move in get_possible_moves(current_board):
            #print(f"current_board: {current_board}")
            new_board = apply_move(current_board, move)
            # only add to stack if not already visited
            # print(f"new_board: {new_board}, move: {move}")
            # print(f"visited: {visited}")
            if new_board not in visited:
                #print("here")
                # we always add as by definition, sets cannot have duplicates
                queue.append((new_board, path + [move])) # add at the end
   
    return [], visited  # no solution found within depth limit
    
 # function to solve the puzzle by DFS
def solve_dfs(initial_state):
    print("in dfs")
    visited = set()	# unique set of boards for the visited boards
    stack = [(initial_state, [])]	# the stack will be a list of tuples (board, path)
    # visited.add(initial_state)  # Mark initial state as visited

    # continue until the stack runs out
    while stack:
        # pop the first element (FIFO) and deconstruct the tuple into two variables
        current_board, path = stack.pop(-1)
    	
        if current_board in visited:
            continue
        visited.add(current_board)  # mark as expanded

    	# check if the path is already complete
        if finished_state(current_board):
            return path, visited
         
        # explore all possible moves from current state
        for move in get_possible_moves(current_board):
            #print(f"current_board: {current_board}")
            new_board = apply_move(current_board, move)
            # only add to stack if not already visited
            #print(f"new_board: {new_board}, move: {move}")
            #print(f"visited: {visited}")
            if new_board not in visited:
                #print("here")
                # we always add as by definition, sets cannot have duplicates
                stack.append((new_board, path + [move])) # add at the end
    return [], visited  # no solution found within depth limit

# function for computing the heuristic H distance    
def heuristic_manhattan(board):
    goal = '123456780'
    distance = 0
    # find the index where 0 is
    for i, tile in enumerate(board):
        if tile == '0': # skip blank
            continue
        goal_idx = goal.index(tile)
        current_row = i // 3        # convert 1d indices to 2d format for easier processing
        current_col = i % 3
        best_row = goal_idx // 3
        best_col = goal_idx % 3
        distance += abs(current_row - best_row) + abs(current_col - best_col)
    return distance

# function to solve A* star
def solve_astar(initial_state, heuristic):
    print("in A*")
    
    # 1) put the intial state into open with G=0, calculate its H, and calculate F=G+H
    H = heuristic
    open = [(initial_state, [], 0, H)] # the priority queue will be a list of tuples (board, [moves], G, F)
    visited = set() # the visited states
    
    while open:
    # 2) find the lowest F cost in the open set (lowest H cost if tied) and call it current.
        best_idx = 0 # temporary best, this will change as iterations go on
        for i in range(1, len(open)):
            board1, path1, G, F = open[i] # exract tuple contents of the board state
            board_best, path_best, G_best, F_best = open[best_idx] # extract tuple of the the best board state
            # find the lowest F or if tied, lowest H
            if F < F_best or (F == F_best and heuristic_manhattan(board1) < heuristic_manhattan(board_best)):
                best_idx = i        
    
    # 3) remove the lowest F from open and add current state to the visited set
        current, path, G, F = open.pop(best_idx)
        if current in visited:
            continue
        visited.add(current)

    # 4) check if the current is the final state. If yes, return the current.path
        if finished_state(current):
            return path, visited

    # 5) for every possible next state:
    #       generate a new board using the move
    #       skip it if is already in the visited set
    #       compute G (currentG + 1)
    #       compute H (heuristic function)
    #       compute F (G + H)
    #       append the new state to open
        for move in get_possible_moves(current):
            new_board = apply_move(current, move)
            if new_board in visited:
                continue
            new_G = G + 1
            new_H = heuristic_manhattan(new_board)
            new_F = new_G + new_H
            open.append((new_board, path + [move], new_G, new_F))

    return [], visited # for no solutions

    # Main function to start and solve the puzzle
def start_game():
    user_choice = 0
    while user_choice != 4:
        print("Initial board:")
        display_board(board)
        print("=======================")
        print("[1] solve using dfs")
        print("[2] solve using bfs")
        print("[3] solve using A*")
        print("[4] exit")
        user_choice = int(input("Enter your choice: "))
        print("=======================")
        start = time.time() # take time snapshor right before the puzzle is attempted

        # solve the puzzle
        match (user_choice):
            case 1:
                solution, visited = solve_dfs(board)
            case 2:
                solution, visited = solve_bfs(board)
            case 3:
                solution, visited = solve_astar(board, heuristic_manhattan(board))
            case 4:
                print("Goodbye!")
            case _:
                print("Only input 1, 2, 3, or 4!")
        #solution, visited = solve_dfs(board)
        #solution, visited = solve_bfs(board)
        #solution, visited = solve_astar(board)

        end = time.time() # take time snapshor right after the puzzle is attempted
        if solution:
       
            # Display each move in the solution
            current = board

            for i, move in enumerate(solution):
                current = apply_move(current, move)
                print(f"Step#{i + 1} ({move}): ")
                display_board(current)
       
            print("Puzzle solved!")
            print(f"Solution found in {len(solution)} {solution}, Explored stases: {len(visited)}")
            print(f"Time took {(end - start):.10f} seconds")
            print(f"Path cost: {len(solution)}")
            print("Step-by-step solution:")
        else:
            print("No solution found within depth limit")

# start the game
start_game()