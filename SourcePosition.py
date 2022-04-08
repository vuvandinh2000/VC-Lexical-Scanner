# This class is used to store the positions of tokens and phrases

class SourcePosition:
  # can be called by the scanner to store the position of a token
	def __init__(self, theLineNum=0, theCharStart=0, theCharFinish=0):
		self.lineStart = self.lineFinish = theLineNum 
		self.charStart = theCharStart
		self.charFinish = theCharFinish

	def toString(self):
		return self.lineStart + "(" + self.charStart + ").." + self.lineFinish + "(" + self.charFinish + ")"
