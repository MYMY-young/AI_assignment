from util import manhattanDistance
from game import Directions
import random, util

from game import Agent

## Example Agent
class ReflexAgent(Agent):

  def Action(self, gameState):

    move_candidate = gameState.getLegalActions()

    scores = [self.reflex_agent_evaluationFunc(gameState, action) for action in move_candidate]
    bestScore = max(scores)
    Index = [index for index in range(len(scores)) if scores[index] == bestScore]
    get_index = random.choice(Index)

    return move_candidate[get_index]

  def reflex_agent_evaluationFunc(self, currentGameState, action):

    successorGameState = currentGameState.generatePacmanSuccessor(action)
    newPos = successorGameState.getPacmanPosition()
    oldFood = currentGameState.getFood()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    return successorGameState.getScore()



def scoreEvalFunc(currentGameState):

  return currentGameState.getScore()

class AdversialSearchAgent(Agent):

  def __init__(self, getFunc ='scoreEvalFunc', depth ='2'):
    self.index = 0
    self.evaluationFunction = util.lookup(getFunc, globals())

    self.depth = int(depth)

######################################################################################

class MinimaxAgent(AdversialSearchAgent):
  """
    [문제 01] MiniMax의 Action을 구현하시오. (20점)
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
    ####################### Write Your Code Here ################################
  def Action(self,gameState):

    
    move_able = gameState.getLegalActions(0)
    move = Directions.STOP

    v = float("-inf")

    for i in move_able:
      aa = self.Min_Value(gameState.generateSuccessor(0,i),0,1)
      if aa > v:
        v = aa
        move = i
    
    return move


  def Max_Value(self,state,depth):
    if (depth == self.depth or state.isWin() or state.isLose()):
      return self.evaluationFunction(state)

    v = float("-inf")
    pac = 0
    for s in state.getLegalActions(pac):
      v2 = self.Min_Value(state.generateSuccessor(pac,s),depth,1)
      if(v2 > v):
        v = v2

    return v

  def Min_Value(self,state,depth,agent_num):
    if (depth == self.depth or state.isWin() or state.isLose()):
      return self.evaluationFunction(state)

    v = float("inf")

    for s in state.getLegalActions(agent_num):
      if (agent_num == state.getNumAgents()-1):
        v2 = self.Max_Value(state.generateSuccessor(agent_num,s),depth+1)
      else:
        v2 = self.Min_Value(state.generateSuccessor(agent_num,s),depth,agent_num+1)
      if v2 < v:
        v = v2

    return v




    
    


    #raise Exception("Not implemented yet")

    ############################################################################




class AlphaBetaAgent(AdversialSearchAgent):
  """
    [문제 02] AlphaBeta의 Action을 구현하시오. (25점)
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
 # def Action(self, gameState):
    ####################### Write Your Code Here ################################



  

  def Action(self,gameState):

    alpha = float("-inf")
    beta = float("inf")

    return self.Max_Value(gameState,0,alpha,beta)[1]
      
    

  def Max_Value(self,state,depth,alpha,beta):
    if (depth == self.depth or state.isWin() or state.isLose() or len(state.getLegalActions(0))==0):
      return (self.evaluationFunction(state),None)

    v = float("-inf")
    pac = 0
    move = None
    for s in state.getLegalActions(0):
      v2 = self.Min_Value(state.generateSuccessor(pac,s),depth,1,alpha,beta)[0]
      if v2 > v:
        v,move = v2,s
      if(depth==0 and v> beta):
        return (v,move)
      if (depth != 0 and v >= beta):
        return (v,move)
      alpha = max(alpha,v)

    return (v,move)

  def Min_Value(self,state,depth,agent_num,alpha,beta):
    if (depth == self.depth or state.isWin() or state.isLose() or len(state.getLegalActions(0))==0):
      return self.evaluationFunction(state),None
    
    v = float("inf")


    move = None

    
    for s in state.getLegalActions(agent_num):
      if(agent_num == state.getNumAgents()-1):
        v2 = self.Max_Value(state.generateSuccessor(agent_num,s),depth+1,alpha,beta)[0]
      else:
        v2 = self.Min_Value(state.generateSuccessor(agent_num,s),depth,agent_num+1, alpha,beta)[0]
      if v2 < v:
        v,move = v2,s
      if (depth == 0 and v < alpha):
        return (v,move)
      if(depth != 0 and v<=alpha):
        return (v,move)
      beta = min(beta,v)

    return (v,move)
    





   # raise Exception("Not implemented yet")

    ############################################################################



class ExpectimaxAgent(AdversialSearchAgent):
  """
    [문제 03] Expectimax의 Action을 구현하시오. (25점)
    (depth와 evaluation function은 위에서 정의한 self.depth and self.evaluationFunction을 사용할 것.)
  """
  #def Action(self, gameState):
    ####################### Write Your Code Here ################################

  def Action(self,gameState):


    move_able = gameState.getLegalActions(0)
    move = Directions.STOP

    v = float("-inf")

    for i in move_able:
      aa = self.Min_Value(gameState.generateSuccessor(0,i),0,1)
      if aa > v:
        v = aa
        move = i
    return move


  def Max_Value(self,state,depth):
    if (depth == self.depth or state.isWin() or state.isLose()):
      return self.evaluationFunction(state)

    v = float("-inf")
    pac = 0
    for s in state.getLegalActions(pac):
      v = max(v,self.Min_Value(state.generateSuccessor(pac,s),depth,1))

    return v

  def Min_Value(self,state,depth,agent_num):
    if (depth == self.depth or state.isWin() or state.isLose()):
      return self.evaluationFunction(state)

    v = 0

    if (agent_num == state.getNumAgents()-1):
      for s in state.getLegalActions(agent_num):
        v = v + self.Max_Value(state.generateSuccessor(agent_num,s),depth+1)
    else:
      for s in state.getLegalActions(agent_num):
        v = v + self.Min_Value(state.generateSuccessor(agent_num,s),depth,agent_num+1)

    return float(v/len(state.getLegalActions(agent_num)))
    
























    raise Exception("Not implemented yet")

    ############################################################################
