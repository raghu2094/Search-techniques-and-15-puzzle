#!/usr/bin/env python3


# put your 15 puzzle solver here!

# Fall 2017, B-551 Elements of AI. Prof. Crandall
# Assignment 1, Question 3
# Raghottam Dilip Talwai, Siddharth Jayant Pathak and Yue Chen



# The given problem is to solve the 15 puzzle using A* search technique.
# In A* we use heuristics to find an optimal path to reach the goal state.
# A heuristic has to be admissible and consistent to give an optimal path

# Abstraction

# Set of Valid States: Any state having 15 tiles in any order and a blank tile is a valid state.
# Initial State:  A configuration of 4*4 board including any arrangement of  numbered tiles from 1 to 15 and a  blank tile.
#                 Each tile occupies exactly one place on the board.

# Goal state: A sequential arrangement of tiles starting from 1 to 15 with each tile having a unique position and
#             the blank tile occupying the last position towards the right of the 15th tile.

# Successor Function: This is a variant of the usual 15 puzzle problem wherein a tile can slide at the most 3 places in
#                     left, right , up or down direction in a single move generating 6 possible successors for each state.
#                     Each successor will have a cost and the path taken to reach from the parent state associated with it.

# Edge Weights:-f(s)-  It is the sum of the cost of moving a tile and heuristic cost. f(s)= g(s)+h(s)
#                      The Fringe will pop out the state with the lowest edge weight to get the successors of that state
# Cost Function:-g(s)- The cost of moving one, two or three tiles is considered to be the same.

# Heuristic Function:-h(s)- We are using linear conflict heuristic.
#                                        h(s)= MD/3 + lc *2
#                           where MD is the total Manhattan distance and lc is the number of linear conflicts.

# Manhattan Distance- The Manhattan Distance is the distance between tile's current position and its goal position.
#                     We  are taking the total Manhattan distance for all the tiles and dividing by 3 in order to account
#                     for the fact that in a each move maximum 3 tiles can be moved.

# Linear Conflict: Two tiles Ti and Tj are in a linear conflict if Ti and Tj are in the same line, the goal positions of
#                  Ti and Tj  are both in that line, Ti is to the right of Tj and goal position of Ti is to the left of
#                  the goal position of Tj.(Referred: https://heuristicswiki.wikispaces.com/Linear+Conflict)


# For any given tile, it will have to travel at the least its Manhattan distance to reach its goal position.
# But if it faces any other tile in its path leading into a linear conflict, then two moves will be added to its Manhattan distance
# as one of the two tiles would have to make way for the other so that both tiles reach their goal position.

# In this case 2 moves will be added to the Manhattan distance of both tiles and both these tiles will have to travel
# at the least this distance moves to reach its goal.
# The number of moves required would always be greater than the heuristic value.
# Hence linear conflict heuristic will never overestimate the actual number of moves required and will be admissible.

# Search Algorithm

# We have used designed the code based on the search algorithm 3 for implemeting A*.
# Initial state is checked for the the goal condition. If not then it is added to the fringe
# We have used fringe as s heap structure . The fringe will by default pop the state having the lowest cost first.
# As soon as a state is popped, it is checked for the goal condition, if goal is reached, the path containing moves from
# the initial state is returned. Otherwise the state is checked if it is already in the visited list. If so,then
# the next state with lowest cost is popped from the fringe. If the state is not visited, then it is added to the
# visited list and is expanded to get its successors.
# The heuristic function is called and the total cost of reaching the goal state is calculated.
# If a state is already existing in the fringe with a cost higher than the current cost, then the higher cost is ignored
# and the state is stored in the fringe with the current lower cost.
# If a state doesnt exists in the fringe, it is added to the fringe along with its associated cost
# The steps are repeated until the goal state is found.


# Problems Faced

# The selection of the correct heuristic function was a big task. For problems such as the 15 puzzle, getting an optimal
# solution entirley depends on how strong the heuristic is. We tried first using the Manhattan distance/3 as the heuristic function.
# But though it was giving a solution yet we found it is weak compared to linear conflict heuristic, as for the same input
# state we got a solution in less number of moves.

