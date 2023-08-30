import numpy as np
import pygame
import sys
import math

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

#draws the GUI of the gameboard after each move
def draw_game_board(game_board):
    for col in range(COLUMN):
        for row in range(ROW):
            pygame.draw.rect(screen, BOARD_BACKGROUND, (col*SQUARE_SIZE, row*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))
            pygame.draw.circle(screen, TOKEN_BACKGROUND, (int(col*SQUARE_SIZE+SQUARE_SIZE/2), int(row*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)), TOKEN_RADIUS)

    for col in range(COLUMN):
        for row in range(ROW):        
            if game_board[row][col] == 1:
                pygame.draw.circle(screen, PLAYER_ONE, (int(col*SQUARE_SIZE+SQUARE_SIZE/2), screen_height - int(row*SQUARE_SIZE+SQUARE_SIZE/2)), TOKEN_RADIUS)
            elif game_board[row][col] == 2:
                pygame.draw.circle(screen, PLAYER_TWO, (int(col*SQUARE_SIZE+SQUARE_SIZE/2), screen_height - int(row*SQUARE_SIZE+SQUARE_SIZE/2)), TOKEN_RADIUS)
    pygame.display.update()

#prints the game board in the terminal
def print_board(game_board):
    print(np.flip(game_board,0))


game_board = create_gameboard()
print(game_board)
game_over = False
turn = 0

#GUI initialisation
pygame.init()

screen_width = COLUMN * SQUARE_SIZE
screen_height = (ROW+1) * SQUARE_SIZE

screen_size = (screen_width, screen_height)

screen = pygame.display.set_mode(screen_size)
draw_game_board(game_board)
pygame.display.update()

#font initialisation for rendering the text
display_font = pygame.font.SysFont("Verdana", 75)

#game loop until the game is not over
while not game_over:

    #read every interaction in the system with the GUI
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        #detect mouse motion and draw the tokens for each player respectively indicating the player who is currently playing on the top
        if event.type == pygame.MOUSEMOTION:
            pygame.draw.rect(screen, TOKEN_HOVER_BACKGROUND, (0, 0, screen_width, SQUARE_SIZE))
            cursor_posx = event.pos[0]
            if turn == 0:
                pygame.draw.circle(screen, PLAYER_ONE, (cursor_posx, int(SQUARE_SIZE/2)), TOKEN_RADIUS)
            else:
                pygame.draw.circle(screen, PLAYER_TWO, (cursor_posx, int(SQUARE_SIZE/2)), TOKEN_RADIUS)
        
        pygame.display.update()

        #detect mouse click, and drop the player's token into the selected column at the right position and mark it on the GUI
        if event.type == pygame.MOUSEBUTTONDOWN:

            pygame.draw.rect(screen, TOKEN_HOVER_BACKGROUND, (0, 0, screen_width, SQUARE_SIZE))

            #Player 1's game
            if turn == 0:
                cursor_posx = event.pos[0]
                col_choice =  int(math.floor(cursor_posx/SQUARE_SIZE))  #int(input("Player 1's Turn to choose the column(0-6) to insert the token"))
                if check_isValid_Location(game_board, col_choice):
                        open_row = get_next_open_row(game_board, col_choice)
                        drop_token(game_board, open_row, col_choice, 1)

                        if is_winning_move(game_board, 1):
                            display_label = display_font.render("Player 1 Wins!", 1, PLAYER_ONE)
                            screen.blit(display_label, (70,10))
                            print("Player 1 Wins!")
                            game_over = True
                            #break

            #Player 2's game
            else:
                cursor_posx = event.pos[0]
                col_choice =  int(math.floor(cursor_posx/SQUARE_SIZE))  #int(input("Player 2's Turn to choose the column(0-6) to insert the token"))
                if check_isValid_Location(game_board, col_choice):
                    open_row = get_next_open_row(game_board, col_choice)
                    drop_token(game_board, open_row, col_choice, 2)

                    if is_winning_move(game_board, 2):
                        display_label = display_font.render("Player 2 Wins!", 1, PLAYER_TWO)
                        screen.blit(display_label, (70,10))
                        print("Player 2 Wins!")
                        game_over = True
                        #break

            #draw the game board after each players turn with the updated UI
            print_board(game_board)
            draw_game_board(game_board)

            #calculation for indicating the player turn
            turn += 1
            turn = turn % 2

            #wait function after the game ends
            if game_over:
                pygame.time.wait(10000)