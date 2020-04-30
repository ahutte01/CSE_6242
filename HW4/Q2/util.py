from scipy import stats
import numpy as np

from collections import Counter # this is from Standard Library 

# This method computes entropy for information gain
def entropy(class_y):
    # Input:            
    #   class_y         : list of class labels (0's and 1's)
    
    # TODO: Compute the entropy for a list of classes
    #
    # Example:
    #    entropy([0,0,0,1,1,1,1,1,1]) = 0.92
        
    entropy = 0
    ### Implement your code here
    #############################################

    denominator = len(class_y)
    ones = class_y.count(1) ## count of 1's
    zeros = class_y.count(0) ## count of 0's 

    if ones == 0:
        prob1 = 0
        H1 = 0
    else: 
        prob1 = ones/denominator
        H1 = -prob1*(np.log2(prob1))

    if zeros == 0:
        prob0 = 0
        H0 = 0
    else: 
        prob0 = zeros/denominator
        H0 = -prob0*(np.log2(prob0))
    

    entropy = H1 + H0

    #############################################
    return entropy


def partition_classes(X, y, split_attribute, split_val):
    # Inputs:
    #   X               : data containing all attributes
    #   y               : labels
    #   split_attribute : column index of the attribute to split on
    #   split_val       : either a numerical or categorical value to divide the split_attribute
    
    # TODO: Partition the data(X) and labels(y) based on the split value - BINARY SPLIT.
    # 
    # You will have to first check if the split attribute is numerical or categorical    
    # If the split attribute is numeric, split_val should be a numerical value
    # For example, your split_val could be the mean of the values of split_attribute
    # If the split attribute is categorical, split_val should be one of the categories.   
    #
    # You can perform the partition in the following way
    # Numeric Split Attribute:
    #   Split the data X into two lists(X_left and X_right) where the first list has all
    #   the rows where the split attribute is less than or equal to the split value, and the 
    #   second list has all the rows where the split attribute is greater than the split 
    #   value. Also create two lists(y_left and y_right) with the corresponding y labels.
    #
    # Categorical Split Attribute:
    #   Split the data X into two lists(X_left and X_right) where the first list has all 
    #   the rows where the split attribute is equal to the split value, and the second list
    #   has all the rows where the split attribute is not equal to the split value.
    #   Also create two lists(y_left and y_right) with the corresponding y labels.

    '''
    Example:
    
    X = [[3, 'aa', 10],                 y = [1,
         [1, 'bb', 22],                      1,
         [2, 'cc', 28],                      0,
         [5, 'bb', 32],                      0,
         [4, 'cc', 32]]                      1]
    
    Here, columns 0 and 2 represent numeric attributes, while column 1 is a categorical attribute.
    
    Consider the case where we call the function with split_attribute = 0 and split_val = 3 (mean of column 0)
    Then we divide X into two lists - X_left, where column 0 is <= 3  and X_right, where column 0 is > 3.
    
    X_left = [[3, 'aa', 10],                 y_left = [1,
              [1, 'bb', 22],                           1,
              [2, 'cc', 28]]                           0]
              
    X_right = [[5, 'bb', 32],                y_right = [0,
               [4, 'cc', 32]]                           1]

    Consider another case where we call the function with split_attribute = 1 and split_val = 'bb'
    Then we divide X into two lists, one where column 1 is 'bb', and the other where it is not 'bb'.
        
    X_left = [[1, 'bb', 22],                 y_left = [1,
              [5, 'bb', 32]]                           0]
              
    X_right = [[3, 'aa', 10],                y_right = [1,
               [2, 'cc', 28],                           0,
               [4, 'cc', 32]]                           1]
               
    ''' 
    
    X_left = []
    X_right = []
    
    y_left = []
    y_right = []
    ### Implement your code here
    #############################################

    ## Numerical split
    if str(split_val).isnumeric():
        for i in range(0, len(X)):

            decider = X[i][split_attribute]
            if decider <= split_val:
                X_left.append(X[i])
                y_left.append(y[i])
            if decider > split_val:
                X_right.append(X[i])
                y_right.append(y[i])

    ## Categorial split 
    if str(split_val).isnumeric() == False:
        for i in range(0, len(X)):
            
            decider = X[i][split_attribute]

            if decider == split_val:
                X_left.append(X[i])
                y_left.append(y[i])
            if decider != split_val:
                X_right.append(X[i])
                y_right.append(y[i])

    #############################################
    return (X_left, X_right, y_left, y_right)

    
