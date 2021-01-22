# baselineTeam.py
# ---------------
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


# baselineTeam.py
# ---------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

from captureAgents import CaptureAgent
import distanceCalculator
import random, time, util, sys
from game import Directions
import game
from util import manhattanDistance
from util import nearestPoint

#################
# Team creation #
#################

def createTeam(firstIndex, secondIndex, isRed,
               first = 'OffensiveReflexAgent', second = 'DefensiveReflexAgent'):
  """
  This function should return a list of two agents that will form the
  team, initialized using firstIndex and secondIndex as their agent
  index numbers.  isRed is True if the red team is being created, and
  will be False if the blue team is being created.

  As a potentially helpful development aid, this function can take
  additional string-valued keyword arguments ("first" and "second" are
  such arguments in the case of this function), which will come from
  the --redOpts and --blueOpts command-line arguments to capture.py.
  For the nightly contest, however, your team will be created without
  any extra arguments, so you should make sure that the default
  behavior is what you want for the nightly contest.
  """
  #print (first, second)
  return [eval(first)(firstIndex), eval(second)(secondIndex)]

#####################
# Structure for UCT #
#####################
maxDeepth =50
class Node(object):

    def __init__(self,gameState,agent,action,parentNode):
        self.parentNode = parentNode
        self.action = action
        if parentNode == None:
            self.deepth = 0
        else:
            self.deepth = parentNode.deepth + 1

        self.child = []
        self.v_times = 1
        self.q_value = 0

        self.gameState = gameState.deepCopy()
        #self.ghostPos = ghostPos
        self.legalActions = gameState.getLegalActions(agent)
        self.illegalActions = []
        self.legalActions.remove('Stop')

        self.legalActions = list(set(self.legalActions)-set(self.illegalActions))

        self.unexploredActions = self.legalActions[:]
        #self.borderline = borderline
        
        self.agent = agent
        self.E = 0.95
"""
def getBestChild(node):
    bestScore = -99999
    bestChild = None
    for n in node.child:
        score = n.q_value/n.v_times
        if score > bestScore:
            bestScore = score
            bestChild = n
    return bestChild

def getExpandedNode(node):
    if node.deepth >= maxDeepth:
        return node

    if node.unexploredActions != []:
        action = node.unexploredActions.pop()
        tempGameState = node.gameState.deepCopy()
        nextGameState = tempGameState.generateSuccessor(node.agent,action)
        if node.agent ==3 :
            childNode = Node(nextGameState,0,action,node)
        else :
            childNode = Node(nextGameState,node.agent+1,action,node)
        node.child.append(childNode)
        return childNode
    
    if util.flipCoin(node.E): # E-greedy 
        nextBestNode = getBestChild(node)
    else:
        nextBestNode = random.choice(node.child)
    return getExpandedNode(nextBestNode)

def getReward(node):
    # lastPos = node.parentNode.gameState.getAgentPosition(node.agent.index)
    gamestate = node.gameState
    return gamestate.getScore()
    
def backpropagation(node,reward):
    node.v_times += 1
    node.q_value += reward
    if node.parentNode != None:
        backpropagation(node.parentNode,reward)

def MCTS(node):
    timeLimit = 0.01
    start = time.time()
    while(time.time()-start < timeLimit):
    # for i in range(maxTreeIteration):
        
        nodeForSimulation = getExpandedNode(node) #selection and expand

        reward = getReward(nodeForSimulation)

        backpropagation(nodeForSimulation,reward)
    
    return getBestChild(node).action
def evaluationfunction (node) :
    gameState = node.gameState
    
"""    
    
        

##########
# Agents #
##########



