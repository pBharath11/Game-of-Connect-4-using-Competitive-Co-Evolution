import numpy as np
import pygame
import sys
import math
import random
import copy


#global value declarations
ROW = 6
COLUMN = 7
SQUARE_SIZE = 100
TOKEN_RADIUS = int(SQUARE_SIZE/2 - 5)

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

def check_possible_moves(game_board, token, OFFSET):

    possible_token_slots = []
    #checking horizontally
    for col in range(COLUMN-(OFFSET-1)):
        for row in range(ROW):

            empty_tokens = 0
            value_tokens = 0
            for offset in range(OFFSET): 
                if game_board[row][col+offset] == token:
                    value_tokens += 1
                elif game_board[row][col+offset] == 0:
                    empty_tokens += 1
            if (value_tokens == OFFSET-1 and empty_tokens == 1):
                print('row: '+ str(row))
                print('col: '+ str(col))
                print('empty: '+ str(empty_tokens))
                print('value: '+ str(value_tokens))
                orientation = 'HORIZONTAL'
                possible_token_slots.append((row, col, OFFSET, orientation))
            
    #checking vertically      
    for col in range(COLUMN):
        for row in range(ROW-(OFFSET-1)):

            empty_tokens = 0
            value_tokens = 0
            for offset in range(OFFSET): 
                if game_board[row+offset][col] == token:
                    value_tokens += 1
                elif game_board[row+offset][col] == 0:
                    empty_tokens += 1
            if (value_tokens == OFFSET-1 and empty_tokens == 1):
                print('row: '+ str(row))
                print('col: '+ str(col))
                print('empty: '+ str(empty_tokens))
                print('value: '+ str(value_tokens))
                orientation = 'VERTICAL'
                possible_token_slots.append((row, col, OFFSET, orientation))
            
    #checking for +ve diagonal       
    for col in range(COLUMN-(OFFSET-1)):
        for row in range(ROW-(OFFSET-1)):
            empty_tokens = 0
            value_tokens = 0
            for offset in range(OFFSET): 
                if game_board[row+offset][col+offset] == token:
                    value_tokens += 1
                elif game_board[row+offset][col+offset] == 0:
                    empty_tokens += 1
            if (value_tokens == OFFSET-1 and empty_tokens == 1):
                print('row: '+ str(row))
                print('col: '+ str(col))
                print('empty: '+ str(empty_tokens))
                print('value: '+ str(value_tokens))
                orientation = 'DIAGONAL'
                possible_token_slots.append((row, col, OFFSET, orientation))
    
    #checking for -ve diagonal
    for col in range(COLUMN-(OFFSET-1)):
        for row in range((OFFSET-1), ROW):
            empty_tokens = 0
            value_tokens = 0
            for offset in range(OFFSET): 
                if game_board[row-offset][col+offset] == token:
                    value_tokens += 1
                elif game_board[row-offset][col+offset] == 0:
                    empty_tokens += 1
            if (value_tokens == OFFSET-1 and empty_tokens == 1):
                print('row: '+ str(row))
                print('col: '+ str(col))
                print('empty: '+ str(empty_tokens))
                print('value: '+ str(value_tokens))
                orientation = 'INV_DIAGONAL'
                possible_token_slots.append((row, col, OFFSET, orientation))
    return possible_token_slots


