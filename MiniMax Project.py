#!/usr/bin/env python
# coding: utf-8

# In[1]:


import time #Going to use time metric to compare speed of minimax vs Alpha-Beta

class Game:
    def __init__(self):
        self.initialize_game() #constructor to start game
    
    def initialize_game(self):
        self.current_state = [['.', '.', '.'],
                             ['.', '.', '.'],
                             ['.', '.', '.']] #Game board is initially empty
        self.player_turn = 'X' # set starting player as X
        
    def draw_board(self):
        for i in range(0,3):
            for j in range(0,3): #This is a 3 by 3 array so we want to draw it that way
                print('{}|'.format(self.current_state[i][j]), end = " ") #populates array row by row
            print()
        print()
        
    def is_valid(self, px, py):
        if px < 0 or px > 2 or py < 0 or py > 2: #if the coordinates dont fall within the board return False
            return False
        elif self.current_state[px][py] != '.': #if that position on the board is already filled, return False
            return False
        else:
            return True
        
    def is_end(self): #need a method to check if the game is over
        #There are 4 different checks we must implement: vertical, horizontal and both diagonals
        
        #Check for vertical win (3 X's or O's in a vertical line)
        for i in range(0, 3):
            if (self.current_state[0][i] != '.' and #make sure square is not empty
               self.current_state[0][i] == self.current_state[1][i] and #check if first and second item in the column match
               self.current_state[1][i] == self.current_state[2][i]): #check if second and third item in the colunm match
                return self.current_state[0][i] #return the winning player (either X or O)
            
        #Check for horizontal win
        for i in range(0,3):
            if (self.current_state[i] == {'X', 'X', 'X'}):
                return 'X'
            elif (self.current_state[i] == {'O', 'O', 'O'}):
                return 'O'
            
        #Check for top left to bottom right diagonal win
        if (self.current_state[0][0] != '.' and #make sure top left entry isnt empty
           self.current_state[0][0] == self.current_state[1][1] and #make sure top left has same value as middle middle
           self.current_state[1][1] == self.current_state[2][2]): #make sure middle middle has same value as bottom right
            return self.current_state[0][0]
       
    
    
        #Check for top right to bottom left diagonal win
        if (self.current_state[0][2] != '.' and #make sure top left entry isnt empty
           self.current_state[0][2] == self.current_state[1][1] and #make sure top left has same value as middle middle
           self.current_state[1][1] == self.current_state[2][0]): #make sure middle middle has same value as bottom right
            return self.current_state[0][2]
        
        #Check if no more available square are left in which case game is also over
        for i in range(0,3):
            for j in range(0,3):
                if (self.current_state[i][j] == '.'):
                    return None #no actions should be taken if their are still open spaces on the board
        #If its a tie!
        return '.'
    
    
    #We will say that player 'O' is max
    def max(self):
        #There are 3 possible values for maxv: -1 (loss), 0 (Tie), 1 (Win)
        
        maxv = -2 #We set this to a 'worse than worst' case to initialize
        
        px = None #x-coordinate of next move for this player
        py = None #y-coordinate of next move
        
        result = self.is_end()
        
        if result == 'X':
            return (-1,0,0) #This signifies a loss. If the game is over, we do not care about px, py so we set them to 0
        if result == 'O':
            return (1,0,0) #A Win
        if result == ".":
            return (0,0,0) #A Tie
        
        for i in range(0,3):
            for j in range(0,3):
                if self.current_state[i][j] == '.': # Check if the field is empty
                    self.current_state[i][j] = 'O' #Mark that square as 'O' temporarily
                    (m, min_i, min_j) = self.min() #examines one branch of the game tree
                    
                    #Check if the maxv value must be updated after evaluating a branch
                    if m > maxv: #if there is a move that is more beneficial
                        maxv = m
                        px = i #store coordinates of new move
                        py = j
                    #once we store the values, we set the square back to '.' so we can try other states for better moves
                    self.current_state[i][j] = '.'
        return (maxv, px, py) #returns highest possible value for m and the coordinates of that point
    
    #Now we need a min function for player 'X'
    #Goal for this player is to minimize the value so it will be opposite of max function
    def min(self):
        #Here -1 (Win), 0 (Tie), 1(Loss)
        
        
        minv = 2 #worse than worst case, since 1 is a loss
        #qx and qy are the x and y coordinates of the best move for this player
        qx = None
        qy = None
        
        result = self.is_end() #Will return None if game is not over
        
        if result == 'X':
            return (-1,0,0) #This signifies a Win. If the game is over, we do not care about qx, qy so we set them to 0
        if result == 'O':
            return (1,0,0) #A Loss
        if result == ".":
            return (0,0,0) #A Tie  
        
        for i in range(0,3):
            for j in range(0,3):
                if self.current_state[i][j] == '.': # Check if the field is empty
                    self.current_state[i][j] = 'X' #Mark that square as 'X' temporarily
                    (m, max_i, max_j) = self.max() #examines one branch of the game tree
                    
                    #Check if the minv value must be updated after evaluating a branch
                    if m < minv: #if there is a move that is more beneficial
                        minv = m
                        qx = i #store coordinates of new move
                        qy = j
                    #once we store the values, we set the square back to '.' so we can try other states for better moves
                    self.current_state[i][j] = '.'
        return (minv, qx, qy) #returns highest possible value for m and the coordinates of that point
    
    def optimal_move(self, input_state):
        self.current_state = input_state
        (m, px, py) = self.max()
        return (px, py)
    
    
    #Now we must create a method so we can play against the computer
    def play(self):
        while True:
            self.draw_board() #Draw the board initially and after each move
            self.result = self.is_end() #will return name of winner or None
            
            #Visual output for each outcome
            if self.result != None:
                if self.result == 'X':
                    print('The winner is player X!')
                elif self.result == 'O':
                    print('The winner is player O!')
                elif self.result == '.':
                    print("It's a tie!")
                    
                self.initialize_game() #Reset board if game is over
                return
            
            if self.player_turn == 'X': #if it is our turn
                while True:
                    start = time.time()
                    (m, qx, qy) = self.min() #get the recommended coordinates of next move (qx, qy) using min function
                    end = time.time()
                    print('Evaluation Time: {}s'.format(round(end-start,7)))
                    print('Recommended move: X = {}, Y = {}'.format(qx, qy))
                    
                    px = int(input('Please insert an X coordinate: '))
                    py = int(input('Please insert a Y coordinate: '))
                    
                    (qx, qy) = (px, py) #copy coordinates
                    
                    if self.is_valid(px,py): #Check if the entered values are a valid move
                        self.current_state[px][py] = 'X' #Set the desired coordinate to 'X' if possible
                        self.player_turn = 'O' #After our move, we set the turn to the computer (O's)
                        break
                    else:
                        print('Invalid move. Please try again')
            else:
                (m, px, py) = self.max()
                self.current_state[px][py] = 'O' #use the recommended point and mark it as 'O'
                self.player_turn = 'X' #set player turn back to use


