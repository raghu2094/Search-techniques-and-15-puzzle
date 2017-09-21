# put your routing program here!


city_routes = {}  #to store the file data in Dictionary


def read_input(file_name):
    '''
        Reads the road-segments data into city_routes Dictionary
    '''
    input_file = open(file_name,"r")
    speed = 0
    for l in input_file:
        temp = l.split(" ")
        if temp[-3] !='' and temp[-2] !='':
            if int(temp[-3]) != 0 and int(temp[-2]) != 0:
                if temp[0] in city_routes:
                    city_routes[temp[0]].append(temp[1:])
                else:
                    city_routes[temp[0]] = [temp[1:]]
                if temp[1] in city_routes:
                    city_routes[temp[1]].append(temp[:1]+temp[2:])
                else:
                    city_routes[temp[1]] = [temp[:1]+temp[2:]]

def is_goal(s,end_city):
    return s == end_city

def successors(temp):
    suc = city_routes[temp[0]]
    return [ [s[0]]+temp[0:-2]+[int(s[-3])+int(temp[-2])]+[float(s[-3])/float(s[-2])+float(temp[-1])] for s in suc]

read_input("road-segments.txt")


def solve_dfs_bfs(start_city = "Abbot_Village,_Maine",end_city="Fairborn,_Ohio",type="bfs"):
    visited = {}
    fringe = []
    fringe.append([start_city,0,0])
    while len(fringe) > 0:
        temp = fringe.pop()
        if temp[0] in visited:
            pass
        else:
            visited[temp[0]] = 1
            for s in successors(temp):
                if is_goal(s[0],end_city):
                    return s
                fringe.append(s)
    return False

result =  solve_dfs_bfs()

print result[::-1]