# Though linear conflict heuristic is admissible and strong compared to other, yet we could not get solution for input states
# requiring large number of moves. We tried executing the code for different test cases and at the most the code could
# solve a puzzle requiring 17 moves to reach the goal state within 3 mins.


# Design Decisions:

# Decided to use search algorithm 3 as this problem will have a large state space and there has to be some mechanism based on
# which only optimal states are expanded and unecessary states are ignored. Using search algorithm 3 served this purpose.

# Used a heapq for fringe. The total cost and the states are stored in a single tupple. The fringe being a heapq will
# automatically pop out the state with the lowest cost. This avoids sorting states in the fringe according to the cost.

# Also implemented a check_parity function which will calculate the number of inversions on the input state and will
# return if the state is solvable or not.
# Referred: http://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/




#SOURCE CODE

import sys
import copy
import timeit
import heapq


goal_state=[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]
s=[] #stores the list of successors. It is a list of lists which each list consisting of the state and the moves
     # taken to reach that state

visited=[] #stores the list of visited states

#To move blank tile in the horizontal direction
def move_horizontal(G,i,j,path):

    move_left=copy.deepcopy(G)
    move_right=copy.deepcopy(G)
    tiles_moved=0 #To store the number of tiles moved, can be 1,2 or 3

    #To move right
    right = j-1
    while right >=0:
        move_right[i][right],move_right[i][right+1]=move_right[i][right+1],move_right[i][right]
        tiles_moved+=1
        s1=copy.deepcopy(move_right)
        if path==' ':
            moves='R'+str(tiles_moved)+str(i+1)
        else:
            moves= path+" "+'R'+str(tiles_moved)+str(i+1)
        s2=[s1,moves]
        #Adding states to the successors list
        s.append(s2)
        right=right-1

    #To move Left
    left = j+1
    tiles_moved=0
    while(left<4):
        move_left[i][left],move_left[i][left-1]=move_left[i][left-1],move_left[i][left]
        tiles_moved+=1
        s1=copy.deepcopy(move_left)
        if path==' ':
            moves='L'+str(tiles_moved)+str(i+1)
        else:
            moves= path+" "+'L'+str(tiles_moved)+str(i+1)
        left=left+1
        s2=[s1,moves]
        s.append(s2)           

#To move blank tile in the vertical direction
def move_vertical(G,i,j,path):
    move_up=copy.deepcopy(G)
    move_down=copy.deepcopy(G)

    #To move Down
    down = i-1
    tiles_moved = 0
    while down>=0 :
        move_down[down][j],move_down[down+1][j]=move_down[down+1][j],move_down[down][j]
        tiles_moved+=1
        s1=copy.deepcopy(move_down)
        if path==' ':
            moves='D'+str(tiles_moved)+str(j+1)
        else:
            moves= path+" "+'D'+str(tiles_moved)+str(j+1)
        s2=[s1,moves]
        s.append(s2)
        down=down-1

    #To move UP                    
    up = i+1
    tiles_moved = 0
    while(up<4):
        move_up[up][j],move_up[up-1][j]=move_up[up-1][j],move_up[up][j]
        tiles_moved+=1
        s1=copy.deepcopy(move_up)
        if path==' ':
            moves='U'+str(tiles_moved)+str(j+1)
        else:
            moves= path+" "+'U'+str(tiles_moved)+str(j+1)
        s2=[s1,moves]
        up = up+1
        s.append(s2)


#Calculates number of linear conflicts.
#Referred https://github.com/jDramaix/SlidingPuzzle/blob/master/src/be/dramaix/ai/slidingpuzzle/server/search/heuristic/LinearConflict.java