def find_empty_slot(game_board, possible_move_set):
    print('finding empty slot for set:')
    print(possible_move_set)
    print(type(possible_move_set))
    row = possible_move_set[0]
    col = possible_move_set[1]
    offset = possible_move_set[2]
    orientation = possible_move_set[3]
    row_val = None
    col_val = None
    print('Inside empty slot functiobn')
    if orientation == 'HORIZONTAL':
        for col_len in range(offset):
            print('Inside for loop horizontal')
            print('Checking Row: ' + str(row) + ' col: ' + str(col+col_len))
            print('value is: ' + str(game_board[row][col+col_len]) )
            if game_board[row][col+col_len] == 0:
                print('Horizontal fn' + str(row), str(col+col_len))
                row_val = row
                col_val = col+col_len
    elif orientation == 'VERTICAL':
        for row_len in range(offset):
            print('Inside for loop Vertical')
            print('Checking Row: ' + str(row+row_len) + ' col: ' + str(col))
            print('value is: ' + str(game_board[row+row_len][col]) )
            if game_board[row+row_len][col] == 0:
                print('Vertical fn' + str(row+row_len), str(col))
                row_val = row+row_len
                col_val = col
    elif orientation == 'DIAGONAL':
        for len in range(offset):
            print('Inside for loop Diagonal')
            print('Checking Row: ' + str(row+len) + ' col: ' + str(col+len))
            print('value is: ' + str(game_board[row+len][col+len]) )
            if game_board[row+len][col+len] == 0:
                print('Diagonal fn' + str(row+len), str(col+len))
                row_val = row+len
                col_val = col+len
    elif orientation == 'INV_DIAGONAL':
        for len in range(offset):
            print('Inside for loop inverse Diagonal')
            print('Checking Row: ' + str(row-len) + ' col: ' + str(col+len))
            print('value is: ' + str(game_board[row-len][col+len]) )
            if game_board[row-len][col+len] == 0:
                print('Inverse Diagonal fn' + str(row-len), str(col+len))
                row_val = row-len
                col_val = col+len
    else:
        print("Find Empty Slot! Invalid Orientation")
        sys.exit(1)
    return row_val, col_val      

def check_winning_recursive(game_board, token, first_time = False):
    # TODO: Generate col_choice (response[1])
    response = []
    if first_time:
        discard_num = random.randint(0,6)
        while game_board[0][discard_num] == 2:
            discard_num = random.randint(0,6)
        response = (0, discard_num, 1, 'VERTICAL')
        print('TEST first time=' + str(response))
        return response
    
    if len(response) == 0:
        response.append(check_possible_moves(game_board, token, 4))
        #print('4 token moves =')
        #print(response)
        response.append(check_possible_moves(game_board, token, 3))
        #print('3 token moves =')
        #print(response)
        response.append(check_possible_moves(game_board, token, 2))
        #print('2 token moves =')
        #print(response)
        response = [ x for i in response for x in i]
    return response


def find_if_best_move(game_board, token, row, col, offset, orientation, possible_row_move, possible_col_move):
    game_board_copy = game_board
    game_board_copy[possible_row_move][possible_col_move] = token
    token_count = 0
    result = find_if_valid_row_col_for_mutation(row, col, offset, orientation)
    if result:
        if orientation == 'HORIZONTAL':
            for col_len in range(offset):
                print('Inside for loop horizontal for find_if_best_move')
                print('Checking Row: ' + str(row) + ' col: ' + str(col+col_len))
                print('value is: ' + str(game_board[row][col+col_len]) )
                if game_board_copy[row][col+col_len] == token:
                    token_count += 1
        elif orientation == 'VERTICAL':
            for row_len in range(offset):
                print('Inside for loop vertical for find_if_best_move')
                print('Checking Row: ' + str(row+row_len) + ' col: ' + str(col))
                print('value is: ' + str(game_board[row+row_len][col]) )
                if game_board_copy[row+row_len][col] == token:
                    token_count += 1
        elif orientation == 'DIAGONAL':
            for len in range(offset):
                print('Inside for loop diagonal for find_if_best_move')
                print('Checking Row: ' + str(row+len) + ' col: ' + str(col+len))
                print('value is: ' + str(game_board[row+len][col+len]) )
                if game_board_copy[row+len][col+len] == token:
                    token_count += 1
        elif orientation == 'INV_DIAGONAL':
            for len in range(offset):
                print('Inside for loop inverse_Diagonal for find_if_best_move')
                print('Checking Row: ' + str(row-len) + ' col: ' + str(col+len))
                print('value is: ' + str(game_board[row-len][col+len]) )
                if game_board_copy[row-len][col+len] == token:
                    token_count += 1
        if token_count == offset:
            return True
        else:
            return False
    else:
        return False


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
    
    print(new_row,new_col)
    if (0 <= new_row < ROW) and (0 <= new_col < COLUMN):
        return True
    else:
        return False