import numpy as np
import pygame
import sys
import math
import gamemechanics as gm
import random
import copy

#global value declarations
ROW = 6
COLUMN = 7
SQUARE_SIZE = 100
TOKEN_RADIUS = int(SQUARE_SIZE/2 - 5)
MUTATION_RATE = 0.2
GENERATIONS = 10
ORIENTATION_LIST = ['HORIZONTAL', 'VERTICAL', 'DIAGONAL', 'INV_DIAGONAL']
BAD_MOVE = -999
GOOD_MOVE = 30
GREAT_MOVE = 300
MOVE_COUNTER = 0

IS_FIRST_MOVE = True
INITIAL_COL_CHOICE =  random.randint(0,6)
turn = 0
best_possible_moves_for_game = []

#Define colors in RGB
BOARD_BACKGROUND = (222,225,230)
TOKEN_BACKGROUND = (14,15,16)
PLAYER_ONE = (255,0,0)
PLAYER_TWO = (255,255,0)
TOKEN_HOVER_BACKGROUND = (0, 0, 0)

#class Treenode to represent a strategy
class TreeNode:
    #initialising the Tree node object
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

    #returns the node value of the object
    def assign_node_val(self, node_val):
        self.node_val = node_val
    
    #identifies the child node payoff values based on offset
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
    #decides node values and child node values
    def decide_node_values(self):
        self.find_child_node_value_payoff()
        #Initialising the node values for the first time based on offset
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
            #print("Decision is None")
        else:
            #checks if the move is the best move or not and returns a boolean
            decision = gm.find_if_best_move(self.board_status, self.token, self.row_move_start_point, self.col_move_start_point, self.offset_val, self.orientation, self.possible_row_move, self.possible_col_move)
            #fetches the next open row available for the column
            open_row = gm.get_next_open_row(self.board_status, self.possible_col_move)
            if decision:
                if open_row == self.possible_row_move:
                    #if its the best move and the row matches the open row, its considered a great move
                    self.node_val = self.node_val + self.left + self.left + GREAT_MOVE
                #if its the best move but the row does not match the open row, its considered a good move
                self.node_val = self.node_val + self.left + GOOD_MOVE
            else:
                #if both the conditions fail, consider it as a bad move
                self.node_val = self.node_val + self.right + self.right + BAD_MOVE

    #adds a win by updating the root node value
    def add_win(self):
        self.node_val = self.node_val + 1
        self.left = self.left + 1
    #prints the tree object
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
    
    #prints the node value
    def print_node_val(self):
        print(self.node_val)
    
    #fetches the node value
    def fetch_node_value(self):
        #print(self.node_val)
        return self.node_val
    
    #fetches offset
    def fetch_offset(self):
        return self.offset_val
    
    #fetches the row and column values from the object
    def fetch_move_row_col_value(self):
        return self.possible_row_move, self.possible_col_move, self.token
    
    #mutation mechanism
    def mutate(self):
        mutated_self = copy.deepcopy(self)
        orientation_for_mutation = None
        row_start_point_for_mutation = None
        col_start_point_for_mutation = None
        is_valid_result = False
        mutation_probability = random.random() #generates a mutation probability in random
        #print("Mutation probability:" + str(mutation_probability))
        while is_valid_result is False: #generates a set of values for row, column, orientation and checks if its a valid move or not
            orientation_for_mutation = random.choice(ORIENTATION_LIST)
            row_start_point_for_mutation = random.randint(0,(ROW-1))
            col_start_point_for_mutation = random.randint(0,(COLUMN-1))
            is_valid_result = gm.find_if_valid_row_col_for_mutation(row_start_point_for_mutation, col_start_point_for_mutation, self.offset_val, orientation_for_mutation)
        #if mutation probability is greater than mutation rate, the generated values above are updated to the tree object completing mutation
        if mutation_probability > MUTATION_RATE:
            mutated_self.row_move_start_point = col_start_point_for_mutation
            mutated_self.col_move_start_point = row_start_point_for_mutation
            mutated_self.orientation = orientation_for_mutation
        return mutated_self

#finds the best move after evolution
def find_best_move_after_evolution(population1, population2):

    #sorts both teh populations based on root node value
    sorted_pop1 = sorted(population1, key= lambda x:x.fetch_node_value(), reverse=True)
    sorted_pop2 = sorted(population2, key= lambda x:x.fetch_node_value(), reverse=True)
    pop1_best_move_node_val = sorted_pop1[0].fetch_node_value()
    pop2_best_move_node_val = sorted_pop2[0].fetch_node_value()
    pop1_best_move_offset = sorted_pop1[0].fetch_offset()
    pop2_best_move_offset = sorted_pop2[0].fetch_offset()
    if pop1_best_move_offset >= pop2_best_move_offset:              #if population 1 has a better chance of winning based on offset, population 1's best move is taken to maximize winning chances
        best_move = sorted_pop1[0].fetch_move_row_col_value()       
    elif pop1_best_move_offset < pop2_best_move_offset:             #if population 2 has a better chance of winning based on offset, population 2's best move is taken to minimize loss
        best_move = sorted_pop2[0].fetch_move_row_col_value()
    else:                                                           #if both have the same offsets, move is selected based on the node values between the best strategies from the 2 populations
        if pop1_best_move_node_val > pop2_best_move_node_val:
            best_move = sorted_pop1[0].fetch_move_row_col_value()
        else:
            best_move = sorted_pop2[0].fetch_move_row_col_value()
    return best_move

