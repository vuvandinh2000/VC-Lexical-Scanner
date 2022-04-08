# ====== PLEASE DO NOT MODIFY THIS FILE =====

class Token(Object):

  kind = 0
  spelling = '' # lexeme 
  position = SourcePosition()

  def __init__(self, kind, spelling, position):

    if kind == Token.ID:
      currentKind = firstReservedWord
      searching = True

      while searching:
        comparison = keywords[currentKind].compareTo(spelling)
        if comparison == 0:
          self.kind = currentKind
          searching = False
        elif (comparison > 0 or currentKind == lastReservedWord):
          self.kind = Token.ID
          searching = False
        else:
          currentKind+=1
    else
      self.kind = kind

    this.spelling = spelling
    this.position = position

  def spell(kind):
    return keywords[kind]

  def toString():
    return "Kind = " + kind + " [" + spell(kind) + 
          "], spelling = \"" + spelling + "\", position = " + position
#    return "Kind=" + kind + " [" + spell(kind) + 
#            "], spelling=\"" + spelling + "\", pos=" + position

  # Token classes...

    # reserved words - must be in alphabetical order...
    BOOLEAN		= 0,
    BREAK		= 1,
    CONTINUE	= 2,
    ELSE		= 3,
    FLOAT 		= 4,
    FOR         = 5,
    IF			= 6,
    INT         = 7,
    RETURN		= 8,
    VOID		= 9,
    WHILE		= 10,

    # operators
    PLUS		= 11,
    MINUS		= 12,
    MULT		= 13,
    DIV			= 14,
    NOT			= 15,
    NOTEQ		= 16,
    EQ			= 17,
    EQEQ		= 18,
    LT			= 19,
    LTEQ		= 20,
    GT			= 21,
    GTEQ		= 22,
    ANDAND		= 23,
    OROR		= 24,

    # separators
    LCURLY		= 25,
    RCURLY		= 26,
    LPAREN		= 27,
    RPAREN		= 28,
    LBRACKET    = 29,
    RBRACKET    = 30,
    SEMICOLON   = 31,
    COMMA		= 32,

    # identifiers
    ID			= 33,

    # literals
    INTLITERAL 		= 34,
    FLOATLITERAL	= 35,
    BOOLEANLITERAL	= 36,
    STRINGLITERAL	= 37,


    # special tokens...
    ERROR		= 38,
    EOF			= 39

  def keywords = [
    "boolean",
    "break",
    "continue",
    "else",
    "float",
    "for",
    "if",
    "int",
    "return",
    "void",
    "while",
    "+",
    "-",
    "*",
    "/",
    "!",
    "!=",
    "=",
    "==",
    "<",
    "<=",
    ">",
    ">=",
    "&&",
    "||",
    "{",
    "}",
    "(",
    ")",
    "[",
    "]",
    "",
    ",",
    "<id>",
    "<int-literal>",
    "<float-literal>",
    "<boolean-literal>",
    "<string-literal>",
    "<error>",
    "$"
  ]

    firstReservedWord = Token.BOOLEAN, lastReservedWord  = Token.WHILE