class OffensiveReflexAgent(CaptureAgent):
    """
    A reflex agent that seeks food. This is an agent
    we give you to get an idea of what an offensive agent might look like,
    but it is by no means the best or only way to build an offensive agent.
    """

    # print("offensive")
    # print("hello")

    def registerInitialState(self, gameState):
        self.start = gameState.getAgentPosition(self.index)
        CaptureAgent.registerInitialState(self, gameState)

    def chooseAction(self, gameState):
        """
        Picks among the actions with the highest Q(s,a).
        """
        rootNode = Node(gameState, self.index, None, None)
        resultAction = self.MCTS(rootNode)
        
        return resultAction
    def getBestChild(self, node):
        #bestScore = -99999
        bestChild = None
        
        if node.agent ==1 or node.agent ==3 :
            bestScore = 99999
            for n in node.child:
                score = n.q_value / n.v_times
                if score < bestScore:
                    bestScore = score
                    bestChild = n
            return bestChild
        else :
            bestScore = -99999
            for n in node.child:
                score = n.q_value / n.v_times
                if score > bestScore:
                    bestScore = score
                    bestChild = n
            return bestChild
        
            
        
        for n in node.child:
            score = n.q_value / n.v_times
            if score > bestScore:
                bestScore = score
                bestChild = n
        return bestChild

    def getExpandedNode(self, node):
        if node.deepth >= maxDeepth:
            return node

        if node.unexploredActions != []:
            action = node.unexploredActions.pop()
            tempGameState = node.gameState.deepCopy()
            nextGameState = tempGameState.generateSuccessor(node.agent, action)
            if node.agent == 1:
                childNode = Node(nextGameState, 0, action, node)
            else:
                childNode = Node(nextGameState, node.agent + 1, action, node)
            node.child.append(childNode)
            return childNode

        if util.flipCoin(node.E):  # E-greedy
            nextBestNode = self.getBestChild(node)
        else:
            nextBestNode = random.choice(node.child)
        return self.getExpandedNode(nextBestNode)

    def getReward(self,node):
        # lastPos = node.parentNode.gameState.getAgentPosition(node.agent.index)
        gamestate = node.gameState
        #print(node.agent)
        #print(gamestate.getScore())
        return self.evaluationfunction(gamestate, self.index , node.action)

    def backpropagation(self,node, reward):
        node.v_times += 1
        node.q_value += reward
        if node.parentNode != None:
            self.backpropagation(node.parentNode, reward)

    def MCTS(self, node):
        timeLimit = 0.4
        start = time.time()
        while (time.time() - start < timeLimit):
            # for i in range(maxTreeIteration):

            nodeForSimulation = self.getExpandedNode(node)  # selection and expand

            reward = self.getReward(nodeForSimulation)

            self.backpropagation(nodeForSimulation, reward)

        return self.getBestChild(node).action
        
    
    
    def evaluationfunction(self, gamestate, index,action):
        agent = index
        #gamestate = node.gameState
        #gamestate = gameState.generateSuccessor(self.index, action)
        #print(agent , "Stop") 
        pos = gamestate.getAgentPosition(agent)
        totalpoints = 0
        totalpoints += 100* gamestate.getScore()
        
        """
        capsules = gamestate.getBlueCapsules() 
        newFoodPositions = gamestate.getRedFood().asList()
        newGhostPositions = gamestate.getAgentPosition(0),gamestate.getAgentPosition(2)
        totalFoodItems = len(newFoodPositions)
        totalCapsules = len(capsules)
        """
        
        
        
        
        
           
        
        bcapsules = gamestate.getRedCapsules() 
        bnewFoodPositions = gamestate.getRedFood().asList()
        bnewGhostPositions = gamestate.getAgentPosition(0),gamestate.getAgentPosition(2)
        btotalFoodItems = len(bnewFoodPositions)
        btotalCapsules = len(bcapsules)
        if btotalCapsules==0:
            bcapsules=0
        
        rcapsules = gamestate.getBlueCapsules()
        rnewFoodPositions = gamestate.getBlueFood().asList()
        rnewGhostPositions = gamestate.getAgentPosition(1),gamestate.getAgentPosition(3)
        rtotalFoodItems = len(rnewFoodPositions)
        rtotalCapsules = len(rcapsules)
        if rtotalCapsules==0:
            rcapsules=0
        walls = gamestate.getWalls().asList()
        #z = 0
        #distance = []
        xhome = int(walls[len(walls) - 1][0] / 2)
        if not self.ghostorpacman(gamestate,index):
            if len(bnewFoodPositions)-len(rnewFoodPositions) <=0:
                if  not self.ghostorpacman(gamestate,1) or not self.ghostorpacman(gamestate,3):
                    if (self.ghostDistance(bnewGhostPositions[0], gamestate) < 2 and bnewGhostPositions[0][0]<xhome) or (self.ghostDistance(bnewGhostPositions[1], gamestate) < 2 and bnewGhostPositions[1][0]<xhome):
                        return -10*self.ghostDistance(pos, gamestate)+10*rnewGhostPositions[0][1]
                    else :
                        if self.distancetonearestfood(pos,gamestate) -self.ghostDistance(pos,gamestate) <2:
                            return 5*self.distancetonearestfood(pos,gamestate)
                        else :
                            return 10*self.ghostDistance(pos,gamestate)+10*rnewGhostPositions[0][0]+10*rnewGhostPositions[1][0]
                else:
                    if xhome<pos[0]:
                        if(self.ghostDistance(pos,gamestate)==None or self.ghostDistance(pos,gamestate)==0):
                            return 1000*self.ghostDistance(pos,gamestate)-100*rnewGhostPositions[0][0]-100*rnewGhostPositions[1][0]
                        return -100*self.ghostDistance(pos,gamestate)-10*rnewGhostPositions[0][0]-10*rnewGhostPositions[1][0]
                    else :
                        return -100*self.distancetonearestfood(pos,gamestate)
                    #return 100* self.distancetohome(pos,gamestate)
                    
                    
                
            else :
                return 100 * (-10*xhome) + 5*self.distancetonearestfood(pos,gamestate)-3*self.distancetonearestfood(pos,gamestate)
        else :
            if len(bnewFoodPositions)-len(rnewFoodPositions) < 3:
                if  self.ghostorpacman(gamestate,1) or self.ghostorpacman(gamestate,3):
                    #print(self.ghostDistance(pos,gamestate))
                    return 10*self.ghostDistance(pos,gamestate)+2*self.distancetonearestfood(pos,gamestate)+10*rnewGhostPositions[0][0]+10*rnewGhostPositions[1][0]
                
                else:
                    if pos[0]>xhome:
                        #print(self.ghostDistance(pos,gamestate))
                        if self.ghostDstance(pos,gamestate)>10:
                            return 100* self.distancetonearestfood(pos,gamestate)+10*rnewGhostPositions[0][0]+10*rnewGhostPositions[1][0]
                        else:
                            return -100*self.ghostDstance(pos,gamestate)+10*rnewGhostPositions[0][0]+10*rnewGhostPositions[1][0]
                    
                    
                
            else :
                return 100 * xhome+10 + 50*self.distancetonearestfood(pos,gamestate)- 10*self.ghostDistance(pos,gamestate)
        
        
        



    

    def ghostorpacman(self, gameState , index):
        walls = gameState.getWalls().asList()
        z = 0
        distance = []
        xhome = int(walls[len(walls) - 1][0] / 2)
        #print(xhome)
        state = gameState.getAgentPosition(index)
        if state[0]<=xhome :
            return False
        else :
            return True   
        
        #return gameState.getAgentPosition(self.index)

    def ghostDistance(self, pos, gameState):
        ghost1 = gameState.getAgentPosition(1)
        ghost2 = gameState.getAgentPosition(3)
        # print(ghost1)
        # print("hello")
        # print(type(ghost2))
        # print(type(pos))
        # print("dad")
        if ghost1 == None and ghost2 == None:
            return 100

        if ghost1 == None:
            return self.getMazeDistance(pos, ghost2)
        else:
            return self.getMazeDistance(pos, ghost1)
        a1 = self.getMazeDistance(pos, ghost1)
        a2 = self.getMazeDistance(pos, ghost2)

        if a1 > a2:
            return a2
        else:
            return a1

    def distancetonearestfood(self, newPos, gameState):
        foodDistances = []
        newFood = self.getFood(gameState)
        # print(newFood)
        food = newFood.asList()
        # print(food)
        # print("food")
        xFood = util.PriorityQueue()
        for item in food:
            # 'pos':item
            a = self.getMazeDistance(newPos, item)
            # print(item)

            foodDistances.append(a)
            xFood.push(item, a)
        foodDistances.sort()
        x = xFood.pop()
        for item in foodDistances:
            if item > self.getMazeDistance(x, newPos):
                return item

        return foodDistances[0]

    def distancetohome(self, newPos, gameState):
        walls = gameState.getWalls().asList()
        z = 0
        distance = []
        xhome = int(walls[len(walls) - 1][0] / 2)
        # print (walls)
        for item in walls:
            if item[0] == 0:
                z = z + 1
            else:
                break
        for i in range(0, z - 1):
            if not gameState.hasWall(xhome, i):
                # print(newPos,(xhome,i))
                distance.append(self.getMazeDistance(newPos, (xhome, i)))
        distance.sort()
        # print(distance)
        return distance[0]
        # print(z)

        # print( xhome,"yello" )
        # print(man11)

    def getFeatures(self, gameState, action):
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)
        foodList = self.getFood(successor).asList()
        features['successorScore'] = -len(foodList)  # self.getScore(successor)

        # Compute distance to the nearest food

        if len(foodList) > 0:  # This should always be True,  but better safe than sorry
            myPos = successor.getAgentState(self.index).getPosition()
            minDistance = min([self.getMazeDistance(myPos, food) for food in foodList])
            features['distanceToFood'] = minDistance
        return features

    def getSuccessor(self, gameState, action):
        """
        Finds the next successor which is a grid position (location tuple).
        """
        successor = gameState.generateSuccessor(self.index, action)
        pos = successor.getAgentState(self.index).getPosition()
        if pos != nearestPoint(pos):
            # Only half a grid position was covered
            return successor.generateSuccessor(self.index, action)
        else:
            return successor

    def evaluate(self, gameState, action):
        """
        Computes a linear combination of features and feature weights
        """
        features = self.getFeatures(gameState, action)
        weights = self.getWeights(gameState, action)
        return features * weights

    def getFeatures(self, gameState, action):
        """
        Returns a counter of features for the state
        """
        features = util.Counter()
        successor = self.getSuccessor(gameState, action)
        features['successorScore'] = self.getScore(successor)
        return features

    def getWeights(self, gameState, action):
        """
        Normally, weights do not depend on the gamestate.  They can be either
        a counter or a dictionary.
        """
        return {'successorScore': 1.0}

    def getWeights(self, gameState, action):
        return {'successorScore': 100, 'distanceToFood': -1}
