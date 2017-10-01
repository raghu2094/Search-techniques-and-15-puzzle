#B-551 Elements of AI. Prof. Crandall
#Assignment 1, question 1


import heapq
import math
import sys

city_routes = {}  # to store the file data in Dictionary
gps = {}          # to store longitude and latitude of Cities


def get_coordinates(city_gps):
    input_file = open(city_gps, "r")
    for line in input_file:
        temp = line.strip().split(" ")
        gps[temp[0]] = (float(temp[1]), float(temp[2]))


def read_input(road_segments):
    """
        Reads the road-segments data into city_routes Dictionary.
        Ignores routes which have speed or distance as 0 or blank.
    """
    input_file = open(road_segments, "r")
    for l in input_file:
        temp = l.split(" ")
        if temp[-3] != '' and temp[-2] != '':
            if int(temp[-3]) != 0 and int(temp[-2]) != 0:
                if temp[0] in city_routes:
                    city_routes[temp[0]].append(temp[1:])
                else:
                    city_routes[temp[0]] = [temp[1:]]
                if temp[1] in city_routes:
                    city_routes[temp[1]].append(temp[:1]+temp[2:])
                else:
                    city_routes[temp[1]] = [temp[:1]+temp[2:]]


def print_route(end_city, goal):
    """
    Prints the route to the goal in a similar way to Google Maps.
    """
    total_miles,time_required =0,0
    temp_end_city = end_city
    temp = goal[temp_end_city]
    result = []
    while temp[0] is not None:
        result.append(["From ", temp[0], " to ", temp_end_city, "via", temp[-1].strip(), "(", temp[1], " miles)"])
        total_miles = total_miles + float(temp[1])
        time_required = time_required + float(temp[2])
        temp_end_city = temp[0]
        temp = goal[temp_end_city]
    for r in reversed(result):
        for x in r:
            print x,
        print
    temp = goal[end_city]
    result = []
    result.append(end_city)
    while temp[0] is not None:
        result.append(temp[0])
        temp_end_city = temp[0]
        temp = goal[temp_end_city]


    print "Total Miles:", total_miles, "Time Required:", time_required , "at average speed of:", float(total_miles / time_required), "mph"
    print total_miles,time_required,
    for p in result[::-1]:
        print p,


def is_goal(s,end_city):
    """
        Checks if the goal city has reached.
    """
    return s == end_city

def heuristic(current_city,goal_city):
    """
    Returns heuristic value using Great Circle Formula.
    If city or junction doesn't have latitude/longitude info in ctiy-gps file then take average of its neighbour's longitude and latitude.
    """
    temp_x,temp_y,count = 0,0,0
    if current_city not in gps:
        for neighbours in city_routes[current_city]:
            if neighbours[0] in gps:
                temp_x = temp_x + gps[neighbours[0]][0]
                temp_y = temp_y + gps[neighbours[0]][1]
                count = count + 1
        if count != 0:
            x1,y1 = temp_x/count,temp_y/count
        else:
            x1,y1=0,0
    else:
        x1,y1 = gps[current_city]

    x2,y2 = gps[goal_city]
    x1 = math.radians(x1)
    y1 = math.radians(y1)
    x2 = math.radians(x2)
    y2 = math.radians(y2)
    distance = float(69.1105 * (math.degrees(math.acos(math.sin(x1) * math.sin(x2) \
         + math.cos(x1) * math.cos(x2) * math.cos(y1 - y2)))))
    return distance


def successors(temp,cost="bfs/dfs"):
    suc = city_routes[temp[-1]]
    if cost == "distance":
        return [ [int(s[-3])+int(temp[0])]+[int(s[-3])]+[float(s[-3])/float(s[-2])]+[s[-1]]+ [temp[-1]]+ [s[0]] for s in suc]
    elif cost == "time":
        return [ [float(s[-3])/float(s[-2])+float(temp[0])]+[int(s[-3])]+[float(s[-3])/float(s[-2])]+[s[-1]]+[temp[-1]]+[s[0]] for s in suc]
    elif cost == "longtour":
        return [ [-(int(s[-3]))+int(temp[0])]+[int(s[-3])]+[float(s[-3])/float(s[-2])]+[s[-1]]+[temp[-1]]+[s[0]] for s in suc]
    elif cost == "segments":
        return [[1+int(temp[0])]+[int(s[-3])]+[float(s[-3])/float(s[-2])]+[s[-1]]+[temp[-1]]+[s[0]] for s in suc]
    else:
        return [[0]+[int(s[-3])]+[float(s[-3])/float(s[-2])]+[s[-1]]+[temp[-1]]+[s[0]]for s in suc]

