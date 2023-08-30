import numpy as np
import pygame
import sys
import math
import random


#global value declarations
ROW = 6
COLUMN = 7
SQUARE_SIZE = 100
TOKEN_RADIUS = int(SQUARE_SIZE/2 - 5)

#Define colors in RGB
BOARD_BACKGROUND = (222,225,230)
TOKEN_BACKGROUND = (14,15,16)
PLAYER_ONE = (24,187,156)
PLAYER_TWO = (241,111,247)
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
"""
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
"""




#check for a valid 4th token move and return a boolean value accordingly
def check_winning_move(game_board, token):

    OFFSET = 4
    #checking horizontally
    for col in range(COLUMN-3):
        for row in range(ROW):
            consecutive_tokens = 0
            empty_tokens = 0
            value_tokens = 0
            for offset in range(OFFSET): 
                if game_board[row][col+offset] == token:
                    consecutive_tokens += 1
                    value_tokens += 1
                elif game_board[row][col+offset] == 0:
                    consecutive_tokens += 1
                    empty_tokens += 1
            if empty_tokens == 1:
                orientation = 'HORIZONTAL'
                return row, col, OFFSET, orientation
            
    #checking vertically      
    for col in range(COLUMN):
        for row in range(ROW-3):
            consecutive_tokens = 0
            empty_tokens = 0
            value_tokens = 0
            for offset in range(OFFSET): 
                if game_board[row+offset][col] == token:
                    consecutive_tokens += 1
                    value_tokens += 1
                elif game_board[row+offset][col] == 0:
                    consecutive_tokens += 1
                    empty_tokens += 1
            if empty_tokens == 1:
                orientation = 'VERTICAL'
                return row, col, OFFSET, orientation
            
    #checking for +ve diagonal       
    for col in range(COLUMN-3):
        for row in range(ROW-3):
            consecutive_tokens = 0
            empty_tokens = 0
            value_tokens = 0
            for offset in range(OFFSET): 
                if game_board[row+offset][col+offset] == token:
                    consecutive_tokens += 1
                    value_tokens += 1
                elif game_board[row+offset][col+offset] == 0:
                    consecutive_tokens += 1
                    empty_tokens += 1
            if empty_tokens == 1:
                orientation = 'DIAGONAL'
                return row, col, OFFSET, orientation
    
    #checking for -ve diagonal
    for col in range(COLUMN-3):
        for row in range(3, ROW):
            consecutive_tokens = 0
            empty_tokens = 0
            value_tokens = 0
            for offset in range(OFFSET): 
                if game_board[row-offset][col+offset] == token:
                    consecutive_tokens += 1
                    value_tokens += 1
                elif game_board[row-offset][col+offset] == 0:
                    consecutive_tokens += 1
                    empty_tokens += 1
            if empty_tokens == 1:
                orientation = 'INV_DIAGONAL'
                return row, col, OFFSET, orientation


#check for a 3rd token move and return a boolean value accordingly
def check_third_token_move(game_board, token):

    OFFSET = 3
    #checking horizontally
    for col in range(COLUMN-2):
        for row in range(ROW):
            consecutive_tokens = 0
            empty_tokens = 0
            value_tokens = 0
            for offset in range(OFFSET): 
                if game_board[row][col+offset] == token:
                    consecutive_tokens += 1
                    value_tokens += 1
                elif game_board[row][col+offset] == 0:
                    consecutive_tokens += 1
                    empty_tokens += 1
            if empty_tokens == 1:
                orientation = 'HORIZONTAL'
                return row, col, OFFSET, orientation
            
    #checking vertically      
    for col in range(COLUMN):
        for row in range(ROW-2):
            consecutive_tokens = 0
            empty_tokens = 0
            value_tokens = 0
            for offset in range(OFFSET): 
                if game_board[row+offset][col] == token:
                    consecutive_tokens += 1
                    value_tokens += 1
                elif game_board[row+offset][col] == 0:
                    consecutive_tokens += 1
                    empty_tokens += 1
            if empty_tokens == 1:
                orientation = 'VERTICAL'
                return row, col, OFFSET, orientation
            
    #checking for +ve diagonal       
    for col in range(COLUMN-2):
        for row in range(ROW-2):
            consecutive_tokens = 0
            empty_tokens = 0
            value_tokens = 0
            for offset in range(OFFSET): 
                if game_board[row+offset][col+offset] == token:
                    consecutive_tokens += 1
                    value_tokens += 1
                elif game_board[row+offset][col+offset] == 0:
                    consecutive_tokens += 1
                    empty_tokens += 1
            if empty_tokens == 1:
                orientation = 'DIAGONAL'
                return row, col, OFFSET, orientation
    
    #checking for -ve diagonal
    for col in range(COLUMN-2):
        for row in range(2, ROW):
            consecutive_tokens = 0
            empty_tokens = 0
            value_tokens = 0
            for offset in range(OFFSET): 
                if game_board[row-offset][col+offset] == token:
                    consecutive_tokens += 1
                    value_tokens += 1
                elif game_board[row-offset][col+offset] == 0:
                    consecutive_tokens += 1
                    empty_tokens += 1
            if empty_tokens == 1:
                orientation = 'INV_DIAGONAL'
                return row, col, OFFSET, orientation


