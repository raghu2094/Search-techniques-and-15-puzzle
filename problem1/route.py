# put your routing program here!

import sys

city_routes = {}


def read_input(file_name):
    input_file = open(file_name,"r")
    speed = 0
    for l in input_file:
        temp = l.split(" ")
        if temp[-3]!='' and temp[-2]!='':
            if int(temp[-3]) != 0 and int(temp[-3]) != 0:
                if temp[0] in city_routes:
                    city_routes[temp[0]].append(temp[1:])
                else:
                    city_routes[temp[0]] = [temp[1:]]
                if temp[1] in city_routes:
                    city_routes[temp[1]].append(temp[:1]+temp[2:])
                else:
                    city_routes[temp[1]] = [temp[:1]+temp[2:]]

        # if int(temp) == 0:
        #     print l
        # if not temp.split():
        #     print l

def is_goal(s):
    return s == end_city

def successors(temp):
    suc = city_routes[temp[0]]
    return [ [s[0],temp[0:-1],int(s[-3])+int(temp[-1])] for s in suc]

read_input("road-segments.txt")
visited = {}
start_city = "Abbot_Village,_Maine"
end_city = "Fairborn,_Ohio"
fringe = []
fringe.append([start_city,0])
while len(fringe) > 0:
    temp = fringe.pop(0)
    if temp[0] in visited:
        pass
    else:
        visited[temp[0]] = 1
        for s in successors(temp):
            if is_goal(s[0]):
                print s
                sys.exit(0)
                break
            fringe.append(s)
