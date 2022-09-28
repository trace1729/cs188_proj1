# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

from calendar import prmonth
import util

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]
class serNode:
    def __init__(self, prior, pos, action, expense=0,cost=0) -> None:
        self.prior = prior
        self.pos = pos
        self.action = action
        self.expense = expense
        self.cost = cost
    
    def getPrior(self):
        return self.prior
   
    def getPos(self):
        return self.pos
  
    def getAction(self):
        return self.action
            
    def getExpense(self):
        return self.expense

    def getF(self):
        return self.cost
    

            
def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))
    """
    
    actions = []  # 操作序列
    fringe = util.Stack() 
    visited_state = set() # 已经展开的状态
    
    fringe.push(serNode(any, problem.getStartState(), any, 0))
        
    while not fringe.isEmpty():
        top = fringe.pop()
        assert isinstance(top, serNode)
        visited_state.add(top.getPos())
        
        if problem.isGoalState(top.getPos()):
            while top.getPos() != problem.getStartState():
                actions.append(top.getAction())
                top = top.getPrior()
            break        
        
        for n in problem.getSuccessors(top.getPos()):
            if n[0] not in visited_state:
                fringe.push(serNode(top, n[0], n[1], n[2]))
        
    print(len(actions))
    return list(reversed(actions))
    

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    
    actions = []  # 操作序列
    fringe = util.Queue() 
    visited_state = set() # 已经展开的状态
    fringe.push(serNode(any, problem.getStartState(), any, 0))
        
    while not fringe.isEmpty():
        top = fringe.pop()
        assert isinstance(top, serNode)
        visited_state.add(top.getPos())
        
        if problem.isGoalState(top.getPos()):
            while top.getPos() != problem.getStartState():
                actions.append(top.getAction())
                top = top.getPrior()
            break        
        
        for n in problem.getSuccessors(top.getPos()):
            if n[0] not in visited_state:
                fringe.push(serNode(top, n[0], n[1], n[2]))
            
    return list(reversed(actions))

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    actions = []  # 操作序列
    fringe = util.PriorityQueue() 
    visited_state = set() # 已经展开的状态
    fringe.push(serNode(any, problem.getStartState(), any, 0), 0)
        
    while not fringe.isEmpty():
        top = fringe.pop()
        assert isinstance(top, serNode)
        visited_state.add(top.getPos())
        
        if problem.isGoalState(top.getPos()):
            while top.getPos() != problem.getStartState():
                actions.append(top.getAction())
                top = top.getPrior()
            break        
        
        for n in problem.getSuccessors(top.getPos()):
            if n[0] not in visited_state:
                fringe.push(serNode(top, n[0], n[1], n[2]), n[2])
            
    return list(reversed(actions))

    

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    
    actions = []  # 操作序列
    fringe = util.PriorityQueue() 
    visited_state = set() # 已经展开的状态
    fringe.push(serNode(any, problem.getStartState(), any), 0)
        
    while not fringe.isEmpty():
        top = fringe.pop()
        assert isinstance(top, serNode)
        visited_state.add(top.getPos())
        
        if problem.isGoalState(top.getPos()):
            while top.getPos() != problem.getStartState():
                actions.append(top.getAction())
                top = top.getPrior()
            break        
        
        for n in problem.getSuccessors(top.getPos()):
            if n[0] not in visited_state:
                fringe.push(serNode(top, n[0], n[1], n[2], top.getF() + n[2]), 
                            top.getF() + n[2] + heuristic(n[0], problem))
            
    return list(reversed(actions))

   


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
