import os

class SourceFile:
  # eof = '\u0000'
  # reader = LineNumberReader()

  def __init__(self, filename):
    self.EOF = '\u0000'
    if os.path.exists(filename):
      self.reader = open(filename, 'r')
    else:
      raise Exception(f"{filename} does not exist")
    # try:
    #self.reader = FileReader(filename)
    # except (FileNotFoundException e):
    #   print("[# vc #]: can't read: " + filename)
    #   # exit(1)
    # except (Exception e):
    #   e.printStackTrace()
    #   print("Caught IOException: " + e.getMessage())
      # exit(1)

  def getNextChar(self):
    try:
      c = self.reader.read()
      if c == -1:
          c = '' #EOF
      return str(c)
    except Exception:
      print("Caught IOException: " + Exception)
      return ''
      
  def inspectChar(self, nthChar):
  # nthChar must be >= 1.
    if nthChar < 1:
      return 1

    try:
      self.reader.mark(nthChar)
      while nthChar != 0:
            c = self.reader.read()
            nthChar -= 1
      self.reader.reset()
      if c == -1: 
          c = ''
      return str(c)
    except:
      print("Caught IOException")
      return ''