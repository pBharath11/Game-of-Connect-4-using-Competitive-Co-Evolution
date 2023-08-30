import numpy as np
import gamemechanics as gm
ROW = 6
COLUMN = 7

class TreeNode:
    def __init__(self, board_status, player_no, orientation, node_val, latest_move_row, latest_move_col):
        self.left = None
        self.right = None
        self.board_status = board_status
        self.player_no = player_no
        self.orientation = orientation
        self.node_val = node_val
        self.latest_move_row = latest_move_row
        self.latest_move_col = latest_move_col

    def insert(self, board_status, player_no, orientation, node_val, latest_move_row, latest_move_col):
        if self.node_val:
            if node_val <= self.node_val:
                if self.left is None:
                    self.left = TreeNode(board_status, player_no, orientation, node_val, latest_move_row, latest_move_col)
                else:
                    self.left.insert(board_status, player_no, orientation, node_val, latest_move_row, latest_move_col)
            elif node_val > self.node_val:
                if self.right is None:
                    self.right = TreeNode(board_status, player_no, orientation, node_val, latest_move_row, latest_move_col)
                else:
                    self.right.insert(board_status, player_no, orientation, node_val, latest_move_row, latest_move_col)
        else:
            self.node_val = node_val
    
    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print(self.board_status)
        print(self.player_no)
        print(self.orientation)
        print(self.node_val)
        print(self.latest_move_row)
        print(self.latest_move_col)
        if self.right:
            self.right.PrintTree()

    

board = np.zeros((ROW,COLUMN))
board1 = np.ones((ROW,COLUMN))


root = TreeNode(board1, 2, 'ROOTNODE', 3, 4, 7)
root.insert(board, 2, 'LEFTNODE', 3, 7, 8)
root.insert(board, 2, 'RIGHTNODE', 4, 7, 8)

root.PrintTree()