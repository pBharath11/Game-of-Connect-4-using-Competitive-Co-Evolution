import numpy as np
import pygame
import sys
import math
import tree_implement as ti
import gamemechanics as gm
import random
import copy

#global value declarations
ROW = 6
COLUMN = 7
SQUARE_SIZE = 100
TOKEN_RADIUS = int(SQUARE_SIZE/2 - 5)
MUTATION_RATE = 0.2
GENERATIONS = 5
ORIENTATION_LIST = ['HORIZONTAL', 'VERTICAL', 'DIAGONAL', 'INV_DIAGONAL']
BAD_MOVE = -999
GOOD_MOVE = 25
GREAT_MOVE = 999

#Define colors in RGB
BOARD_BACKGROUND = (222,225,230)
TOKEN_BACKGROUND = (14,15,16)
PLAYER_ONE = (255,0,0)
PLAYER_TWO = (255,255,0)
TOKEN_HOVER_BACKGROUND = (0, 0, 0)

class TreeNode:
    def __init__(self, board_status, token, possible_move_set, possible_move_location_set):
        self.left = None
        self.right = None
        self.board_status = board_status
        self.token = token
        self.node_val = None
        self.row_move_start_point = possible_move_set[0]
        self.col_move_start_point = possible_move_set[1]
        self.offset_val = possible_move_set[2]
        self.orientation = possible_move_set[3]
        self.possible_row_move = possible_move_location_set[0]
        self.possible_col_move = possible_move_location_set[1]

    def assign_node_val(self, node_val):
        self.node_val = node_val
    
    def find_child_node_value_payoff(self):
        if self.offset_val == 1:
            self.left = 1
            self.right = -1
        elif self.offset_val == 2:
            self.left = 2
            self.right = -2
        elif self.offset_val == 3:
            self.left = 3
            self.right = -3
        elif self.offset_val == 4:
            self.left = 4
            self.right = -4

    def decide_node_values(self):
        self.find_child_node_value_payoff()
        if self.node_val is None:
            self.left = 1
            self.right = -1
            if (self.offset_val-1) == 1:
                self.node_val = 10
            elif (self.offset_val-1) == 2:
                self.node_val = 25
            elif (self.offset_val-1) == 3:
                self.node_val = 50
            elif (self.offset_val - 1) == 4:
                self.node_val = 90
            print("Decision is None")
        else:
            decision = gm.find_if_best_move(self.board_status, self.token, self.row_move_start_point, self.col_move_start_point, self.offset_val, self.orientation, self.possible_row_move, self.possible_col_move)
            print(decision)
            open_row = gm.get_next_open_row(self.board_status, self.possible_col_move)
            if decision:
                if open_row == self.possible_row_move:
                    self.node_val = self.node_val + self.left + self.left + GREAT_MOVE
                self.node_val = self.node_val + self.left + GOOD_MOVE
            else:
                self.node_val = self.node_val + self.right + self.right + BAD_MOVE
            print("Deciding Node values here")

    def add_win(self):
        self.node_val = self.node_val + 1
        self.left = self.left + 1

    def PrintTree(self):
        
        print(self.left)
        print(np.flip(self.board_status,0))
        print(self.token)
        print(self.node_val)
        print(self.row_move_start_point)
        print(self.col_move_start_point)
        print(self.offset_val)
        print(self.orientation)
        print(self.possible_row_move)
        print(self.possible_col_move)
        print(self.right)
    
    def print_node_val(self):
        print(self.node_val)

    def fetch_node_value(self):
        #print(self.node_val)
        return self.node_val
    
    def fetch_move_row_col_value(self):
        return self.possible_row_move, self.possible_col_move
    
    def mutate(self):
        mutated_self = copy.deepcopy(self)
        self.PrintTree()
        orientation_for_mutation = None
        row_start_point_for_mutation = None
        col_start_point_for_mutation = None
        is_valid_result = False
        mutation_probability = random.random()
        print("Mutation probability:" + str(mutation_probability))
        while is_valid_result is False:
            orientation_for_mutation = random.choice(ORIENTATION_LIST)
            row_start_point_for_mutation = random.randint(0,(ROW-1))
            col_start_point_for_mutation = random.randint(0,(COLUMN-1))
            is_valid_result = gm.find_if_valid_row_col_for_mutation(row_start_point_for_mutation, col_start_point_for_mutation, self.offset_val, orientation_for_mutation)
            print('result of valid Mutated row/col: ' + str(is_valid_result))

        if mutation_probability > MUTATION_RATE:
            mutated_self.row_move_start_point = col_start_point_for_mutation
            mutated_self.col_move_start_point = row_start_point_for_mutation
            mutated_self.orientation = orientation_for_mutation
        return mutated_self

