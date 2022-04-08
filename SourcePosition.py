# This class is used to store the positions of tokens and phrases

class SourcePosition:
	def __init__(self):
		self.lineStart = 0
		self.lineFinish = 0
		self.charStart = 0
		self.charFinish = 0

  # can be called by the parser to store the position of a phrase
	def __init__(self, theLineStart, theLineFinish):
		self.lineStart = theLineStart
		self.lineFinish = theLineFinish
		self.charStart = 0
		self.charFinish = 0

  # can be called by the scanner to store the position of a token
	def __init__(self, theLineNum, theCharStart, theCharFinish):
		self.lineStart = self.lineFinish = theLineNum 
		self.charStart = theCharStart
		self.charFinish = theCharFinish

	def toString(self):
		return self.lineStart + "(" + self.charStart + ").." + self.lineFinish + "(" + self.charFinish + ")"
