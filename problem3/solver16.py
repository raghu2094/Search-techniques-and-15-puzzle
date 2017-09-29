#!/usr/bin/env python3


# put your 15 puzzle solver here!



import sys
import copy
import timeit
import heapq




goal_state=[[1,2,3,4],[5,6,7,8],[9,10,11,12],[13,14,15,0]]
s=[]
visited=[]


#To move blank tile in the horizontal direction
def move_horizontal(G,i,j,path):
    
    move_left=copy.deepcopy(G)
    move_right=copy.deepcopy(G)
    tiles_moved=0

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
        #print("move left done")

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


#Misplaced Tiles heuristic
def misplaced_heuristic(MP):
    count=0
    for i in range(4):
        for j in range(4):
            if MP[i][j]!=goal_state[i][j]:
               #print("Misplaced tile at %d,%d:"%(i,j))
               count+=1
    return (count/3)

def Linear_conflict(LC):
    conflicts=0
    for row in range(4):
        max = -1
        for col in range(4):
            #print("Element is: %d" % LC[row][col])
            if LC[row][col] != 0 and int((LC[row][col] - 1) / 4) == row:

                if LC[row][col] > max:
                    max = LC[row][col]
                else:
                    #print("Adding")
                    conflicts += 2

    #print("Row Conflict is %d" % lin)
    for col in range(4):
        max = -1
        for row in range(4):
            #print("Element is: %d" % LC[row][col])
            if LC[row][col] != 0 and int((LC[row][col] % 4)) == col + 1:

                if LC[row][col] > max:
                    max = LC[row][col]
                else:
                    #print("Adding")
                    conflicts += 2

    #print("Column Conflict is %d" % lin)
    return conflicts


#Manhattan distance
def manhattan_heuristic(MD):
    heuristic=0
    for x in range(4):
        for y in range(4):
            tile=MD[x][y]
            
            for x_goal , k in enumerate(goal_state):
                if tile in k:
                    y_goal= k.index(tile)
                    break
            #print("MD for %d is %d"%(tile,abs(i-x_goal)+abs(j-y_goal)) )  
            
            heuristic+= abs(x-x_goal)+abs(y-y_goal)
            
    #print("MD IS: %d" %sum)
    lc= Linear_conflict(MD)
    #print("MD with lc is %d" %(sum+lc))
    return(heuristic + lc)



#Successor function
def successors(G,path):
    for row in range(4):
     for col in range(4):
         if(G[row][col]==0):
             
             move_horizontal(G,row,col,path)
             move_vertical(G,row,col,path)
             return s




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
                #print(" in fringe",A)
                return(i,j[0],True)
            else:
                return(0,0,False)

#15 puzzle solver  
def solve(matrix):
    cost=0
    initial_move=' '
    fringe=[]

    heapq.heappush(fringe,(0, [matrix,initial_move,cost]))
    popped=[]
    
    #print ("fringe is ",fringe)
    
    while len(fringe)>0:
        
        #Popping lowest cost state

        popped=heapq.heappop(fringe)

        print("popping with total_cost= %d: "%popped[0])
        state=popped[-1][0]
        
        #Storing Moves
        path= popped[-1][1]
            
        #Adding to visited states
        visited.append(state)

        #Checking goal condition
        if is_goal(state):
            print("No of nodes visitied before reaching goal: %d" %(len(visited)-1))

            return(path)

        #Cost of moving a tile
        cost= popped[-1][2]+1

        for succ in successors(state, path):
            #print("s1 is ",s1[0])
            
            if succ[0] in visited:
                continue

            succ.append(cost)
            #Calculating heuristic
            #total_cost=misplaced_heuristic(s1[0])+cost
            total_cost = manhattan_heuristic(succ[0])+cost

            index,h1,in_fringe= check_infringe(succ[0],fringe)

            #Checking if a larger s' exists in fringe
            if h1>total_cost:
                
                del fringe[index]
                heapq.heappush(fringe,(total_cost,succ))

            elif in_fringe==False:
            #Append successor in the fringe
                
                heapq.heappush(fringe,(total_cost,succ))
            
        #Clearing the successors list for new iteration
        del s[:]
    return False


# Main

filename='input1'
#filename=sys.argv[1]
initial_state=[]
with open(filename+'.txt','r') as b1:
    for line in b1:
        line=line.split()
            
        line = [int(i) for i in line]
        initial_state.append(line)
print ("initial state is :",initial_state)
solution = solve(initial_state)

if solution:
    print("Solution found")
    print(solution)
    
    