def find_best_move_after_evolution(population1, population2):

    sorted_pop1 = sorted(population1, key= lambda x:x.fetch_node_value(), reverse=True)
    sorted_pop2 = sorted(population2, key= lambda x:x.fetch_node_value(), reverse=True)
    pop1_best_move_node_val = sorted_pop1[0].fetch_node_value()
    pop2_best_move_node_val = sorted_pop2[0].fetch_node_value()
    if pop1_best_move_node_val > pop2_best_move_node_val:
        best_move = sorted_pop1[0].fetch_move_row_col_value()
    else:
        best_move = sorted_pop2[0].fetch_move_row_col_value()
    return best_move

def co_evolve(tree_set):
    population1 = copy.deepcopy(tree_set)
    population2 = copy.deepcopy(tree_set)
    mutated_population1 = []
    mutated_population2 = []
    population_size = len(tree_set)

    for gen in range(GENERATIONS):
        print("Generation " + str(gen+1) + "/" + str(GENERATIONS))
        print("Population 1:")
        print(population1)
        print("Population 2:")
        print(population2)
        for i in range(population_size):
            population1[i].PrintTree()
            population1[i].decide_node_values()
            for j in range(population_size):
                population2[j].PrintTree()
                population2[j].decide_node_values()
                if population1[i].node_val >= population2[j].node_val:
                    population1[i].add_win()
                else:
                    population2[j].add_win()
        print("Population 1 Node Values before sorting:")
        for i in range(population_size):
            population1[i].print_node_val()
        fitness_ranked_population1 = sorted(population1, key= lambda x:x.fetch_node_value(), reverse=True)
        print("Population 1 Node Values after sorting:")
        for i in range(population_size):
            fitness_ranked_population1[i].print_node_val()
        print("Population 2 Node Values before sorting:")
        for i in range(population_size):
            population2[i].print_node_val()
        fitness_ranked_population2 = sorted(population2, key= lambda x:x.fetch_node_value(), reverse=True)
        print("Population 2 Node Values after sorting:")
        for i in range(population_size):
            fitness_ranked_population2[i].print_node_val()

        for length in range(int(population_size/2)):
            mutated_population1.append(fitness_ranked_population1[length])
            mutated_population2.append(fitness_ranked_population2[length])
        
        fitness_ranked_population1 = mutated_population1
        fitness_ranked_population2 = mutated_population2
        print(fitness_ranked_population1)
        print(fitness_ranked_population2)
        for i in range(len(fitness_ranked_population1)):
            print("Inside Mutation loop")
            mutated_population1.append(fitness_ranked_population1[i].mutate())
            mutated_population2.append(fitness_ranked_population2[i].mutate())

        population1 = mutated_population1
        population2 = mutated_population2
        population_size = len(population1)

    best_move_after_co_evolution  = find_best_move_after_evolution(population1,population2)
    return best_move_after_co_evolution    

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


game_board = gm.create_gameboard()
print(game_board)
game_over = False
turn = 0
best_possible_moves_for_game = []

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
IS_FIRST_MOVE = True
INITIAL_COL_CHOICE =  random.randint(0,6)


