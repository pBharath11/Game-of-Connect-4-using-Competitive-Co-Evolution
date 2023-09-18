import numpy as np
import sys
import random

#global value declarations
ROW = 6
COLUMN = 7
SQUARE_SIZE = 100
TOKEN_RADIUS = int(SQUARE_SIZE/2 - 5)
#Define colors in RGB
BOARD_BACKGROUND = (222,225,230)
TOKEN_BACKGROUND = (14,15,16)
PLAYER_ONE = (255,0,0)
PLAYER_TWO = (255,255,0)
TOKEN_HOVER_BACKGROUND = (0, 0, 0)

#defines a gameboard layout
def create_gameboard():
    board = np.zeros((ROW,COLUMN))
    return board

#drop a token from each player onto the game board
def drop_token(game_board, open_row, col_choice, token):
    game_board[open_row][col_choice] = token

#check if the location selected by the player is a valid location or not
def check_isValid_Location(game_board, col_choice):
    return game_board[ROW-1][col_choice] == 0

#checks for the top most open slot in a particular selected row and returns the row if its empty for a token to be filled in
def get_next_open_row(game_board, col_choice):
    for r in range(ROW):
        if game_board[r][col_choice] == 0:
            return r    

#check if the current move made by the player is a winning move or not and return a boolean value accordingly
def is_winning_move(game_board, token):
    #checking horizontally for winning move
    for col in range(COLUMN-3):
        for row in range(ROW):
            if game_board[row][col] == token and game_board[row][col+1] == token and game_board[row][col+2] == token and game_board[row][col+3] == token:
                return True

    #checking vertically for winning move
    for col in range(COLUMN):
        for row in range(ROW-3):
            if game_board[row][col] == token and game_board[row+1][col] == token and game_board[row+2][col] == token and game_board[row+3][col] == token:
                return True
            
    #checking for +ve diagonal
    for col in range(COLUMN-3):
        for row in range(ROW-3):
            if game_board[row][col] == token and game_board[row+1][col+1] == token and game_board[row+2][col+2] == token and game_board[row+3][col+3] == token:
                return True
    
    #checking for -ve diagonal
    for col in range(COLUMN-3):
        for row in range(3, ROW):
            if game_board[row][col] == token and game_board[row-1][col+1] == token and game_board[row-2][col+2] == token and game_board[row-3][col+3] == token:
                return True

#prints the game board in the terminal
def print_board(game_board):
    print(np.flip(game_board,0))


#checks all the possible moves in every valid direction based on the offset
def check_possible_moves(game_board, token, OFFSET):

    possible_token_slots = []
    #checking horizontally in the game space
    for col in range(COLUMN-(OFFSET-1)):
        for row in range(ROW):

            empty_tokens = 0
            value_tokens = 0
            for offset in range(OFFSET):  #checking for possible move set based on offset
                if game_board[row][col+offset] == token:
                    value_tokens += 1
                elif game_board[row][col+offset] == 0:
                    empty_tokens += 1
            if (value_tokens == OFFSET-1 and empty_tokens == 1): #if empty tokens is 1 and value tokens is offset-1, a possible move set is found
                orientation = 'HORIZONTAL'
                possible_token_slots.append((row, col, OFFSET, orientation))
            
    #checking vertically in the game space
    for col in range(COLUMN):
        for row in range(ROW-(OFFSET-1)):

            empty_tokens = 0
            value_tokens = 0
            for offset in range(OFFSET):  #checking for possible move set based on offset
                if game_board[row+offset][col] == token:
                    value_tokens += 1
                elif game_board[row+offset][col] == 0:
                    empty_tokens += 1
            if (value_tokens == OFFSET-1 and empty_tokens == 1):  #if empty tokens is 1 and value tokens is offset-1, a possible move set is found
                orientation = 'VERTICAL'
                possible_token_slots.append((row, col, OFFSET, orientation))
            
    #checking for +ve diagonal in the game space      
    for col in range(COLUMN-(OFFSET-1)):
        for row in range(ROW-(OFFSET-1)):
            empty_tokens = 0
            value_tokens = 0
            for offset in range(OFFSET):  #checking for possible move set based on offset
                if game_board[row+offset][col+offset] == token:
                    value_tokens += 1
                elif game_board[row+offset][col+offset] == 0:
                    empty_tokens += 1
            if (value_tokens == OFFSET-1 and empty_tokens == 1):  #if empty tokens is 1 and value tokens is offset-1, a possible move set is found
                orientation = 'DIAGONAL'
                possible_token_slots.append((row, col, OFFSET, orientation))
    
    #checking for -ve diagonal in the game space
    for col in range(COLUMN-(OFFSET-1)):
        for row in range((OFFSET-1), ROW):
            empty_tokens = 0
            value_tokens = 0
            for offset in range(OFFSET):  #checking for possible move set based on offset
                if game_board[row-offset][col+offset] == token:
                    value_tokens += 1
                elif game_board[row-offset][col+offset] == 0:
                    empty_tokens += 1
            if (value_tokens == OFFSET-1 and empty_tokens == 1):  #if empty tokens is 1 and value tokens is offset-1, a possible move set is found
                orientation = 'INV_DIAGONAL'
                possible_token_slots.append((row, col, OFFSET, orientation))
    return possible_token_slots

