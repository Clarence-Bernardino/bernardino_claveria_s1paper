
# Extent and Purpose of AI Use:
# How much AI did you use in your work, which parts of your work involved the use of AI tools?
    #I used AI tools in my base code the 8-puzzle problem. I specifically utilized AI 
    #tools in my move(board, pos) function. 
# Responsible Use Justification:
# Explain how you used AI responsibly and ethically in completing the task.
    #since i was having a difficult time in getting the algorithm for the
    #possible moves the user can do, I inquired on how I can get the value
    #of the new position (when swapped/switched) through mathematical logic, 
    #since I already have the values for the row and column of the 0 or empty slot. 


import time
correct_board = {1: 1, 2: 2, 3: 3, 4: 4, 5: 5, 6: 6, 7: 7, 8: 8, 9: 0}

#reads file from text file
def get_board(file):

    #reference: https://www.geeksforgeeks.org/python/how-to-open-a-file-using-the-with-statement/
    with open(file, 'r') as file:

        per_line = []
        for line in file:
            #references:
            #https://www.w3schools.com/python/ref_string_split.asp
            per_line.append(line.split(";"))

        create_board = []
        for row in per_line:
            for num in row:
                create_board.append(int(num))

        #reference: https://www.geeksforgeeks.org/python/how-to-initialize-a-dictionary-in-python-using-for-loop/
        return {i+1: create_board[i] for i in range(9)}

def print_board(board):
    board = (f"{board[1]}|{board[2]}|{board[3]}\n"
          f"{board[4]}|{board[5]}|{board[6]}\n"
          f"{board[7]}|{board[8]}|{board[9]}\n")
    
    print(board)

#loop to find 0 in board
def empty_slot(board):
    for i in range(1, 10):
        if board[i] == 0:
            return i     
    return False

#similar to move(board, pos) function. finds valid moves in U D R L order
def valid_moves(i):
    #valid moves in U D R L order
    row = (i - 1) // 3
    col = (i - 1) % 3
    moves = []

    if row > 0:
        moves.append(i - 3)
    if row < 2:
        moves.append(i + 3)
    if col < 2:
        moves.append(i + 1)
    if col > 0:
        moves.append(i - 1)
    
    return moves

def result(board, new_pos, empty):

    #swap positions
    if new_pos in valid_moves(empty):
        temp = board[empty]
        board[empty] = board[new_pos]
        board[new_pos] = temp
        return True
    else:
        return False


#finds 0 and moves it
def move(board, pos):
    empty = empty_slot(board)   #get where the position of 0 or "empty space"
    row = (empty - 1) // 3      #divide by 3 to get the row
    col = (empty - 1) % 3       #modulo 3 to get the column
    new = empty                 #new position(switch)

    if pos == "w":
        if row > 0:
            new = empty - 3     #-3 since row is down by 3 positions

    elif pos == "a":
        if col > 0:             
            new = empty - 1     #-1 since going back 1 position

    elif pos == "x":
        if row < 2:
            new = empty + 3     #+3 since row is up by 3 positions

    elif pos == "d":
        if col < 2:
            new = empty + 1     #+1 since going forward 1 position
    else:
        print("Invalid move")
        return False

    return result(board, new, empty)

    
    
def check_win(board):
    return board == correct_board

#heuristic function for counting misplaced tiles
def heuristic(initial_state):
    count = 0

    #excludes blank or 0 tile
    for i in range(1, 10):
        if(initial_state[i] != 0 and initial_state[i] != correct_board[i] ):
            count+=1
    return count


def solve_astar(initial_state, heuristic):
    openList = [(initial_state.copy(), [])] 
    closedList = set()
    visited_count = 0

    while openList:
        #initialize
        bestNode = 0
        bestState, bestPath = openList[0]
        start_g = len(bestPath)  
        start_f = start_g + heuristic(bestState)  #f = g + h

        #find node with lowest f = g + h
        for i in range(len(openList)):
            state = openList[i][0]  #indexing since state is a dictionary
            path = openList[i][1]
            loop_g = len(path)
            loop_f = loop_g + heuristic(state)
            if loop_f < start_f:  #min f
                start_f = loop_f
                bestNode = i

        #pop best node or node with lowest f
        current_state, path = openList.pop(bestNode)
        state = tuple(current_state.values())  #convert to tuple
        visited_count += 1

        if state in closedList:
            continue
        closedList.add(state)

        if check_win(current_state):
            return current_state, path, visited_count

        empty = empty_slot(current_state)
        for i in valid_moves(empty):
            new_state = current_state.copy()
            
            #swap (result(a, b))
            temp = new_state[empty]
            new_state[empty] = new_state[i]
            new_state[i] = temp
            new_state_tuple = tuple(new_state.values()) #make it a tuple to compare 

            if new_state_tuple in closedList:
                continue

            #make new path
            new_path = path + [(empty, i)]
            new_g = len(new_path)
            new_f = new_g + heuristic(new_state)  #f = g + h

            #check if in open list and compare g
            match = False
            for j in range(len(openList)):
                loop_state = openList[j][0]
                loop_path = openList[j][1]
                if tuple(loop_state.values()) == new_state_tuple:
                    match = True
                    existing_g = len(loop_path)
                    if new_g < existing_g:
                        openList[j] = (new_state, new_path)
                    break

            if not match:
                openList.append((new_state, new_path))

    return (None, [], visited_count)  #no sol'n found


