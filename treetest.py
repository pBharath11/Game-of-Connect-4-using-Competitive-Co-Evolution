import numpy as np
ROW = 6
COLUMN = 7

class TreeNode:

    def __init__(self, data):
        self.left = None
        self.right = None
        self.data = data
       

    def insert(self, data):
        if (self.data).all():
            if (data < self.data).all():
                if self.left is None:
                    self.left = TreeNode(data)
                else:
                    self.left.insert(data)
            elif (data > self.data).all():
                if self.right is None:
                    self.right = TreeNode(data)
                else:
                    self.right.insert(data)
        else:
            self.data = data
    
    def PrintTree(self):
        if self.left:
            self.left.PrintTree()
        print(self.data),
        if self.right:
            self.right.PrintTree()
    
###def treetestfunction(gameboard, current_pos, player, orientation):


board = np.zeros((ROW,COLUMN))
board1 = np.ones((ROW,COLUMN))


root = TreeNode(board1)
root.insert(board)

root.PrintTree()