#check for a 3rd token move and return a boolean value accordingly
def check_second_token_move(game_board, token):

    OFFSET = 2
    #checking horizontally
    for col in range(COLUMN-1):
        for row in range(ROW):
            consecutive_tokens = 0
            empty_tokens = 0
            value_tokens = 0
            for offset in range(OFFSET): 
                if game_board[row][col+offset] == token:
                    consecutive_tokens += 1
                    value_tokens += 1
                elif game_board[row][col+offset] == 0:
                    consecutive_tokens += 1
                    empty_tokens += 1
            if empty_tokens == 1:
                orientation = 'HORIZONTAL'
                return row, col, OFFSET, orientation
            
    #checking vertically      
    for col in range(COLUMN):
        for row in range(ROW-1):
            consecutive_tokens = 0
            empty_tokens = 0
            value_tokens = 0
            for offset in range(OFFSET): 
                if game_board[row+offset][col] == token:
                    consecutive_tokens += 1
                    value_tokens += 1
                elif game_board[row+offset][col] == 0:
                    consecutive_tokens += 1
                    empty_tokens += 1
            if empty_tokens == 1:
                orientation = 'VERTICAL'
                return row, col, OFFSET, orientation
            
    #checking for +ve diagonal       
    for col in range(COLUMN-1):
        for row in range(ROW-1):
            consecutive_tokens = 0
            empty_tokens = 0
            value_tokens = 0
            for offset in range(OFFSET): 
                if game_board[row+offset][col+offset] == token:
                    consecutive_tokens += 1
                    value_tokens += 1
                elif game_board[row+offset][col+offset] == 0:
                    consecutive_tokens += 1
                    empty_tokens += 1
            if empty_tokens == 1:
                orientation = 'DIAGONAL'
                return row, col, OFFSET, orientation
    
    #checking for -ve diagonal
    for col in range(COLUMN-1):
        for row in range(1, ROW):
            consecutive_tokens = 0
            empty_tokens = 0
            value_tokens = 0
            for offset in range(OFFSET): 
                if game_board[row-offset][col+offset] == token:
                    consecutive_tokens += 1
                    value_tokens += 1
                elif game_board[row-offset][col+offset] == 0:
                    consecutive_tokens += 1
                    empty_tokens += 1
            if empty_tokens == 1:
                orientation = 'INV_DIAGONAL'
                return row, col, OFFSET, orientation
            
def find_empty_slot(game_board, row, col, offset, orientation):
    if orientation == 'HORIZONTAL':
        for col_len in range(offset):
            if game_board[row][col+col_len] == 0:
                return row, col+col_len
    elif orientation == 'VERTICAL':
        for row_len in range(offset):
            if game_board[row+row_len][col] == 0:
                return row+row_len, col
    elif orientation == 'DIAGONAL':
        for col_len in range(offset):
            for row_len in range(offset):
                if game_board[row+row_len][col+col_len] == 0:
                    return row+row_len, col+col_len
    elif orientation == 'INV_DIAGONAL':
        for col_len in range(offset):
            for row_len in range(offset):
                if game_board[row-row_len][col+col_len] == 0:
                    return row-row_len, col+col_len

def check_winning_recursive(game_board, token, col_choice = None):
    if col_choice is not None:
        response = (0,col_choice ,1,"VERTICAL")
    else:
        response = check_winning_move(game_board, token)
        if response is None:
            response = check_third_token_move(game_board, token)
            if response is None:
                response = check_second_token_move(game_board, token)
        print('x =' + response)

    return response
                    