def solve_bfs(initial_state):

    #set frontier as a copy list and in it contains the initial_state and a list for the paths
    #reference:
    #https://www.w3schools.com/python/ref_list_copy.asp
    frontier = [(initial_state.copy(), [])]

    #visited set
    #reference: 
    #https://www.geeksforgeeks.org/python/python-set-function/
    visited = set()
    visited_count = 0

    while (frontier != []):
        current_state, path = frontier.pop(0)   #remove

        #reference: 
        #https://www.w3schools.com/python/ref_dictionary_values.asp
        state = tuple(current_state.values())   #convert to tuple

        #check if state has been visited
        if state in visited:
            continue
        else:
            visited.add(state)
            visited_count += 1             

        if check_win(current_state):
            #if solved already return current board state and path/s
            return current_state, path, visited_count

        #get position of 0 or "empty space"
        empty = empty_slot(current_state)

        #serves as result(a,b)
        for i in valid_moves(empty):
            new_state = current_state.copy()

            # swap 0 or "empty space" with move in pos i
            temp = new_state[empty]
            new_state[empty] = new_state[i]
            new_state[i] = temp

            #references: 
            #https://www.w3schools.com/python/ref_dictionary_values.asp
            #https://www.geeksforgeeks.org/python/python-tuple-function/
            result_state = tuple(new_state.values())
            if result_state not in visited:
                new_path = path + [(empty, i)]          #record move made for this state(empty)
                frontier.append((new_state, new_path))  #append to frontier
    
    return (None, [], 0)  #no sol'n found
    
def solve_dfs(initial_state):
    #### copy of bfs code ####

    frontier = [(initial_state.copy(), [])]
    visited = set()
    visited_count = 0

    while (frontier != []):
        current_state, path = frontier.pop()  #use .pop()
        state = tuple(current_state.values())

        if state in visited:
            continue
        else:
            visited.add(state)
            visited_count += 1

        if check_win(current_state):
            return current_state, path, visited_count

        empty = empty_slot(current_state)

        for i in valid_moves(empty):
            
            new_state = current_state.copy()
            temp = new_state[empty]
            new_state[empty] = new_state[i]
            new_state[i] = temp     

            #get new path and append to frontier
            new_path = path + [(empty, i)]
            frontier.append((new_state, new_path))
    
    return (None, [], 0)


#game proper
board = get_board("input.txt")

if board == None:
    print("File not found.")
    exit()
else:
    #flags
    playing = True
    moves = 0

    print_board(board)

    while playing:
        choice = input("Enter w(up), a(left), x(down), d(right), b(bfs), or f(dfs): ")

        if choice == "q":
            playing = False
            print("Goodbye!")

        elif choice == "b":
            start = time.time()
            solved, path, visited = solve_bfs(board)
            if solved:
                print("\nSolution found:")
                print_board(solved)

                board = solved

                #print path taken to get to sol'n
                print("Path:")
                for i in path:
                    print(f"{i[0]} - {i[1]}")

                #take length of path
                print("Path Cost: " + str(len(path)))

                #take total states visited
                print("Total states visited: " + str(visited))

                #print time
                print(f"Time taken: {time.time() - start} seconds")

                playing = False
                print("\nSolved! Goodbye!")

            else:
                print("\nNo solution found.")


        elif choice == "f":
            start = time.time()
            solved, path, visited = solve_dfs(board)
            if solved:
                print("\nSolution found:")
                print_board(solved)

                board = solved

                #print path taken to get to sol'n
                print("\nPath:")
                for i in path:
                    print(f"{i[0]} - {i[1]}")

                #take length of path
                print("Path Cost: " + str(len(path)))

                #take total states visited
                print("Total states visited: " + str(visited))

                #print time
                print(f"Time taken: {time.time() - start} seconds")

                playing = False
                print("\nSolved! Goodbye!")

            else:
                print("\nNo solution found.")

        elif choice == "s":
            start = time.time()
            solved, path, visited = solve_astar(board, heuristic)
            if solved:
                print("\nSolution found:")
                print_board(solved)

                board = solved

                #print path taken to get to sol'n
                print("\nPath:")
                for i in path:
                    print(f"{i[0]} - {i[1]}")

                #take length of path
                print("Path Cost: " + str(len(path)))

                #take total states visited
                print("Total states visited: " + str(visited))

                #print time
                print(f"Time taken: {time.time() - start} seconds")


                playing = False
                print("\nSolved! Goodbye!")

        else:
            moved = move(board, choice)
            if moved:
                moves += 1

                print_board(board)

                if check_win(board):
                    print(f"Player {moves % 2 + 1} wins!")
                    playing = False

            else:
                print("Invalid move.")
                continue

            

    if not check_win(board):
        print("Final board:")
        print_board(board)

        print("not solved!")