def Linear_conflict(LC):
    conflicts=0
    for row in range(4):
        max = -1
        for col in range(4):
            if LC[row][col] != 0 and int((LC[row][col] - 1) / 4) == row:

                if LC[row][col] > max:
                    max = LC[row][col]
                else:

                    conflicts += 2
    for col in range(4):
        max = -1
        for row in range(4):
            if LC[row][col] != 0 and int((LC[row][col] % 4)) == (col + 1)%4 :

                if LC[row][col] > max:
                    max = LC[row][col]
                else:

                    conflicts += 2


    return conflicts


# Calculates Manhattan distance
def manhattan_heuristic(MD):
    heuristic=0
    for x in range(4):
        for y in range(4):
            tile=MD[x][y]
            if tile == 0:
                continue
            else:
                for x_goal , k in enumerate(goal_state):
                    if tile in k:
                     y_goal= k.index(tile)
                     break
                heuristic+= abs(x-x_goal)+abs(y-y_goal)
            

    lc= Linear_conflict(MD)
    return(heuristic/3 + lc)



#Successor function
def successors(G,path):
    for row in range(4):
     for col in range(4):
         if(G[row][col]==0):
             
             move_horizontal(G,row,col,path)
             move_vertical(G,row,col,path)
             return s

#Goal function
def is_goal(s):
    if s==goal_state:
        return True

#To check if a state is already existing in the fringe
def check_infringe(succ,fringe):
    if len(fringe)==0:
        return(0,0,False)
    else:
        
        for i,j in enumerate(fringe):
            if succ == j[1][0]:

                return(i,j[0],True)
            else:
                return(0,0,False)

#15 puzzle solver  
def solve(matrix):
    cost=0
    initial_move=' '
    fringe=[]
    heapq.heappush(fringe,(0,[matrix,initial_move,cost]))
    popped=[]
    
    while len(fringe)>0:
        #Popping lowest cost state
        popped=heapq.heappop(fringe)

        #To store the state popped
        state=popped[-1][0]

        #Storing Moves
        path= popped[-1][1]

        # Checking goal condition
        if is_goal(state):
            print("No of nodes visitied before reaching goal: %d" % (len(visited) - 1))
            return (path)

        #To check if state is already in the visited list
        if state in visited:
            continue
        else:

            #Adding to visited states
            visited.append(state)
            #Cost of moving a tile
            cost= popped[-1][2]+1

            for succ in successors(state, path):

                succ.append(cost)

                #Calculating heuristic
                total_cost = manhattan_heuristic(succ[0])+cost
                index,h1,in_fringe= check_infringe(succ[0],fringe)

                #Checking if a state exists with a larger cost in the fringe
                if in_fringe == True and h1 > total_cost:
                    del fringe[index]
                    heapq.heapify(fringe)
                    heapq.heappush(fringe,(total_cost,succ))

                elif in_fringe == False:
                    #Append successor in the fringe with its total cost
                    heapq.heappush(fringe,(total_cost,succ))
            
            #Clearing the successors list for new iteration
            del s[:]
    return False

#To calculate inversions of a particular input state. Read about it on http://www.geeksforgeeks.org/check-instance-15-puzzle-solvable/
def check_parity(initial_puzzle):

    parity=[ele for l in initial_puzzle for ele in l]
    count = 0
    for i, ele in enumerate(parity):
        if ele == 0:
            pos = int(i / 4)
            continue
        for j in range(i + 1, len(parity)):
            if parity[j] == 0:
                continue
            elif ele > parity[j]:
                count += 1

    pos_above = (4 - pos) % 2
    if (count % 2 == 0 and pos_above != 0) or (count % 2 != 0 and pos_above == 0):
        return True
    else:
        return False


# Main
filename=sys.argv[1]

#Reads input from file
with open(filename,'r') as b1:
    initial_state = [[int(i) for i in line.split()] for line in b1]

print ("Given puzzle is :",initial_state)
if is_goal(initial_state):
        print("Input provided is the goal state ")
else:
    check= check_parity(initial_state)
    if check == False:
        print("Sorry, puzzle not solvable")
    else:
        solution = solve(initial_state)
        if solution:
            print("Solution found")
            print(solution)
    
    