class DefensiveReflexAgent(CaptureAgent):
    """
    A reflex agent that seeks food. This is an agent
    we give you to get an idea of what an offensive agent might look like,
    but it is by no means the best or only way to build an offensive agent.
    """

    # print("offensive")
    # print("hello")

    def registerInitialState(self, gameState):
        self.start = gameState.getAgentPosition(self.index)
        CaptureAgent.registerInitialState(self, gameState)

    def chooseAction(self, gameState):
        """
        Picks among the actions with the highest Q(s,a).
        """
        rootNode = Node(gameState, self.index, None, None)
        resultAction = self.MCTS(rootNode)
        
        return resultAction
    def getBestChild(self, node):
        #bestScore = -99999
        bestChild = None
        
        if node.agent ==1 or node.agent ==3 :
            bestScore = 99999
            for n in node.child:
                score = n.q_value / n.v_times
                if score < bestScore:
                    bestScore = score
                    bestChild = n
            return bestChild
        else :
            bestScore = -99999
            for n in node.child:
                score = n.q_value / n.v_times
                if score > bestScore:
                    bestScore = score
                    bestChild = n
            return bestChild
        
            
        
        for n in node.child:
            score = n.q_value / n.v_times
            if score > bestScore:
                bestScore = score
                bestChild = n
        return bestChild

    def getExpandedNode(self, node):
        if node.deepth >= maxDeepth:
            return node

        if node.unexploredActions != []:
            action = node.unexploredActions.pop()
            tempGameState = node.gameState.deepCopy()
            nextGameState = tempGameState.generateSuccessor(node.agent, action)
            if node.agent == 3:
                childNode = Node(nextGameState, 2, action, node)
            else:
                childNode = Node(nextGameState, node.agent + 1, action, node)
            node.child.append(childNode)
            return childNode

        if util.flipCoin(node.E):  # E-greedy
            nextBestNode = self.getBestChild(node)
        else:
            nextBestNode = random.choice(node.child)
        return self.getExpandedNode(nextBestNode)

    def getReward(self,node):
        # lastPos = node.parentNode.gameState.getAgentPosition(node.agent.index)
        gamestate = node.gameState
        #print(node.agent)
        #print(gamestate.getScore())
        return self.evaluationfunction(gamestate, self.index)

    def backpropagation(self,node, reward):
        node.v_times += 1
        node.q_value += reward
        if node.parentNode != None:
            self.backpropagation(node.parentNode, reward)

    def MCTS(self, node):
        timeLimit = 0.4
        start = time.time()
        while (time.time() - start < timeLimit):
            # for i in range(maxTreeIteration):

            nodeForSimulation = self.getExpandedNode(node)  # selection and expand

            reward = self.getReward(nodeForSimulation)
            print(reward)
            if reward==None:
                reward=2

            self.backpropagation(nodeForSimulation, reward)

        return self.getBestChild(node).action
            
    def evaluationfunction(self, gamestate, index):
        agent = index
        #gamestate = node.gameState
        #gamestate = gameState.generateSuccessor(self.index, action)
        #print(agent , "Stop") 
        pos = gamestate.getAgentPosition(agent)
        totalpoints = 0
        totalpoints += 100* gamestate.getScore()
        
        """
        capsules = gamestate.getBlueCapsules() 
        newFoodPositions = gamestate.getRedFood().asList()
        newGhostPositions = gamestate.getAgentPosition(0),gamestate.getAgentPosition(2)
        totalFoodItems = len(newFoodPositions)
        totalCapsules = len(capsules)
        """
        
        
        
        
        
           
        
        bcapsules = gamestate.getRedCapsules() 
        bnewFoodPositions = gamestate.getRedFood().asList()
        bnewGhostPositions = gamestate.getAgentPosition(0),gamestate.getAgentPosition(2)
        btotalFoodItems = len(bnewFoodPositions)
        btotalCapsules = len(bcapsules)
        
        rcapsules = gamestate.getBlueCapsules()
        rnewFoodPositions = gamestate.getBlueFood().asList()
        rnewGhostPositions = gamestate.getAgentPosition(1),gamestate.getAgentPosition(3)
        rtotalFoodItems = len(rnewFoodPositions)
        rtotalCapsules = len(rcapsules)
        walls = gamestate.getWalls().asList()
        #z = 0
        #distance = []
        xhome = int(walls[len(walls) - 1][0] / 2)
        if self.ghostorpacman(gamestate,index):
            if len(bnewFoodPositions)-len(rnewFoodPositions) > 3:
                if  self.ghostorpacman(gamestate,1) or self.ghostorpacman(gamestate,3):
                    if (self.ghostDistance(bnewGhostPositions[0], gamestate) < 2 and bnewGhostPositions[0][0]>xhome) or (self.ghostDistance(bnewGhostPositions[1], gamestate) < 2 and bnewGhostPositions[1][0]>xhome):
                        return -10*self.ghostDistance(pos, gamestate)
                    else :
                        if self.distancetonearestfood(pos,gamestate) -self.ghostDistance(pos,gamestate) >2:
                            return 20*self.distancetonearestfood(pos,gamestate)
                        else :
                            return 10*self.ghostDistance(pos,gamestate)
                else:
                    if xhome<pos[0]:
                        return 1000
                    else :
                        return -1000
                    #return 100* self.distancetohome(pos,gamestate)
                    
                    
                
            else :
                return 100 * xhome+10 + self.distancetonearestfood(pos,gamestate)
        else :
            if len(bnewFoodPositions)-len(rnewFoodPositions) < 3:
                if  self.ghostorpacman(gamestate,1) or self.ghostorpacman(gamestate,3):
                    #print(self.ghostDistance(pos,gamestate))
                    return -10*self.ghostDistance(pos,gamestate)+2*self.distancetonearestfood(pos,gamestate)
                
                else:
                    if pos[0]>xhome:
                        #print(self.ghostDistance(pos,gamestate))
                        if self.ghostDstance(pos,gamestate)>10:
                            return 100* self.distancetonearestfood(pos,gamestate)
                        else:
                            return -100*self.ghostDstance(pos,gamestate)
                    
                    
                
            else :
                return 100 * xhome+10 + 50*self.distancetonearestfood(pos,gamestate)- 10*self.ghostDistance(pos,gamestate)
    
    def ghostorpacman(self, gameState , index):
        walls = gameState.getWalls().asList()
        z = 0
        distance = []
        xhome = int(walls[len(walls) - 1][0] / 2)
        #print(xhome)
        state = gameState.getAgentPosition(index)
        if state[0]<=xhome :
            return False
        else :
            return True   
        
        #return gameState.getAgentPosition(self.index)
    def ghostDistance(self, pos, gameState):
        ghost1 = gameState.getAgentPosition(1)
        ghost2 = gameState.getAgentPosition(3)
        # print(ghost1)
        # print("hello")
        # print(type(ghost2))
        # print(type(pos))
        # print("dad")
        if ghost1 == None and ghost2 == None:
            return 100

        if ghost1 == None:
            return self.getMazeDistance(pos, ghost2)
        elif ghost2 == None:
            return self.getMazeDistance(pos, ghost1)
        a1 = self.getMazeDistance(pos, ghost1)
        a2 = self.getMazeDistance(pos, ghost2)

        if a1 > a2:
            return a2
        else:
            return a1

    def distancetonearestfood(self, newPos, gameState):
        foodDistances = []
        newFood = self.getFood(gameState)
        # print(newFood)
        food = newFood.asList()
        # print(food)
        # print("food")
        xFood = util.PriorityQueue()
        for item in food:
            # 'pos':item
            a = self.getMazeDistance(newPos, item)
            # print(item)

            foodDistances.append(a)
            xFood.push(item, a)
        foodDistances.sort()
        x = xFood.pop()
        for item in foodDistances:
            if item > self.getMazeDistance(x, newPos):
                return item

        return foodDistances

    def distancetohome(self, newPos, gameState):
        walls = gameState.getWalls().asList()
        z = 0
        distance = []
        xhome = int(walls[len(walls) - 1][0] / 2)
        # print (walls)
        for item in walls:
            if item[0] == 0:
                z = z + 1
            else:
                break
        for i in range(0, z - 1):
            if not gameState.hasWall(xhome, i):
                # print(newPos,(xhome,i))
                distance.append(self.getMazeDistance(newPos, (xhome, i)))
        distance.sort()
        # print(distance)
        return distance[0]
        # print(z)

        # print( xhome,"yello" )
        # print(man11)