#co-evolution
def co_evolve(tree_set, tree_set_human):
    population1 = copy.deepcopy(tree_set)
    population2 = copy.deepcopy(tree_set_human)
    mutated_population1 = []
    mutated_population2 = []
    population1_size = len(tree_set)
    population2_size = len(tree_set_human)
    win_count = 0
    #loop runs for each generation
    for gen in range(GENERATIONS):
        print("Generation " + str(gen+1) + "/" + str(GENERATIONS))
        for i in range(population1_size):       #outer for loop for iterating  population 1
            population1[i].decide_node_values()  #decides node values for the particular strategy(tree object)
            for j in range(population2_size):   #outer for loop for iterating  population 2
                population2[j].decide_node_values() #decides node values for the particular strategy(tree object)
                if population1[i].node_val >= population2[j].node_val:      #competitions are initiated and the winner is decided based on the root node values of the 2 strategies,
                    population1[i].add_win()                                # and add a win based on who wins
                else:
                    population2[j].add_win()
        #sorting the population based on root node values
        fitness_ranked_population1 = sorted(population1, key= lambda x:x.fetch_node_value(), reverse=True)
        fitness_ranked_population2 = sorted(population2, key= lambda x:x.fetch_node_value(), reverse=True)
        
        #keeping the best half for the next generation (Elitism) 
        for length in range(int(population1_size/2)):
            mutated_population1.append(fitness_ranked_population1[length])
        for length in range(int(population2_size/2)):
            mutated_population2.append(fitness_ranked_population2[length])
        
        #copying results into variables
        fitness_ranked_population1 = mutated_population1
        population1 = mutated_population1
        fitness_ranked_population2 = mutated_population2
        population2 = mutated_population2

        #perform the mutation if the current generation is is less than the total generations
        if gen+1 < GENERATIONS:
            for i in range(len(fitness_ranked_population1)):
                mutated_population1.append(fitness_ranked_population1[i].mutate()) #mutation on the best half individuals for stronger offsprings
            for i in range(len(fitness_ranked_population2)):
                mutated_population2.append(fitness_ranked_population2[i].mutate()) #mutation on the best half individuals for stronger offsprings

            population1 = mutated_population1
            population2 = mutated_population2

        population1_size = len(population1)
        population2_size = len(population2)
        #No. of wins by AI afteer the algorithm finishes
        sum_of_wins = find_best_move_after_evolution(population1,population2)
        if sum_of_wins[2] == 1:
            win_count += 1
    #finds the best move after all the generations
    best_move_after_co_evolution  = find_best_move_after_evolution(population1,population2)
    return best_move_after_co_evolution, win_count    

#draws the GUI of the gameboard after each move
def draw_game_board(game_board):
    for col in range(COLUMN):
        for row in range(ROW):
            pygame.draw.rect(screen, BOARD_BACKGROUND, (col*SQUARE_SIZE, row*SQUARE_SIZE+SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE)) #draws the board background
            pygame.draw.circle(screen, TOKEN_BACKGROUND, (int(col*SQUARE_SIZE+SQUARE_SIZE/2), int(row*SQUARE_SIZE+SQUARE_SIZE+SQUARE_SIZE/2)), TOKEN_RADIUS) #draws the token background

    for col in range(COLUMN):
        for row in range(ROW):        
            if game_board[row][col] == 1: #checks for all the slots that contains player 1's (AI's)  tokens and updates with the respctive colour 
                pygame.draw.circle(screen, PLAYER_ONE, (int(col*SQUARE_SIZE+SQUARE_SIZE/2), screen_height - int(row*SQUARE_SIZE+SQUARE_SIZE/2)), TOKEN_RADIUS)
            elif game_board[row][col] == 2: #checks for all the slots that contains player 2's (Human's)  tokens and updates with the respctive colour 
                pygame.draw.circle(screen, PLAYER_TWO, (int(col*SQUARE_SIZE+SQUARE_SIZE/2), screen_height - int(row*SQUARE_SIZE+SQUARE_SIZE/2)), TOKEN_RADIUS)
    pygame.display.update() #updates the drawing on the GUI


game_board = gm.create_gameboard()
print(game_board)
game_over = False

#GUI initialisation
pygame.init()