#finds the empty slot location give the possible move set
def find_empty_slot(game_board, possible_move_set):
    row = possible_move_set[0]
    col = possible_move_set[1]
    offset = possible_move_set[2]
    orientation = possible_move_set[3]
    row_val = None
    col_val = None
    if orientation == 'HORIZONTAL':
        for col_len in range(offset):
            if game_board[row][col+col_len] == 0: #just checks for occourance of zero in the move set to indicate the slot is empty
                row_val = row
                col_val = col+col_len
    elif orientation == 'VERTICAL':
        for row_len in range(offset):
            if game_board[row+row_len][col] == 0: #just checks for occourance of zero in the move set to indicate the slot is empty
                row_val = row+row_len
                col_val = col
    elif orientation == 'DIAGONAL':
        for len in range(offset):
            if game_board[row+len][col+len] == 0: #just checks for occourance of zero in the move set to indicate the slot is empty
                row_val = row+len
                col_val = col+len
    elif orientation == 'INV_DIAGONAL':
        for len in range(offset):
            if game_board[row-len][col+len] == 0: #just checks for occourance of zero in the move set to indicate the slot is empty
                row_val = row-len
                col_val = col+len
    else:
        print("Find Empty Slot! Invalid Orientation")
        sys.exit(1)
    return row_val, col_val      

#checks for winning potential for every move in the board
def check_winning_recursive(game_board, token, first_time = False):
    response = []
    if first_time and token == 1:           #if its the first time, generate a random value and return the response tuple
        discard_num = random.randint(0,6)
        while game_board[0][discard_num] == 2:
            discard_num = random.randint(0,6)
        response = (0, discard_num, 1, 'VERTICAL')
        return response
    
    if len(response) == 0:                  
        response.append(check_possible_moves(game_board, token, 4)) # check for possible moves with 3 in line and finding for a winning move
        response.append(check_possible_moves(game_board, token, 3)) # check for possible moves with 2 in line and has a possibility of having 3 of them aligned with open rows
        response.append(check_possible_moves(game_board, token, 2)) # check for possible moves with 1 in line and has a possibility of having 2  of them aligned with open rows
        response = [ x for i in response for x in i]
    return response

#find if its the best move
def find_if_best_move(game_board, token, row, col, offset, orientation, possible_row_move, possible_col_move):
    game_board_copy = game_board
    game_board_copy[possible_row_move][possible_col_move] = token
    token_count = 0
    result = find_if_valid_row_col_for_mutation(row, col, offset, orientation) #check if its a valid move which returns a boolean
    if result:
        #checking if the token is placed, does it actually win or not on a copy of the game board
        if orientation == 'HORIZONTAL':
            for col_len in range(offset):
                if game_board_copy[row][col+col_len] == token:
                    token_count += 1
        elif orientation == 'VERTICAL':
            for row_len in range(offset):
                if game_board_copy[row+row_len][col] == token:
                    token_count += 1
        elif orientation == 'DIAGONAL':
            for len in range(offset):
                if game_board_copy[row+len][col+len] == token:
                    token_count += 1
        elif orientation == 'INV_DIAGONAL':
            for len in range(offset):
                if game_board_copy[row-len][col+len] == token:
                    token_count += 1
        if token_count == offset: 
            return True
        else:
            return False
    else:
        return False

#finds if move set breaks the game rules or not the given row, column, offset and orientation
def find_if_valid_row_col_for_mutation(row, col, offset, orientation):

    if orientation == 'HORIZONTAL':
        new_row = row
        new_col = col+offset
    elif orientation == 'VERTICAL':
        new_row = row+offset
        new_col = col
    elif orientation == 'DIAGONAL':
        new_row = row+offset
        new_col = col+offset
    elif orientation == 'INV_DIAGONAL':
        new_row = row-offset
        new_col = col+offset
    
    if (0 <= new_row < ROW) and (0 <= new_col < COLUMN):
        return True
    else:
        return False