def successors_heuristic(temp,cost):
    suc = city_routes[temp[-1]]
    if cost == "distance":
        return [[float(s[-3])+float(temp[1])+heuristic((s[0]),end_city)]+[float(s[-3])+float(temp[1])]+[int(s[-3])]+[float(s[-3])/float(s[-2])]+[s[-1]]+[temp[-1]]+[s[0]] for s in suc]
    elif cost == "time":
        return [[float(s[-3])/float(s[-2])+float(temp[1])+heuristic((s[0]),end_city)/85.0]+[float(s[-3])/float(s[-2])+float(temp[1])]+[int(s[-3])]+[float(s[-3])/float(s[-2])]+[s[-1]]+[temp[-1]]+[s[0]] for s in suc]
    elif cost == "segments":
         return [[1+float(temp[1])+heuristic((s[0]),end_city)/4000]+[1+float(temp[1])]+[int(s[-3])]+[float(s[-3])/float(s[-2])]+[s[-1]]+[temp[-1]]+[s[0]] for s in suc]
    else:
        return [[float(s[-3])+float(temp[1])+heuristic((s[0]),end_city)]+[float(s[-3])+float(temp[1])]+[int(s[-3])]+[float(s[-3])/float(s[-2])]+[s[-1]]+[temp[-1]]+[s[0]] for s in suc]


def solve_dfs_bfs(start_city,end_city,type):
    visited = {}
    fringe = []
    trace_route = {}
    fringe.append([0,0,0,None,None,start_city])
    while len(fringe) > 0:
        if type == "bfs":
            temp = fringe.pop(0)
        else:
            temp = fringe.pop()
        if temp[-1] in visited:
            pass
        else:
            trace_route[temp[-1]] = (temp[-2], temp[1], temp[2], temp[-3])
            visited[temp[-1]] = 1
            for s in successors(temp):
                if is_goal(s[-1],end_city):
                    trace_route[s[-1]] = (s[-2], s[1], s[2], s[-3])
                    return trace_route
                fringe.append(s)
    return False


def solve_uniform(start_city,end_city,cost):
    visited = {}
    fringe = []
    trace_route = {}
    heapq.heappush(fringe,[0,0,0,None,None,start_city])
    while len(fringe) > 0:
        temp = heapq.heappop(fringe)
        if is_goal(temp[-1],end_city):
            trace_route[temp[-1]] = (temp[-2], temp[1], temp[2], temp[-3])
            return trace_route
        if temp[-1] in visited:
            pass
        else:
            trace_route[temp[-1]] = (temp[-2], temp[1], temp[2], temp[-3])
            visited[temp[-1]] = 1
            for s in successors(temp,cost):
                heapq.heappush(fringe,s)
    return False



def solve_a_star(start_city,end_city,cost):
    visited = {}
    fringe = []
    trace_route = {}
    heapq.heappush(fringe,[0,0,0,None,None,start_city])
    while len(fringe) > 0:
        temp = heapq.heappop(fringe)
        if is_goal(temp[-1],end_city):
            trace_route[temp[-1]] = (temp[-2], temp[2], temp[3], temp[-3])
            return trace_route
        if temp[-1] in visited:
            if visited[temp[-1]] > temp[0]:
                visited.pop(temp[-1])
        if temp[-1] in visited:
            pass
        else:
            trace_route[temp[-1]] = (temp[-2], temp[2], temp[3], temp[-3])
            visited[temp[-1]] = temp[0]
            for s in successors_heuristic(temp,cost):
                # If the element is already in fringe with a high value then remove that element.
                # But if we keep both the elements in the fringe then the lower value element will be popped and marked as visited.
                # If it's marked as visited, then even if we pop it next time it won't be explored. Removing element from fringe
                # is increasing the time taken to run, as it searches the whole fringe and sorts it again after removing.
                # Reference: Piazza Question 151.
                # for i,s1 in enumerate(fringe):
                #     if s1[-1] == s[-1]:
                #         if s1[0] > s[0]:
                #             fringe.pop(i)
                #             heapq.heapify(fringe)
                heapq.heappush(fringe,s)
    return False


start_city,end_city,routing_algorithm,cost_function = sys.argv[1],sys.argv[2],sys.argv[3],sys.argv[4]

read_input("road-segments.txt")
get_coordinates("city-gps.txt")

if routing_algorithm == "bfs" or routing_algorithm == "dfs":
    print_route(end_city,solve_dfs_bfs(start_city,end_city,routing_algorithm))
elif routing_algorithm == "uniform":
    print_route(end_city,solve_uniform(start_city,end_city,cost_function))
else:
    print_route(end_city,solve_a_star(start_city,end_city,cost_function))



#Test Cases:
# San_Jose,_California Miami,_Florida uniform distance
# San_Jose,_California Miami,_Florida heuristic heuristic
# Seattle,_Washington Bloomington,_Indiana uniform distance
# Seattle,_Washington Bloomington,_Indiana heuristic heuristic
# Boston,_Massachusetts San_Francisco,_California heuristic heuristic
# Boston,_Massachusetts San_Francisco,_California heuristic distance
# Bloomington,_Indiana Chicago,_Illinois heuristic distance
# Bloomington,_Indiana Chicago,_Illinois uniform distance
# Abbot_Village,_Maine Fairborn,_Ohio heuristic distance


