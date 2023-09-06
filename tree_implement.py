import numpy as np
import gamemechanics as gm
ROW = 6
COLUMN = 7

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

    def decide_child_node_value(self, node_value_set = None):
        if self.node_val is None:
            self.left = 1
            self.right = -1
            if (self.offset_val-1) == 1:
                self.node_val = 2
            elif (self.offset_val-1) == 2:
                self.node_val = 5
            elif (self.offset_val-1) == 3:
                self.node_val = 7
            elif (self.offset_val - 1) == 4:
                self.node_val = 100
            print("Decision is None")
        else:
            decision = gm.find_if_best_move(self.board_status, self.token, self.row_move_start_point, self.col_move_start_point, self.offset_val, self.orientation, self.possible_row_move, self.possible_col_move)
            print(decision)
            if decision:
                self.node_val = self.node_val + self.left
            else:
                self.node_val = self.node_val + self.right
            print("Deciding Node values here")

    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print(np.flip(self.board_status,0))
        print(self.token)
        print(self.node_val)
        print(self.row_move_start_point)
        print(self.col_move_start_point)
        print(self.offset_val)
        print(self.orientation)
        print(self.possible_row_move)
        print(self.possible_col_move)
        if self.right:
            self.right.PrintTree()


    """def insert(self, board_status, token, node_val, possible_move_location_set, possible_move_set):
        if self.node_val:
            if node_val <= self.node_val:
                if self.left is None:
                    self.left = TreeNode(board_status, token, node_val, possible_move_location_set, possible_move_set)
                else:
                    self.left.insert(board_status, token, node_val, possible_move_location_set, possible_move_set)
            elif node_val > self.node_val:
                if self.right is None:
                    self.right = TreeNode(board_status, token, node_val, possible_move_location_set, possible_move_set)
                else:
                    self.right.insert(board_status, token, node_val, possible_move_location_set, possible_move_set)
        else:
            self.node_val = node_val
    """    

"""board = np.zeros((ROW,COLUMN))
board1 = np.ones((ROW,COLUMN))


root = TreeNode(board1, 2, 'ROOTNODE', 3, 4, 7)
root.insert(board, 2, 'LEFTNODE', 3, 7, 8)
root.insert(board, 2, 'RIGHTNODE', 4, 7, 8)

root.PrintTree()
"""