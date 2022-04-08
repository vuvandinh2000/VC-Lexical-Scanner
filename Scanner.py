from Token import Token
from RealFMS import RealFMS
from SourcePosition import SourcePosition

class Scanner:
  COMMENT = 0
  SPACE = 1
  TAB = 2
  STRING_UNTERMINATED = 3
  TABSIZE = 8

  def __init__(self, source, reporter):
      self.sourceFile = source
      self.sourcePos = SourcePosition()
      self.debug = False
      self.errorReporter = reporter
      self.currentSpelling = ''
      self.currentChar = self.sourceFile.getNextChar()

      self.lineCounter = 1
      self.columnCounter = 1
      self.realFMS = RealFMS()

  def enableDebugging(self):
      self.debug = True

  def accept(self):
      self.currentSpelling += '$' if self.currentChar == self.sourceFile.EOF else self.currentChar
      self.currentChar = self.sourceFile.getNextChar()
      self.sourcePos.charFinish = self.columnCounter
      self.sourcePos.lineFinish = self.lineCounter
      self.columnCounter += 1

  def ignore(self, times):
    for i in range(times):
      if (self.currentChar == '\n'):
        self.columnCounter = 1
        self.lineCounter += 1
      else:
        self.columnCounter += 1
            
      self.sourcePos.lineStart = self.lineCounter
      self.sourcePos.lineFinish = self.lineCounter
      self.sourcePos.charStart = self.columnCounter
      self.sourcePos.charFinish = self.columnCounter
      self.currentChar = self.sourceFile.getNextChar()

  # inspectChar returns the n-th character after currentChar in the input stream. 
  def inspectChar(self, nthChar):
    return self.sourceFile.inspectChar(nthChar)

  def recognizeId(self, result):
    if self.currentChar.isalpha() or self.currentChar == '_':
      self.accept()
      while self.currentChar.isalpha() or self.currentChar.isdigit() or self.currentChar == '_':
        self.accept()
      return self.Token.ID
    return result

  def recognizeBool(self, result):
    if str(self.currentSpelling) in ("True", "False"):
      return self.Token.BOOLEANLITERAL
    else:
      return result

  def recognizeReal(self, result):
    self.realFMS.reset()
    readlNumStart = self.columnCounter
    counter = 1
    markCounter = 0
    inspectChar = self.currentChar
    while True:
      while True:
        if self.realFMS.isRealSet(inspectChar):
          self.realFMS.realNextStateOfNextChar = self.realFMS.next(self.realFMS.realState, inspectChar)
          break
        else:
          if self.realFMS.realStateOfLastAccept != self.realFMS.STATE_FAILURE:
            self.realFMS.realNextStateOfNextChar = self.realFMS.STATE_FAILURE
            break
          else:
            return result
      if self.realFMS.realState != self.realFMS.STATE_FAILURE:
        if self.realFMS.realAnchor == self.realFMS.isAccept(self.realFMS.realNextStateOfNextChar):
          self.realFMS.realPrevStateOfLastAccept = self.realFMS.realState
          self.realFMS.realStateOfLastAccept = self.realFMS.realNextStateOfNextChar
          markCounter = counter
          self.realFMS.realState = self.realFMS.realNextStateOfNextChar
          inspectChar = inspectChar(counter=counter+1)
        else:
          if self.realFMS.realStateOfLastAccept == self.realFMS.STATE_FAILURE:
            return result
          else:
            if self.realFMS.realStateOfLastAccept == 1:
              self.getValidReal(readlNumStart, markCounter)
              return self.Token.INTLITERAL
            #elif self.realFMS.realStateOfLastAccept == 2:
            elif self.realFMS.realStateOfLastAccept == 6:
              self.getValidReal(readlNumStart, markCounter)
              return self.Token.FLOATLITERAL
            else:
              return result

  def getValidReal(self, readlNumStart, markCounter):
    i = markCounter
    self.sourcePos.charStart = readlNumStart
    self.sourcePos.charFinish = readlNumStart + markCounter - 1
    self.sourcePos.lineStart = self.sourcePos.lineFinish = self.lineCounter
    while i >= 2:
      i -= 1
      self.currentSpelling.append(currentChar)
      currentChar = self.sourceFile.getNextChar()
    columnCounter = self.sourcePos.charFinish + 1

  def recognizeString(self, result):
    if self.currentChar == '"':
      stringLineStart = self.lineCounter
      stringColumnStart = self.columnCounter
      # ignore(1)
      while self.currentChar != '"':
        if self.currentChar == self.SourceFile.eof or self.currentChar == '\n':
          self.errorReporter.reportError(
              str(self.currentSpelling) + ": unterminated string",\
              None,\
              SourcePosition(stringLineStart, stringColumnStart, stringColumnStart))
          self.sourcePos.charStart = stringColumnStart
          return self.Token.STRINGLITERAL
                
        if self.currentChar == '\\':
          legal = self.escapeHandler(self.inspectChar(1))
          if legal == '0':
            self.errorReporter.reportError(
                "\\" + str(self.inspectChar(1)) + ": illegal escape character", 
                None, 
                SourcePosition(stringLineStart, stringColumnStart, self.sourcePos.charFinish + 1))
            self.accept()
            self.accept()
          else:
            self.currentSpelling.append(legal)
            # ignore(2)
          continue
        
        self.accept()
      
      self.sourcePos.charStart = stringColumnStart
      self.sourcePos.charFinish = self.columnCounter
      self.currentChar = self.sourceFile.getNextChar()
      self.columnCounter+=1
      return self.Token.STRINGLITERAL
    
    return -1


  def escapeHandler(inspectChar):
    return_dict = {
      'b': '\b',
      'f': '\f',
      'n': '\n',
      'r': '\r',
      't': '\t',
      '\'': '\'',
      '\"': '\"',
      '\\': '\\'
    }

    if inspectChar in return_dict.keys():
      return return_dict[inspectChar]
    return '0'


  def nextToken(self):
    # Tokens: separators operators literals identifiers and keyworods
    # return_dict = {
    #   '+': self.Token.PLUS,
    #   '-': self.Token.MINUS,
    #   '*': self.Token.MULT,
    #   '{': self.Token.LCURLY,
    #   '': self.Token.SEMICOLON
    # }
    if self.currentChar == '+':
      self.accept()
      return self.Token.PLUS
    elif self.currentChar == '-':
      self.accept()
      return self.Token.MINUS
    elif self.currentChar == '*':
      self.accept()
      return self.Token.MULT
    elif self.currentChar == '/':
      if self.inspectChar(1) == '*' or self.inspectChar(1) == '/':
          return self.COMMENT
      self.accept()
      return self.Token.DIV
    elif self.currentChar == '!':
      self.accept()
      if self.currentChar == '=':
        self.accept()
        return self.Token.NOTEQ
      return self.Token.NOT
    elif self.currentChar == '=':
        self.accept()
        if self.currentChar == '=':
          self.accept()
          return self.Token.EQEQ
        return self.Token.EQ
    elif self.currentChar == '<':
        self.accept()
        if self.currentChar == '=':
            self.accept()
            return self.Token.LTEQ
        return self.Token.LT
    elif self.currentChar == '>':
        self.accept()
        if self.currentChar == '=': # case: >=
            self.accept()
            return self.Token.GTEQ
        return self.Token.GT
    elif self.currentChar == '&':
        self.accept()
        if self.currentChar == '&': # case: &&
          self.accept()
          return self.Token.ANDAND
        return self.Token.ERROR
    elif self.currentChar == '|':
        self.accept()
        if self.currentChar == '|': # case: ||
          self.accept()
          return self.Token.OROR
        return self.Token.ERROR
    elif self.currentChar == '{':
        self.accept()
        return self.Token.LCURLY
    elif self.currentChar == '':
        self.accept()
        return self.Token.RCURLY
    elif self.currentChar == '(':
        self.accept()
        return self.Token.LPAREN
    elif self.currentChar == ')':
        self.accept()
        return self.Token.RPAREN
    elif self.currentChar == '[':
        self.accept()
        return self.Token.LBRACKET
    elif self.currentChar == ']':
        self.accept()
        return self.Token.RBRACKET
    elif self.currentChar == '':
        self.accept()
        return self.Token.SEMICOLON
    elif self.currentChar == '':
        self.accept()
        return self.Token.COMMA
    elif self.currentChar == ' ':
        return self.SPACE
    elif currentChar == '\t':
      if self.columnCounter > self.TABSIZE:
          columnCounter = self.TABSIZE - (columnCounter - 1) % 8 + columnCounter
      else:
          columnCounter = self.TABSIZE + 1 
      
      currentChar = self.sourceFile.getNextChar()
      return self.TAB	
    elif currentChar == self.SourceFile.EOF:
        self.accept()
        return self.Token.EOF
    # else:
    #   break
    
    result = -1
    result = self.recognizeId(result)
    result = self.recognizeBool(result)
    if result == self.Token.BOOLEANLITERAL:
      return self.Token.BOOLEANLITERAL
    
    if result == self.Token.ID:
      return self.Token.ID
    
    result = self.recognizeString(result)
    if result == self.Token.STRINGLITERAL:
      return self.Token.STRINGLITERAL
    
    if result == self.STRING_UNTERMINATED:
      return self.STRING_UNTERMINATED
    
    result = self.recognizeReal(result)
    if result == self.Token.INTLITERAL:
      return self.Token.INTLITERAL
    
    if result == self.Token.FLOATLITERAL:
      return self.Token.FLOATLITERAL
    
    self.skipSpaceAndComments()
    self.accept() 
    return self.Token.ERROR


  def skipSpaceAndComments(self):
    if self.currentChar == '/' and self.inspectChar(1) == '*':
      self.terminatedColumnStart = columnCounter
      tempChar1 = chr(0)
      tempChar2 = chr(0)
      counter = 1
      lineNum = 0 
      columnNum = columnCounter
      flag = True
      while (True):
        tempChar1 = self.inspectChar(counter)
        tempChar2 = self.inspectChar(counter + 1)
        if (tempChar1 == '*' and tempChar2 == '/'):
          counter+=1
          columnNum = columnNum + 2
          break
        elif tempChar1 == '\n':
          lineNum +=1
          columnNum = 1
        elif self.SourceFile.eof == tempChar1:
          flag = False
          break
        else:
          columnNum += 1
        counter += 1
      
      if flag == False:
        self.errorReporter.reportError(": unterminated comment", \
                                      str(self.inspectChar(1)), \
                                      SourcePosition(lineCounter, self.terminatedColumnStart, self.terminatedColumnStart))
        while(True):
          if (self.SourceFile.EOF == currentChar):
            break
        
      else:
        lineCounter = lineCounter + lineNum
        columnCounter = columnNum + 1
        while counter >= 1:
          counter -= 1
          currentChar = self.sourceFile.getNextChar()
        
      
    
    # if currentChar == '/' and self.inspectChar(1) == '/':
    #   # ignore(2)
    #   while currentChar != '\n':
    #     # ignore(1)
      
    #   # ignore(1)
    
    # while currentChar == ' ' or currentChar == '\n':
      # ignore(1)
      
  def getToken(self):
    tok = Token()
    kind = 0
    while True:
      sourcePos = SourcePosition()
      currentSpelling = ''
      sourcePos.charStart = self.columnCounter
      sourcePos.lineStart = self.lineCounter
      self.skipSpaceAndComments()
      kind = self.nextToken()
      if kind != self.COMMENT and kind != self.SPACE and kind != self.TAB and kind != self.STRING_UNTERMINATED:
        break
    tok = Token(kind, str(currentSpelling), sourcePos)
		# * do not remove these three lines
    if self.debug:
      print(tok)
    return tok