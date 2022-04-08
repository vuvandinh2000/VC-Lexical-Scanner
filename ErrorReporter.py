# import VC.Scanner.SourcePosition;

class ErrorReporter:
  def __init__(self):
    self.numErrors = 0

  def reportError(self, message, tokenName, pos):
    print("ERROR: ")
    print(pos.lineStart + "(" + pos.charStart + ").." +
          pos.lineFinish+ "( " + pos.charFinish + "): ")

    for  p in range(len(message)):
      if message.charAt(p) == '%':
        print(tokenName)
      else:
        print(message.charAt(p))

    print()
    self.numErrors+=1

  def reportRestriction(message):
    print("RESTRICTION: " + message)