import numpy as np

class RealFMS:
  def __init__(self):
    self.ASCII_NUM = 128
    self.STATE_NUM = 7
    self.fmsTable = np.ones((self.STATE_NUM, self.ASCII_NUM))
    self.STATE_FAILURE = -1
    self.accept = [False, True, True, False, False, False, True]
    self.realState = 0
    self.realStateOfLastAccept = self.STATE_FAILURE
    self.realPrevStateOfLastAccept = self.STATE_FAILURE
    self.realNextStateOfNextChar = self.STATE_FAILURE
    self.realAnchor = False
    self.endReads = False
    for i in range(self.STATE_NUM):
      for j in range(self.ASCII_NUM):
        self.fmsTable[i][j] = self.STATE_FAILURE

    self.initStateByDigit(0, 1)
    self.initStateByDigit(1, 1)
    self.initStateByDigit(2, 2)
    self.initStateByDigit(3, 2)
    self.initStateByDigit(4, 6)
    self.initStateByDigit(5, 6)
    self.initStateByDigit(6, 6)	
    self.initStateBySpecial(0, '.', 3)
    self.initStateBySpecial(1, '.', 2)
    self.initStateBySpecial(1, 'E', 4)
    self.initStateBySpecial(1, 'e', 4)
    self.initStateBySpecial(2, 'E', 4)
    self.initStateBySpecial(2, 'e', 4)
    self.initStateBySpecial(4, '+', 5)
    self.initStateBySpecial(4, '-', 5)
  

  def reset(self):
    self.realState = 0
    self.realStateOfLastAccept = self.STATE_FAILURE
    self.realPrevStateOfLastAccept = self.STATE_FAILURE
    self.realNextStateOfNextChar = self.STATE_FAILURE
    self.realAnchor = False
    

  def initStateByDigit(self, previousState, nextState):
    for i in range(10):
      self.fmsTable[previousState]['0' + i] = nextState 
  
  def isRealSet(currentChar):
    if currentChar.isdigit():
      return True
    elif currentChar in ['E', 'e', '+', '-', '.']:
      return True
    else:
      return False
  
  def initStateBySpecial(self, previousState, value, nextState):
    self.fmsTable[previousState][value] = nextState 
  
  
  def next(self, state, currentChar):
    if (state == self.STATE_FAILURE or currentChar >= self.ASCII_NUM):
      return self.STATE_FAILURE
    
    return self.fmsTable[state][currentChar]
  
  
  def isAccept(self, state):
    if (state == self.STATE_FAILURE):
      return False
    return self.accept[state]