#game loop until the game is not over
while not game_over:
    possible_token_slot_sets = []
    possible_token_slot_locations = []
    generated_tree_set = []
    node_value_set = []
    best_possible_move = None
    GLOBAL_CNTR = 0
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
                if IS_FIRST_MOVE:
                    #print(100000)
                    possible_token_slot_sets = gm.check_winning_recursive(game_board, 1, True)
                    IS_FIRST_MOVE = False
                    gm.drop_token(game_board, possible_token_slot_sets[0], possible_token_slot_sets[1], 1)
                else:
                    possible_token_slot_sets = gm.check_winning_recursive(game_board, 1)
                    print(possible_token_slot_sets)
                    possible_token_slot_sets_len = len(possible_token_slot_sets)
                    for i in range(possible_token_slot_sets_len):
                        #print('Sending below list to find empty slot')
                        #print(possible_token_slot_set)
                        #print(len(possible_token_slot_set))
                        possible_token_location_row,possible_token_location_col = gm.find_empty_slot(game_board, possible_token_slot_sets[i])
                        if (possible_token_location_row is None) and (possible_token_location_col is None):
                            possible_token_slot_sets.remove(i)
                            print("(None,None) has occoured")
                            print("(None,None) has occoured")
                            print("(None,None) has occoured")
                            print("(None,None) has occoured")
                        else:
                            possible_token_location_var = possible_token_location_row, possible_token_location_col
                            possible_token_slot_locations.append(possible_token_location_var)
                            print('empty slot locations:')
                            print(possible_token_slot_locations)
                            print("for")
                            print(possible_token_slot_sets[i])
                            generated_tree_set.append(TreeNode(game_board, 1, possible_token_slot_sets[i],possible_token_slot_locations[i] ))
                            #print("counter value:" + str(GLOBAL_CNTR))
                            #GLOBAL_CNTR += 1
                            generated_tree_set[i].decide_node_values()
                    best_possible_move = co_evolve(generated_tree_set)
                    best_possible_moves_for_game.append(best_possible_move)

                    print("Best Possible Move is:")
                    print(best_possible_move)
                    gm.drop_token(game_board, best_possible_move[0], best_possible_move[1], 1)
                    print(possible_token_slot_sets)
                    print(possible_token_slot_locations)
                    """print('Trees generated for all possible moves:')
                    for cntr in range(len(generated_tree_set)):
                        generated_tree_set[cntr].PrintTree()
                    temp_row = None
                    temp_col = None
                    for i in range(1):
                        temp_var = possible_token_slot_locations[i]
                        temp_row = temp_var[0]
                        temp_col = temp_var[1]
                    drop_token(game_board, temp_row, temp_col, 1)
                """
                #print(type(possible_token_slot_sets))
                
                if gm.is_winning_move(game_board, 1):
                    display_label = display_font.render("AI Wins!", 1, PLAYER_ONE)
                    screen.blit(display_label, (70,10))
                    print("AI Wins!")
                    game_over = True

            #Player 2's game
            else:
                cursor_posx = event.pos[0]
                col_choice =  int(math.floor(cursor_posx/SQUARE_SIZE))  #int(input("Player 2's Turn to choose the column(0-6) to insert the token"))
                if gm.check_isValid_Location(game_board, col_choice):
                    open_row = gm.get_next_open_row(game_board, col_choice)
                    gm.drop_token(game_board, open_row, col_choice, 2)

                    if gm.is_winning_move(game_board, 2):
                        display_label = display_font.render("Player 2 Wins!", 1, PLAYER_TWO)
                        screen.blit(display_label, (70,10))
                        print("Player Wins!")
                        game_over = True
                        #break

            #draw the game board after each players turn with the updated UI
            gm.print_board(game_board)
            draw_game_board(game_board)

            #calculation for indicating the player turn
            turn += 1
            turn = turn % 2

            #wait function after the game ends
            if game_over:
                print('Best possible Moves generated over the course of the game:')
                print(best_possible_moves_for_game)
                pygame.time.wait(10000)