def information_gain(previous_y, current_y):
    # Inputs:
    #   previous_y: the distribution of original labels (0's and 1's)
    #   current_y:  the distribution of labels after splitting based on a particular
    #               split attribute and split value
    
    # TODO: Compute and return the information gain from partitioning the previous_y labels
    # into the current_y labels.
    # You will need to use the entropy function above to compute information gain
    # Reference: http://www.cs.cmu.edu/afs/cs.cmu.edu/academic/class/15381-s06/www/DTs.pdf
    
    """
    Example:
    
    previous_y = [0,0,0,1,1,1]
    current_y = [[0,0], [1,1,1,0]]
    
    info_gain = 0.45915
    """

    info_gain = 0
    ### Implement your code here
    #############################################
    H = entropy(previous_y)
    
    HL = entropy(current_y[0])
    HR = entropy(current_y[1])

    numL = len(current_y[0])
    numR = len(current_y[1])
    probL = numL / (numL + numR)
    probR = numR / (numL + numR)

    info_gain = H - ( (HL * probL) + (HR * probR))
    #############################################
    return info_gain
    
def best_split(X, y):
    
    if (len(X) > 0):
        d = len(X[0]) # number of attributes
        a = np.arange(d)
        m = np.random.randint(low=1, high=d+1 ) # number of attributes to actually test
        picks = np.random.choice(a, size=m, replace=False).tolist() # Pick the columns to test, by Index 
        
        split_attributes = []
        split_values = []
        X_lefts = []
        X_rights = []
        y_lefts = []
        y_rights = []
        info_gains = [] 

        
        transposed = np.array(X).T.tolist()
        numAttributes = len(transposed)
        
        midpoints = []
        for attrList in transposed:
            if str(attrList[0]).isnumeric():
                attrList = np.array(attrList, dtype = np.float64)
                median = np.median(attrList)
                midpoints.append(median)
            else:
                counts = Counter(attrList).most_common(1)
                mode = counts[0][0]
                midpoints.append(mode)

        for attr in picks:
            split_val = midpoints[attr]
            X_left, X_right, y_left, y_right = partition_classes(X, y, attr, split_val)
            ig = information_gain(y, [y_left, y_right])

            X_lefts.append(X_left)
            X_rights.append(X_right)
            y_lefts.append(y_left)
            y_rights.append(y_right)
            split_attributes.append(attr)
            split_values.append(split_val)
            info_gains.append(ig)

            max_ig = np.amax(info_gains)
            max_ig_ind = np.where(info_gains == np.amax(info_gains))[0][0] # this gives a list of indices of max element 

            best_split_col = split_attributes[max_ig_ind]
            best_split_val = split_values[max_ig_ind]
            best_x_left = X_lefts[max_ig_ind]
            best_x_right = X_rights[max_ig_ind]
            best_y_left = y_lefts[max_ig_ind]
            best_y_right = y_rights[max_ig_ind] 
        return best_split_col, best_split_val, best_x_left, best_x_right, best_y_left, best_y_right 
    return 0, 0, None, None, None, None 



def best_split1(X, y):
    # Inputs:
    #   X       : Data containing all attributes
    #   y       : labels
    # TODO: For each node find the best split criteria and return the 
    # split attribute, spliting value along with 
    # X_left, X_right, y_left, y_right (using partition_classes)
    '''
    
    NOTE: Just like taught in class, don't use all the features for a node.
    Repeat the steps:

    1. Select m attributes out of d available attributes
    2. Pick the best variable/split-point among the m attributes
    3. return the split attributes, split point, left and right children nodes data 

    '''
    
    ### Implement your code here
    #############################################
 
    if (len(X) > 0):
        d = len(X[0]) # number of attributes
 
        a = np.arange(d)
        m = np.random.randint(low=1, high=d+1 ) # number of attributes to actually test
        picks = np.random.choice(a, size=m, replace=False).tolist() # Pick the columns to test, by Index 
        print("picks", picks)
        
        split_attributes = []
        split_values = []
        X_lefts = []
        X_rights = []
        y_lefts = []
        y_rights = []
        info_gains = [] 

        print(X)
        for attr in picks: # this is the split_attribute 
            print("attr column:", attr)
            for i in range(0, len(X)):

                decider = X[i][attr] # this is the split_val 

                X_left, X_right, y_left, y_right = partition_classes(X, y, attr, decider)
                ig = information_gain(y, [y_left, y_right])

                X_lefts.append(X_left)
                X_rights.append(X_right)
                y_lefts.append(y_left)
                y_rights.append(y_right)
                split_attributes.append(attr)
                split_values.append(decider)
                info_gains.append(ig)

            max_ig = np.amax(info_gains)
            max_ig_ind = np.where(info_gains == np.amax(info_gains))[0][0] # this gives a list of indices of max element 
            print("max info gain", max_ig)
            print("index of max info gain", max_ig_ind)

            best_split_col = split_attributes[max_ig_ind]
            best_split_val = split_values[max_ig_ind]
            best_x_left = X_lefts[max_ig_ind]
            best_x_right = X_rights[max_ig_ind]
            best_y_left = y_lefts[max_ig_ind]
            best_y_right = y_rights[max_ig_ind]
        return best_split_col, best_split_val, best_x_left, best_x_right, best_y_left, best_y_right 
    return 0, 0, None, None, None, None 
    #############################################