#declaring screen width and height
screen_width = COLUMN * SQUARE_SIZE
screen_height = (ROW+1) * SQUARE_SIZE

screen_size = (screen_width, screen_height)

#setting the display mode and drawing the game board as GUI
screen = pygame.display.set_mode(screen_size)
draw_game_board(game_board)
pygame.display.update()

#font initialisation for rendering the text
display_font = pygame.font.SysFont("Verdana", 75)

win_count_list = []

#game loop until the game is not over
while not game_over:
    possible_token_slot_sets = []
    possible_token_slot_sets_human = []
    possible_token_slot_locations = []
    possible_token_slot_locations_human = []
    generated_tree_set = []
    generated_tree_set_human = []
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
                #if its the first move, randomize the position on the board and drop the token
                if IS_FIRST_MOVE:
                    possible_token_slot_sets = gm.check_winning_recursive(game_board, 1, True)
                    IS_FIRST_MOVE = False
                    gm.drop_token(game_board, possible_token_slot_sets[0], possible_token_slot_sets[1], 1)
                else:
                    MOVE_COUNTER += 1
                    #checks the winning recursive function and returns the possible token move sets for both AI and player to compete against the human while evolving
                    possible_token_slot_sets = gm.check_winning_recursive(game_board, 1)
                    possible_token_slot_sets_human = gm.check_winning_recursive(game_board, 2)
                    possible_token_slot_sets_len = len(possible_token_slot_sets)
                    possible_token_slot_sets_human_len = len(possible_token_slot_sets_human)
                    #finds and returns the empty slot in each of the possible token move set for AI
                    for i in range(possible_token_slot_sets_len):
                        possible_token_location_row,possible_token_location_col = gm.find_empty_slot(game_board, possible_token_slot_sets[i])
                        if (possible_token_location_row is None) and (possible_token_location_col is None):     #if its a possible move, but the game board has no empty slots, remove the set from the list
                            possible_token_slot_sets.remove(i)
                            print("(None,None) has occoured")
                        else:
                            #save the empty slot row and column values and generate a treenode object to represent a strategy
                            possible_token_location_var = possible_token_location_row, possible_token_location_col
                            possible_token_slot_locations.append(possible_token_location_var)       
                            generated_tree_set.append(TreeNode(game_board, 1, possible_token_slot_sets[i],possible_token_slot_locations[i] ))
                            generated_tree_set[i].decide_node_values()      #decide node values after generating the tree

                    #finds and returns the empty slot in each of the possible token move set for human
                    for i in range(possible_token_slot_sets_human_len):
                        possible_token_location_row,possible_token_location_col = gm.find_empty_slot(game_board, possible_token_slot_sets_human[i])
                        if (possible_token_location_row is None) and (possible_token_location_col is None):        #if its a possible move, but the game board has no empty slots, remove the set from the list
                            possible_token_slot_sets_human.remove(i)
                            print("(None,None) has occoured")
                        else:
                            #save the empty slot row and column values and generate a treenode object to represent a strategy
                            possible_token_location_var = possible_token_location_row, possible_token_location_col
                            possible_token_slot_locations_human.append(possible_token_location_var)
                            generated_tree_set_human.append(TreeNode(game_board, 2, possible_token_slot_sets_human[i],possible_token_slot_locations_human[i] ))
                            generated_tree_set_human[i].decide_node_values()    #decide node values after generating the tree

                    #best possible move(row, col tuple) and the win count of AI in generations are returned whent he co-evolve function is called performing the competitive co-evolution process 
                    best_possible_move, win_count_num = co_evolve(generated_tree_set, generated_tree_set_human)
                    win_count_list.append(win_count_num)
                    best_possible_moves_for_game.append(best_possible_move)
                    #drop the token at the best possible move decided by the algorithm
                    gm.drop_token(game_board, best_possible_move[0], best_possible_move[1], 1)
                
                #check if it is a winning move, end the game if yes
                if gm.is_winning_move(game_board, 1):
                    display_label = display_font.render("AI Wins!", 1, PLAYER_ONE)
                    screen.blit(display_label, (70,10))
                    print("AI Wins!")
                    game_over = True

            #Player 2's game
            else:
                cursor_posx = event.pos[0]
                col_choice =  int(math.floor(cursor_posx/SQUARE_SIZE))  #takes a mouse click input to identify the column for the token to drop
                if gm.check_isValid_Location(game_board, col_choice):   #checks if it is a valid location or not and returns a boolean
                    open_row = gm.get_next_open_row(game_board, col_choice)     #fetches the net open row for the token to be placed at the selected column 
                    gm.drop_token(game_board, open_row, col_choice, 2)      #drop the token at the given row and column

                    #check if it is a winning move, end the game if yes
                    if gm.is_winning_move(game_board, 2):
                        display_label = display_font.render("Human Wins!", 1, PLAYER_TWO)
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
                print(f"Win counts over the game: {win_count_list}")
                pygame.time.wait(10000)