# In[3]:


A= Game()
A.play()


# In[7]:


import time

class Game_ab:
    def __init__(self):
        self.initialize_game() #constructor to start game
    
    def initialize_game(self):
        self.current_state = [['.', '.', '.'],
                             ['.', '.', '.'],
                             ['.', '.', '.']] #Game board is initially empty
        self.player_turn = 'X' # set starting player as X
        
    def draw_board(self):
        for i in range(0,3):
            for j in range(0,3): #This is a 3 by 3 array so we want to draw it that way
                print('{}|'.format(self.current_state[i][j]), end = " ") #populates array row by row
            print()
        print()
        
    def is_valid(self, px, py):
        if px < 0 or px > 2 or py < 0 or py > 2: #if the coordinates dont fall within the board return False
            return False
        elif self.current_state[px][py] != '.': #if that position on the board is already filled, return False
            return False
        else:
            return True
        
    def is_end(self): #need a method to check if the game is over
        #There are 4 different checks we must implement: vertical, horizontal and both diagonals
        
        #Check for vertical win (3 X's or O's in a vertical line)
        for i in range(0, 3):
            if (self.current_state[0][i] != '.' and #make sure square is not empty
               self.current_state[0][i] == self.current_state[1][i] and #check if first and second item in the column match
               self.current_state[1][i] == self.current_state[2][i]): #check if second and third item in the colunm match
                return self.current_state[0][i] #return the winning player (either X or O)
            
        #Check for horizontal win
        for i in range(0,3):
            if (self.current_state[i] == {'X', 'X', 'X'}):
                return 'X'
            elif (self.current_state[i] == {'O', 'O', 'O'}):
                return 'O'
            
        #Check for top left to bottom right diagonal win
        if (self.current_state[0][0] != '.' and #make sure top left entry isnt empty
           self.current_state[0][0] == self.current_state[1][1] and #make sure top left has same value as middle middle
           self.current_state[1][1] == self.current_state[2][2]): #make sure middle middle has same value as bottom right
            return self.current_state[0][0]
       
    
    
        #Check for top right to bottom left diagonal win
        if (self.current_state[0][2] != '.' and #make sure top left entry isnt empty
           self.current_state[0][2] == self.current_state[1][1] and #make sure top left has same value as middle middle
           self.current_state[1][1] == self.current_state[2][0]): #make sure middle middle has same value as bottom right
            return self.current_state[0][2]
        
        #Check if no more available square are left in which case game is also over
        for i in range(0,3):
            for j in range(0,3):
                if (self.current_state[i][j] == '.'):
                    return None #no actions should be taken if their are still open spaces on the board
        #If its a tie!
        return '.'
    
    
    #We will say that player 'O' is max
    def max_ab(self, alpha, beta):
        #There are 3 possible values for maxv: -1 (loss), 0 (Tie), 1 (Win)
        
        maxv = -2 #We set this to a 'worse than worst' case to initialize
        
        px = None #x-coordinate of next move for this player
        py = None #y-coordinate of next move
        
        result = self.is_end()
        
        if result == 'X':
            return (-1,0,0) #This signifies a loss. If the game is over, we do not care about px, py so we set them to 0
        if result == 'O':
            return (1,0,0) #A Win
        if result == ".":
            return (0,0,0) #A Tie
        
        for i in range(0,3):
            for j in range(0,3):
                if self.current_state[i][j] == '.': # Check if the field is empty
                    self.current_state[i][j] = 'O' #Mark that square as 'O' temporarily
                    (m, min_i, min_j) = self.min_ab(alpha, beta) #examines one branch of the game tree
                    
                    #Check if the maxv value must be updated after evaluating a branch
                    if m > maxv: #if there is a move that is more beneficial
                        maxv = m
                        px = i #store coordinates of new move
                        py = j
                    #once we store the values, we set the square back to '.' so we can try other states for better moves
                    self.current_state[i][j] = '.'
                    
                    if maxv >= beta:
                        return (maxv, px, py)
                    if maxv > alpha:
                        alpha = maxv
                        
        return (maxv, px, py) #returns highest possible value for m and the coordinates of that point
    
    #Now we need a min function for player 'X'
    #Goal for this player is to minimize the value so it will be opposite of max function
    def min_ab(self, alpha, beta):
        #Here -1 (Win), 0 (Tie), 1(Loss)
        
        
        minv = 2 #worse than worst case, since 1 is a loss
        #qx and qy are the x and y coordinates of the best move for this player
        qx = None
        qy = None
        
        result = self.is_end() #Will return None if game is not over
        
        if result == 'X':
            return (-1,0,0) #This signifies a Win. If the game is over, we do not care about qx, qy so we set them to 0
        if result == 'O':
            return (1,0,0) #A Loss
        if result == ".":
            return (0,0,0) #A Tie  
        
        for i in range(0,3):
            for j in range(0,3):
                if self.current_state[i][j] == '.': # Check if the field is empty
                    self.current_state[i][j] = 'X' #Mark that square as 'X' temporarily
                    (m, max_i, max_j) = self.max_ab(alpha, beta) #examines one branch of the game tree
                    
                    #Check if the minv value must be updated after evaluating a branch
                    if m < minv: #if there is a move that is more beneficial
                        minv = m
                        qx = i #store coordinates of new move
                        qy = j
                    #once we store the values, we set the square back to '.' so we can try other states for better moves
                    self.current_state[i][j] = '.'
                    
                    if minv <= alpha:
                        return (minv, qx, qy)
                    if minv < beta:
                        beta = minv
                        
        return (minv, qx, qy) #returns highest possible value for m and the coordinates of that point
    
    def optimal_move(self, input_state):
        self.current_state = input_state
        (m, px, py) = self.max_ab(-2, 2)
        return (px, py)
    
    
    #Now we must create a method so we can play against the computer
    def play_ab(self):
        while True:
            self.draw_board() #Draw the board initially and after each move
            self.result = self.is_end() #will return name of winner or None
            
            #Visual output for each outcome
            if self.result != None:
                if self.result == 'X':
                    print('The winner is player X!')
                elif self.result == 'O':
                    print('The winner is player O!')
                elif self.result == '.':
                    print("It's a tie!")
                    
                self.initialize_game() #Reset board if game is over
                return
            
            if self.player_turn == 'X': #if it is our turn
                while True:
                    start = time.time()
                    (m, qx, qy) = self.min_ab(-2,2) #get the recommended coordinates of next move (qx, qy) using min_ab function
                    end = time.time()
                    print('Evaluation Time: {}s'.format(round(end-start,7)))
                    print('Recommended move: X = {}, Y = {}'.format(qx, qy))
                    
                    px = int(input('Please insert an X coordinate: '))
                    py = int(input('Please insert a Y coordinate: '))
                    
                    (qx, qy) = (px, py) #copy coordinates
                    
                    if self.is_valid(px,py): #Check if the entered values are a valid move
                        self.current_state[px][py] = 'X' #Set the desired coordinate to 'X' if possible
                        self.player_turn = 'O' #After our move, we set the turn to the computer (O's)
                        break
                    else:
                        print('Invalid move. Please try again')
            else:
                (m, px, py) = self.max_ab(-2, 2) #get best move for AI using max_ab
                self.current_state[px][py] = 'O' #use the recommended point and mark it as 'O'
                self.player_turn = 'X' #set player turn back to use


# In[8]:


B = Game_ab()
B.play_ab()


# In[17]:


C = Game()
C.current_state = [['.','.', 'O'], ['X', 'O', 'O'], ['.', '.', 'X']]
C.play()


# In[20]:


D = Game_ab()
D.current_state = [['.','.', 'O'], ['X', 'O', 'O'], ['.', '.', 'X']]
D.play_ab()


# In[4]:


E = Game()
E.optimal_move([['.','.', 'O'], ['X', 'O', 'O'], ['.', '.', 'X']])


# In[9]:


F = Game_ab()
F.optimal_move([['.','.', 'O'], ['X', 'O', 'O'], ['.', '.', 'X']])


# The optimal move based on both implementations will be to place X in the first row, second column. Hand implementation attached seperately.

# The following are the 3 different inputs tried on both algorithms

# In[11]:


G = Game()
G.play()


# In[13]:


H = Game_ab()
H.play_ab()


# In[14]:


I = Game()
I.play()


# In[15]:


J = Game_ab()
J.play_ab()


# In[16]:


K = Game()
K.play()


# In[17]:


L = Game_ab()
L.play_ab()


# In[ ]:




