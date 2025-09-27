# Extent and Purpose of AI Use:
# How much AI did you use in your work, which parts of your work involved the use of AI tools?
   #Although no AI was used, I made used of various resources from the web some of
   #which are explicitly mentioned or commented in the code. Other resources or
   #references I used are:
   #https://www.cse.iitk.ac.in/users/se367/10/presentation_local/Danistopic.html
   #https://www.google.com/url?sa=t&source=web&rct=j&opi=89978449&url=https://www.youtube.com/watch%3Fv%3DtrKjYdBASyQ&ved=2ahUKEwjm-e20hdOPAxUAlFYBHTZ-PMQQtwJ6BAgZEAI&usg=AOvVaw10RfiNc-NuKYBunPUdbiGq
# Responsible Use Justification:
# Explain how you used AI responsibly and ethically in completing the task. 


#dictionary to keep track of index of each grid space
spaces = {1:"_", 2:"_", 3:"_", 4:"_", 5:"_",
          6:"_", 7:"_", 8:"_", 9:"_"}

###### FUNCTIONS ######
def print_board(spaces):
    #Reference for fstring formatting:
    #https://www.w3schools.com/python/python_string_formatting.asp

    #access the spaces dictionary to print the board
    board = (f"{spaces[1]}|{spaces[2]}|{spaces[3]}\n"
             f"{spaces[4]}|{spaces[5]}|{spaces[6]}\n"
             f"{spaces[7]}|{spaces[8]}|{spaces[9]}\n")
    
    print(board)

## commented out function are from tictactoe exer/diagnostic that are
## not used for this exercise
# def check_player(current_player):
#     if current_player % 2 == 0:
#         return "O"
#     else: 
#         return "X"
         
# def print_player(current_player):
#     if current_player % 2 == 0:
#         return "Player 1"
#     else:
#         return "Player 2"

##modified from previous tictactoe exer/diagnostic instead
##of returning true, will return the value to cater to utility function
def check_win(spaces):

        #prev code
        # if (spaces[1] == spaces[2] == spaces[3] != "_") or (spaces[4] == spaces[5] == spaces[6] != "_") or (spaces[7] == spaces[8] == spaces[9] != "_"):
        #     return True
        
        # elif(spaces[1] == spaces[4] == spaces[7] != "_") or (spaces[2] == spaces[5] == spaces[8] != "_") or (spaces[3] == spaces[6] == spaces[9] != "_"):
        #     return True

        # elif(spaces[1] == spaces[5] == spaces[9] != "_") or (spaces[3] == spaces[5] == spaces[7] != "_"):
        #     return True
        # return False


    #rows
    if (spaces[1] == spaces[2] == spaces[3] != "_"):
        return spaces[1] #same symbol/value for each row
    if (spaces[4] == spaces[5] == spaces[6] != "_"):
        return spaces[4]
    if (spaces[7] == spaces[8] == spaces[9] != "_"):
        return spaces[7]
    
    #cols
    if (spaces[1] == spaces[4] == spaces[7] != "_"):
        return spaces[1]
    if (spaces[2] == spaces[5] == spaces[8] != "_"):
        return spaces[2]
    if (spaces[3] == spaces[6] == spaces[9] != "_"):
        return spaces[3]

    #diags
    if (spaces[1] == spaces[5] == spaces[9] != "_"):
        return spaces[1]
    if (spaces[3] == spaces[5] == spaces[7] != "_"):
        return spaces[3]

    #no win
    return None

#utility -> end result
#win -> 1
#loss -> -1
#draw -> 0
#else None
def utility(spaces):
    end_result = check_win(spaces)
    if (end_result == "O"):
        return 1
    elif (end_result == "X"):
        return -1
    elif ("_" not in spaces.values()):
        return 0
    else:
        return None

#correction from first version: used marks to mark possible move
#                                also added if else statement in alpha_beta_search
#                                function. Also fixed logic in the game proper compared
#                                to the first version of the code.

#max -> get max of utility
#    -> then use it as next move
def max_value(spaces, a, b):
    end_result = utility(spaces)
    if (end_result != None):
        return end_result

    else:
        #Reference
        #https://www.geeksforgeeks.org/python/python-infinity/
        m = float('-inf')   #negative infinity
        for i in spaces:
            if spaces[i] == "_":  #check if empty
                spaces[i] = "O"   #mark
                v = min_value(spaces, a, b) #call on min_value() function
                spaces[i] = "_"   # unmark
                m = max(m, v)   #get max
                if (m >= b):    #if at least
                    return m
                a = max(a, m)
        return m

#min -> get minimum of utility
#    -> then use it as next move
def min_value(spaces, a, b):
    end_result = utility(spaces)
    if (end_result != None):
        return end_result

    else:
        m = float('inf') #positive infinity
        for i in spaces:
            if spaces[i] == "_":  #check if empty
                spaces[i] = "X"   #mark
                v = max_value(spaces, a, b) #call on max_value() function
                spaces[i] = "_"   #unmark
                m = min(m, v)   #get min
                if (m <= a):    #if at most
                    return m
                b = min(b, m)
        return m

#minimax - alpha beta search tree
def alpha_beta_search(spaces, player):
    #check if player is max or min
    if player == "O":  #max
        optimal = float("-inf")
        move = None
        for i in spaces:
            if spaces[i] == "_": #check if empty
                spaces[i] = "O" #mark
                value = min_value(spaces, float("-inf"), float("inf")) #call on min_value() function
                spaces[i] = "_" #unmark
                if value > optimal:
                    optimal = value
                    move = i
        return move
    else:  #min
        optimal = float("inf")
        move = None
        for i in spaces:
            if spaces[i] == "_":
                spaces[i] = "X"
                value = max_value(spaces, float("-inf"), float("inf")) #call on max_value() function
                spaces[i] = "_"
                if value < optimal:
                    optimal = value
                    move = i
        return move


##### game proper #####
#flags
playing = True

#let user choose if X or O player
while True:
    player_choice = input("Type 'X' or 'O' to select player: ")
    if player_choice == "X" or player_choice == "O":
        player_turn = "X"  #X is first player
        human = player_choice
        if human == "X":
            ai = "O"
        else:
            ai = "X"
        break
    else:
        print("Invalid Input! Please select from 'X' or 'O'.")


while playing:
    print_board(spaces)

    if utility(spaces) != None:
        final_result = utility(spaces)
        
        if final_result == 1:
            print("O wins!")
        elif final_result == -1:
            print("X wins!")
        else:
            print("It's a draw!")
        break

    if player_turn == human:  # human move
        move = int(input("Enter your move (1-9) and enter '0' to exit game: "))
        
        if move == 0:
            playing = False
            print("Goodbye!")
            break

        if move in spaces:
            if spaces[move] == "_":
                spaces[move] = human  #mark
                player_turn = ai
        
        else:
            print("Invalid move! Try again.")

    else:  #algo move
        move = alpha_beta_search(spaces, ai) #call algo to search for optimal move
        spaces[move] = ai
        player_turn = human

print_board(spaces)