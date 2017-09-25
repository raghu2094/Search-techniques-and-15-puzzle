# put your routing program here!

import heapq
import math


city_routes = {}  #to store the file data in Dictionary
gps = {}          #to store longitude and latitude of Cities

def get_coordinates(city_gps):
    input_file = open(city_gps, "r")
    for line in input_file:
        temp = line.strip().split(" ")
        gps[temp[0]] = (float(temp[1]),float(temp[2]))


def read_input(road_segments):
    '''
        Reads the road-segments data into city_routes Dictionary
    '''
    input_file = open(road_segments, "r")
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


def print_route(goal):
    total_miles = 0
    for i,g in enumerate(goal[2:-1]):
        temp = city_routes[g]
        for x in temp:
            if x[0] == goal[i+3]:
                print "From ",goal[i+2]," to ", x[0], "via ", x[-1][:-1],"(",x[-3]," miles)"
                total_miles = total_miles + int(x[-3])
                break
    print "Total Miles: ", total_miles, "Time Required: ", goal[1], "at average speed of: " , float(total_miles/goal[1]), "mph"


def is_goal(s,end_city):
    return s == end_city


def heuristic(current_city,goal_city="Bloomington,_Indiana"):
    temp_x,temp_y,count = 0,0,0
    if current_city not in gps:
        for neighbours in city_routes[current_city]:
            if neighbours[0] in gps:
                temp_x = temp_x + gps[neighbours[0]][0]
                temp_y = temp_y + gps[neighbours[0]][1]
                count = count + 1
            else:
                for neighbours_2 in city_routes[neighbours[0]]:
                    if neighbours_2[0] in gps:
                        temp_x = temp_x + gps[neighbours_2[0]][0]
                        temp_y = temp_y + gps[neighbours_2[0]][1]
                count = count +1
        x1,y1 = temp_x/count,temp_y/count
    else:
        x1,y1 = gps[current_city]

    x2,y2 = gps[goal_city]
    x1 = math.radians(x1)
    y1 = math.radians(y1)
    x2 = math.radians(x2)
    y2 = math.radians(y2)
    distance = 60.0 * (math.degrees(math.acos(math.sin(x1) * math.sin(x2) \
         + math.cos(x1) * math.cos(x2) * math.cos(y1 - y2))))
    return distance


def successors(temp):
    suc = city_routes[temp[-1]]
    return [ [int(s[-3])+int(temp[0])]+[float(s[-3])/float(s[-2])+float(temp[1])] + temp[2:]+[s[0]] for s in suc]


def successors_cost(temp,cost):
    suc = city_routes[temp[-1]]
    if cost == "distance":
        return [ [int(s[-3])+int(temp[0])]+[int(s[-3])+int(temp[1])]+[float(s[-3])/float(s[-2])+float(temp[2])]+temp[3:]+[s[0]] for s in suc]
    elif cost == "time":
        return [ [float(s[-3])/float(s[-2])+float(temp[0])]+[int(s[-3])+int(temp[1])]+[float(s[-3])/float(s[-2])+float(temp[2])]+temp[3:]+[s[0]] for s in suc]
    elif cost == "longtour":
        return [ [-(int(s[-3]))+int(temp[0])]+[int(s[-3])+int(temp[1])]+[float(s[-3])/float(s[-2])+float(temp[2])]+temp[3:]+[s[0]] for s in suc]
    elif cost == "heuristic":
        return [[int(s[-3]) + int(temp[1]) + heuristic(temp[-1])] + [int(s[-3]) + int(temp[1])] + [float(s[-3]) / float(s[-2]) + float(temp[2])] + temp[3:] + [s[0]] for s in suc]
    return [[1+int(temp[0])]+[int(s[-3])+int(temp[1])]+[float(s[-3])/float(s[-2])+float(temp[2])]+temp[3:]+[s[0]] for s in suc]


def solve_dfs_bfs(start_city = "Abbot_Village,_Maine",end_city="Fairborn,_Ohio",type="bfs"):
    visited = {}
    fringe = []
    fringe.append([0,0,start_city])
    while len(fringe) > 0:
        temp = fringe.pop()
        if temp[-1] in visited:
            pass
        else:
            visited[temp[-1]] = 1
            for s in successors(temp):
                if is_goal(s[-1],end_city):
                    return s
                fringe.append(s)
    return False


def solve_uniform(start_city = "San_Jose,_California",end_city="Bloomington,_Indiana",cost="distance"):
    visited = {}
    fringe = []
    heapq.heappush(fringe,[0,0,0,start_city])
    #fringe.append([0,0,0,start_city])
    while len(fringe) > 0:
        temp = heapq.heappop(fringe)
        #fringe = sorted(fringe,key = itemgetter(0))
        #temp = fringe.pop(0)
        if is_goal(temp[-1],end_city):
            return temp
        if temp[-1] in visited:
            pass
        else:
            visited[temp[-1]] = 1
            for s in successors_cost(temp,cost):
                heapq.heappush(fringe,s)
                #fringe.append(s)
    return False

def solve_a_star(start_city = "San_Jose,_California",end_city="Bloomington,_Indiana",cost="heuristic"):
    visited = {}
    fringe = []
    heapq.heappush(fringe,[0,0,0,start_city])
    #fringe.append([0,0,0,start_city])
    while len(fringe) > 0:
        temp = heapq.heappop(fringe)
        #fringe = sorted(fringe,key = itemgetter(0))
        #temp = fringe.pop(0)
        if is_goal(temp[-1],end_city):
            return temp
        else:
            if temp[-1] in visited:
                if visited[temp[-1]] > temp[0]:
                    visited[temp[-1]] = temp[0]
                else:
                    visited[temp[-1]] = temp[0]
                    continue
            else:
                visited[temp[-1]] = temp[0]
            for s in successors_cost(temp,cost):
                heapq.heappush(fringe,s)
    return False

read_input("road-segments.txt")
get_coordinates("city-gps.txt")
#result = solve_dfs_bfs()
#print result
# print_route(result)
# print result[1:]

print_route(solve_uniform()[1:])
