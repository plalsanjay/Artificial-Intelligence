# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """


    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()
        #print (legalMoves)

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        #print (scores)
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]


        "* YOUR CODE HERE *"

        smallScareTime = min(newScaredTimes)


        food = newFood.asList()
        foodDistances = []
        ghostDistances = []
        xFood = util.PriorityQueue()
        yGhost = util.PriorityQueue()
        currentCapsuleLoc= currentGameState.getCapsules()

        capsuleLoc  = successorGameState.getCapsules()


        # Calculate distance from every food #
        for item in food:
            a = manhattanDistance(newPos,item)
            foodDistances.append(a)
            xFood.push(item,a)

        x=0
        foodDistances.sort()
        if not currentCapsuleLoc:
            x=x+1

        if xFood.isEmpty()==True:
            return 1000
        else:

            if not capsuleLoc:
                minFoodList= min(1000,foodDistances[0])
                x=x+1
                if x==1:
                    x=x+1
                    return 10000
            else:
                for item in capsuleLoc:

                    minFoodList= min(1000,foodDistances[0],manhattanDistance(newPos,item))


        for ghost in successorGameState.getGhostPositions():
            a = manhattanDistance(newPos,ghost)
            ghostDistances.append(a)
            yGhost.push(ghost,a)

        pos= yGhost.pop()
        if smallScareTime > manhattanDistance(newPos,pos):
            return 1000
        ghostDistances.sort()
        if(ghostDistances[0]<2):
            return -10000

        return successorGameState.getScore() + 1.0/minFoodList
def scoreEvaluationFunction(currentGameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()

class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        "*** YOUR CODE HERE ***"

        def miniMaxalgo(gameState, agent, depth):
            result=[]
            legalActionList = gameState.getLegalActions(agent)
            num =gameState.getNumAgents()-1

            xChildList = []

            k=-1

            """
            if(gameState.isWin() or gameState.isLose() or self.depth==depth):
                variable=self.evaluationFunction(gameState)
            """
            if not gameState.getLegalActions(agent):
                return self.evaluationFunction(gameState),0
            if(gameState.isLose() or gameState.isWin() or depth==self.depth):
                return self.evaluationFunction(gameState),0
            elif agent==num:
                depth=depth+1
                nextAgent=self.index
            else:
                nextAgent=agent+1


            for legalAction in legalActionList:
                data=miniMaxalgo(gameState.generateSuccessor(agent,legalAction),nextAgent,depth)[0]
                result.append(data)

            if(agent==0):
                bestScore = max(result)
                for i in result:
                    k+=1
                    if i==bestScore:

                        break

            else:

                bestScore = min(result)
                for i in result:
                    k+=1
                    if i==bestScore:
                        break
            return bestScore, legalActionList[k]

        miniMaxMove = miniMaxalgo(gameState,0,0)

        return miniMaxMove[1]

        util.raiseNotDefined()


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"

        def miniMaxprunealgo(gameState, agent, depth, alpha, beta):
            result=[]
            resultAction=[]
            legalActionList = gameState.getLegalActions(agent)
            num =gameState.getNumAgents()-1

            xChildList = []

            k=-1

            """
            if(gameState.isWin() or gameState.isLose() or self.depth==depth):
                variable=self.evaluationFunction(gameState)
            """
            if not gameState.getLegalActions(agent):
                return self.evaluationFunction(gameState),0
            if(gameState.isLose() or gameState.isWin() or depth==self.depth):
                return self.evaluationFunction(gameState),0
            elif agent==num:
                depth=depth+1
                nextAgent=self.index
            else:
                nextAgent=agent+1


            for legalAction in legalActionList:
                if beta<alpha:
                    break

                newData=miniMaxprunealgo(gameState.generateSuccessor(agent,legalAction),nextAgent,depth,alpha,beta)[0]
                result.append(newData)

                if agent==self.index:
                    if newData>alpha:
                        alpha=newData
                else :
                    if newData<beta:
                        beta=newData


            if(agent==0):
                bestScore = max(result)
                for i in result:
                    k+=1
                    if i==bestScore:

                        break

            else:

                bestScore = min(result)
                for i in result:
                    k+=1
                    if i==bestScore:
                        break
            return bestScore, legalActionList[k]

        miniMaxMove = miniMaxprunealgo(gameState,0,0,-100000,100000)

        return miniMaxMove[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"

        def expectiminiMaxalgo(gameState, agent, depth):
            result=[]
            bestScore=0
            legalActionList = gameState.getLegalActions(agent)
            num =gameState.getNumAgents()-1

            xChildList = []

            k=-1

            """
            if(gameState.isWin() or gameState.isLose() or self.depth==depth):
                variable=self.evaluationFunction(gameState)
            """
            if not gameState.getLegalActions(agent):
                return self.evaluationFunction(gameState),0
            if(gameState.isLose() or gameState.isWin() or depth==self.depth):
                return self.evaluationFunction(gameState),0
            elif agent==num:
                depth=depth+1
                nextAgent=self.index
            else:
                nextAgent=agent+1


            for legalAction in legalActionList:
                data=expectiminiMaxalgo(gameState.generateSuccessor(agent,legalAction),nextAgent,depth)[0]
                result.append(data)
                if agent!=0:
                    bestScore=bestScore+(1.0/len(gameState.getLegalActions(agent)))*data


            if(agent==0):
                bestScore = max(result)
                for i in result:
                    k+=1
                    if i==bestScore:

                        break

            return bestScore, legalActionList[k]


        miniMaxMove = expectiminiMaxalgo(gameState,0,0)

        return miniMaxMove[1]


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    
    newPacmanPosition = currentGameState.getPacmanPosition()
    newGhostPositions = currentGameState.getGhostPositions()
    newFoodPositions = currentGameState.getFood().asList()
    totalFoodItems = len(newFoodPositions)
    newCapsulePositions = currentGameState.getCapsules()
    totalCapsules = len(newCapsulePositions)
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    ghosty=[]
    

    totalPoints = 0

    totalPoints += 100 * currentGameState.getScore()

    for capsule in newCapsulePositions:
        totalPoints += 5 * (1/(manhattanDistance(newPacmanPosition, capsule)*totalCapsules + 1))

    for ghost in newGhostPositions:
        totalPoints -= 5 * (1/(manhattanDistance(newPacmanPosition, ghost) + 1))
        ghosty.append(manhattanDistance(newPacmanPosition, ghost))
        
        
    for food in newFoodPositions:
        totalPoints += 5 * (1/(manhattanDistance(newPacmanPosition, food)*totalFoodItems + 1))
        
    ghosty.sort()
    if max(newScaredTimes)==0 :
        ghosty[0]<2
        totalPoints -=10000

    for index in range(len(newScaredTimes)):
        if newScaredTimes[index] != 0:
            totalPoints += 10 * (1/(manhattanDistance(newPacmanPosition, newGhostPositions[index])*newScaredTimes[index] + 1))
    


    return totalPoints
# Abbreviation
better = betterEvaluationFunction
