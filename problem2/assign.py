#! /l/python3/bin/python3

# Professor David Crandall
# B551 Elements of Artificial Intelligence
# Yue Chen, Siddharth Jayant Pathak, and Raghottam Dilip Talwai
# October 1st, 2017

# Problem 2

# We define this problem as a problem that could employ A* search. The state space is every possible combination of one
# to three people forming a group. The successor function adds people into a group if there are less than three people
# in the current group, otherwise it creates an empty group and adds people into the new empty group. The edge weights
# are the time consumption from the initial state (i.e. no people in any group at all) to the current state. There is a
# detailed description of our heuristic function in the in-line comment.

# Our search algorithm is a classic A* search that expands the most promising node considering both the sinking cost and
# possible future cost.

# The most challenging problem we faced was that the problem is NP-hard. We are employing dynamic programming techniques
# but we are also very much aware that the optimal sub-decisions do not guarantee the optimal final decision. We could
# have our program do a traversal of the search tree and come up with "the best" solution, but that is computationally
# less feasible. We are, as of now, returning the "a (relatively) best" solution but significantly cutting down our
# processing time. We believe this is the right decision to make.

class Survey:

    # saves students' information and their preferences.

    count = 0

    def __init__(self, name, number, prefer, notPrefer):
        self.name = name
        self.number = number
        self.prefer = prefer.split(",") if prefer != "_" else []
        self.notPrefer = notPrefer.split(",") if notPrefer != "_" else []
        Survey.count += 1

    def __repr__(self):
        return self.name

        # Yingnan Ju helped me finding this method to simplify the printing job.

def successors(state):

    # generates successors of a given state.

    successorState = []

    for eachGroup in state.assigned:
        if len(eachGroup) < 3:
            newState = State(assigned=state.assigned, people=state.people)
            newState.add_person(newState.unassigned[0], state.assigned.index(eachGroup))
            successorState.append(newState)
    newState = State(assigned=state.assigned, people=state.people)
    newState.add_person(newState.unassigned[0], len(newState.assigned))
    successorState.append(newState)

    return successorState

def is_goal(state):

    # returns a boolean value of a state's goal status.

    if len(state.unassigned) == 0:
        return True
    else:
        return False

class State:

    # This is the major class for storing states' information and providing necessary methods for other functions to
    # access them.

    gradeTime = 0
    emailTime = 0
    meetTime = 0

    priority = 0

    people = []
    assigned = []
    unassigned = []

    def __init__(self, assigned, people):

        # Yingnan Ju helped me with 2-dimensional list copy-and-paste. I found out that deepcopy method was not what I
        # was looking for.

        self.assigned = []
        for eachGroup in assigned:
            self.assigned.append(list(eachGroup))
        self.update_priority()
        self.people = list(people)
        self.update_unassigned()

    def set_time(self, gradeTime, emailTime, meetTime):
        State.gradeTime = gradeTime
        State.emailTime = emailTime
        State.meetTime = meetTime

    def update_priority(self):

        assignedCount = 0
        sinkingCost = len(self.assigned) * State.gradeTime
        for group in self.assigned:
            for person in group:
                assignedCount += 1
                if person.number != len(group) and person.number != 0:
                    sinkingCost += 1
                for preferred in person.prefer:
                    if preferred not in list(group[i].name for i in range(0, len(group))):
                        sinkingCost += State.emailTime
                for notPreferred in person.notPrefer:
                    if notPreferred in list(group[i].name for i in range(0, len(group))):
                        sinkingCost += State.meetTime

        # The lowest possible remaining cost given all assigned groups have 3 people and all unassigned groups will have
        # 3 people.

        # heuristic = ((Survey.count - len(self.assigned) *3 ) // 3 + (1 if (Survey.count - len(self.assigned) * 3) % 3 > 0 else 0)) * State.gradeTime

        heuristic = math.ceil((Survey.count - len(self.assigned) * 3) / 3) * State.gradeTime

        self.priority = sinkingCost + heuristic


    def add_person(self, person, groupIndex):
        if groupIndex < len(self.assigned):
            self.assigned[groupIndex].append(person) if len(self.assigned[groupIndex]) < 3 else None
        else:
            self.assigned.append([person])
        self.update_priority()
        self.update_unassigned()

    def update_unassigned(self):
        self.unassigned.clear()
        flatAssigned = []
        for group in self.assigned:
            flatAssigned.extend(group)
        for person in self.people:
            if person not in flatAssigned:
                self.unassigned.append(person)

def solve(initialState):
    if is_goal(initialState):
        return initialState
    else:
        fringe = [initialState]
        while len(fringe) > 0:

            # print(len(fringe))
            # print([state.priority for state in fringe])
            # if fringe.pop(0), djcran and kapadia will be stuck together forever :)

            for s in successors(fringe.pop()):
                if is_goal(s):
                    return s
                isInFringe = False
                for eachState in fringe:
                    if eachState.priority <= s.priority:
                        fringe.insert(fringe.index(eachState), s)
                        isInFringe = True
                        break
                if not isInFringe:
                    fringe.append(s)
        return False

# main()

import sys, math

inputFileName = sys.argv[1]
gradeTime = int(sys.argv[2])
emailTime = int(sys.argv[4])
meetTime = int(sys.argv[3])

inputFile = open(inputFileName, 'r')

people = []

for line in inputFile:
    person = line.split()
    people.append(Survey(name=person[0],number=int(person[1]), prefer=person[2], notPrefer=person[3]))

initialState = State(assigned=[], people=people)

initialState.set_time(gradeTime=gradeTime, emailTime=emailTime, meetTime=meetTime)

solution = solve(initialState)

# print(solution.assigned, solution.priority)

for group in solution.assigned:
    print(" ".join([person.name for person in group]))
print(solution.priority)