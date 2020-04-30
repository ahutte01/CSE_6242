import numpy as np 
import ast
from util import best_split # Added by Amanda 

import pprint # added by Amanda REMOVE THIS

class DecisionTree(object):
    def __init__(self, max_depth):
        # Initializing the tree as an empty dictionary or list, as preferred
        self.tree = {}
        self.max_depth = max_depth
        pass

    def learn(self, X, y, par_node={}, depth=0):
        tree = self.learnRecursive(X, y)
        self.tree = tree

    def learnRecursive(self, X, y, par_node = {}, depth=0):
        # TODO: Train the decision tree (self.tree) using the the sample X and labels y
        # You will have to make use of the functions in utils.py to train the tree

        # Use the function best_split in util.py to get the best split and 
        # data corresponding to left and right child nodes
        
        # One possible way of implementing the tree:
        #    Each node in self.tree could be in the form of a dictionary:
        #       https://docs.python.org/2/library/stdtypes.html#mapping-types-dict
        #    For example, a non-leaf node with two children can have a 'left' key and  a 
        #    'right' key. You can add more keys which might help in classification
        #    (eg. split attribute and split value)
        ### Implement your code here
        #############################################
        
        #print(depth)
        split_col, split_val, X_left, X_right, y_left, y_right =  best_split(X, y)

        node_dict = {
            "split_col": split_col,
            "split_val": split_val,
            "X": X,
            "y": y,
            "label": None,
            "left": None, # Point to left node_dict child
            "right": None # Point to right node_dict child
        }
    
        # Check if Terminal Node:
        if (depth >= self.max_depth):
            #print("final level", node_dict)
            node_dict['label'] = self.make_leaf(X, y)
            return node_dict

        ones = y.count(1)
        zeros = y.count(0)
        length = len(y)
        if (len(y) < 2):
            node_dict['label'] = self.make_leaf(X, y)
            return node_dict
        # if all y are the same, it is a terminal node too 
        if (ones == length):
            node_dict['label'] = self.make_leaf(X, y)
            return node_dict
        if (zeros == length):
            node_dict['label'] = self.make_leaf(X, y)
            return node_dict
        
        # Keep going until depth is too long 
        if (depth < self.max_depth):
            temp = node_dict
            par_node = temp
            node_dict['left'] = self.learnRecursive(X_left, y_left, node_dict, depth + 1)
            node_dict['right'] = self.learnRecursive(X_right, y_right, node_dict, depth + 1) 
        
        return par_node
        #############################################

    # Categorize as leaf 
    def make_leaf(self, X, y):

        ones = y.count(1)
        zeros = y.count(0)

        label = np.random.randint(2)
        if ones > zeros:
            label = 1
        if zeros > ones:
            label = 0
        return label


    def classify(self, record):
        # TODO: classify the record using self.tree and return the predicted label
        ### Implement your code here
        #############################################
        
        # returns 1 or 0, the label referring to the maxium of items at this node 
        tree = self.tree # Traverse the tree!  

        newlabel = self.anotherClassify(record)
        return(newlabel)
        # Use self.tree to find where this record will go, then classify based on majority vote 
        #############################################

    def anotherClassify(self, record):
        node = self.tree 
        while node['left'] :
            if str(node['split_val']).isnumeric():
                if record[node['split_col']] <= node['split_val']:
                    node = node['left']
                else:
                    node = node['right']
            else: #categorical 
                if record[node['split_col']] == node['split_val']:
                    node = node['left']
                else:
                    node = node['right']
        return node['label'] # When exhausted 

