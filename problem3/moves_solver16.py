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
    
    A=copy.deepcopy(G)
    
    A1=copy.deepcopy(G)
    tiles_moved=0

    #To move right
    l=j-1
    
    while l >=0:
        A1[i][l],A1[i][l+1]=A1[i][l+1],A1[i][l]
        tiles_moved+=1
        s1=copy.deepcopy(A1)
        if path==' ':
            moves='R'+str(tiles_moved)+str(i+1)
        else:
            moves= path+" "+'R'+str(tiles_moved)+str(i+1)
        s2=[s1,moves]
        s.append(s2)
        l=l-1
        #print("s is ",s)
        #print("mOVE right DONE")
                    
    #To move Left            
    k=j+1
    tiles_moved=0
    while(k<4):
        A[i][k],A[i][k-1]=A[i][k-1],A[i][k]
                    
        tiles_moved+=1   
        s1=copy.deepcopy(A)
        if path==' ':
            moves='L'+str(tiles_moved)+str(i+1)
        else:
            moves= path+" "+'L'+str(tiles_moved)+str(i+1)
        k=k+1
        s2=[s1,moves]
        s.append(s2)           
        #print("move left done")

#To move blank tile in the vertical direction
def move_vertical(G,i,j,path):
    A=copy.deepcopy(G)
    A1=copy.deepcopy(G)
    #To move Down
    l=i-1
    tiles_moved=0
    while l >=0 :
        A1[l][j],A1[l+1][j]=A1[l+1][j],A1[l][j]
                        
        tiles_moved+=1
        s1=copy.deepcopy(A1)
        if path==' ':
            moves='D'+str(tiles_moved)+str(j+1)
        else:
            moves= path+" "+'D'+str(tiles_moved)+str(j+1)
        
        
        s2=[s1,moves]
        s.append(s2)
        l=l-1
        #print("s is ",s)
        #print("mOVE down DONE")

    #To move UP                    
    k=i+1
    tiles_moved=0  
    while(k<4):
        A[k][j],A[k-1][j]=A[k-1][j],A[k][j]
        tiles_moved+=1
        s1=copy.deepcopy(A)
        if path==' ':
            moves='U'+str(tiles_moved)+str(j+1)
        else:
            moves= path+" "+'U'+str(tiles_moved)+str(j+1)
        s2=[s1,moves]
        k=k+1
        
        s.append(s2)
        #print("move up done")



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
    lin=0
    for row in range(4):
        max = -1
        for col in range(4):
            #print("Element is: %d" % LC[row][col])
            if LC[row][col] != 0 and int((LC[row][col] - 1) / 4) == row:

                if LC[row][col] > max:
                    max = LC[row][col]

                else:
                    #print("Adding")
                    lin += 2

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
                    lin += 2

    #print("Column Conflict is %d" % lin)
    return lin


#Manhattan distance
def manhattan_heuristic(MD):
    sum=0
    for x in range(4):
        for y in range(4):
            tile=MD[x][y]
            
            for x_goal , k in enumerate(goal_state):
                if tile in k:
                    y_goal= k.index(tile)
                    break
            #print("MD for %d is %d"%(tile,abs(i-x_goal)+abs(j-y_goal)) )  
            
            sum+= abs(x-x_goal)+abs(y-y_goal)
            
    print("MD IS: %d" %sum)
    lc= Linear_conflict(MD)
    print("MD with lc is %d" %(sum+lc))
    return(sum+lc)



#Successor function
def successors(G,path):
    for i in range(4):
     for j in range(4):
         if(G[i][j]==0):
             
             move_horizontal(G,i,j,path)
             move_vertical(G,i,j,path)
             return s




def is_goal(s):
    if s==goal_state:
        return True

#To check if a state is already existing in the fringe
def check_infringe(A,fringe):
    if len(fringe)==0:
        return(0,0,False)
    else:
        
        for i,j in enumerate(fringe):
            
            if A == j[1][0]:
                #print(" in fringe",A)
                return(i,j[0],True)
            else:
                return(0,0,False)

#15 puzzle solver  
def solve(matrix):
    cost=0
    mov=0
    
    initial_move=' '
    fringe=[]
    heapq.heappush(fringe,(0, [matrix,initial_move,cost]))
    temp=[]
    
    #print ("fringe is ",fringe)
    
    while len(fringe)>0:
        
        #Popping lowest cost state

        temp=heapq.heappop(fringe)
        
        print("popping with total_cost= %d: "%temp[0])
        
        
        temp1=temp[-1][0]
        
        #Storing Moves
        path= temp[-1][1]
            
        

        #Adding to visited states
        visited.append(temp1)
        

        #Checking goal condition
        if is_goal(temp1):
            
            return(path)

        #Cost of moving a tile
        cost= temp[-1][2]+1
        

        mov+=1
        print("Move No: %d " %(mov)) 
        for s1 in successors(temp1, path):
            print("s1 is ",s1[0])
            
            if s1[0] in visited:
                continue

            s1.append(cost)
            #Calculating heuristic
            #total_cost=misplaced_heuristic(s1[0])+cost
            total_cost = manhattan_heuristic(s1[0])+cost

            index,h1,in_fringe= check_infringe(s1[0],fringe)
            
            
            #Checking if a larger s' exists in fringe
            if h1>total_cost:
                
                del fringe[index]
                heapq.heappush(fringe,(total_cost,s1))

            elif in_fringe==False:
            #Append successor in the fringe
                
                heapq.heappush(fringe,(total_cost,s1))
                
                    
                    
        #print("Fringe after appending is ",fringe)
            
        #Clearing the successors list for new iteration
        s.clear()
        
       
        
    return False


# Main

#filename=input("Enter file name")
filename='input1'

#filename=sys.argv[1]

matrix=[]
    
    
    
with open(filename+'.txt','r') as b1:
    for line in b1:
        line=line.split()
            
        line = [int(i) for i in line]
        matrix.append(line)
print ("initial state is :",matrix)
 
solution = solve(matrix)

if solution:
    print("Solution found")
    print(solution)
    
    
