from SourceFile import SourceFile
from ErrorReporter import ErrorReporter
from Scanner import Scanner
from Token import Token

# scanner = Scanner()
# reporter = ErrorReporter()
# currentToken = Token()
# inputFilename = String()

if __name__=="__main__":
    # inputFilename = args[0]

    inputFilename = "sample/string.vc"
    # inputFilename = "src/VC/Scanner/comment2.vc"
    # inputFilename = "src/VC/Scanner/comment3.vc"
    # inputFilename = "src/VC/Scanner/comment4.vc"
    # inputFilename = "src/VC/Scanner/error1.vc"
    # inputFilename = "src/VC/Scanner/error2.vc"
    # inputFilename = "src/VC/Scanner/error3.vc"
    # inputFilename = "src/VC/Scanner/error4.vc"
    # inputFilename = "src/VC/Scanner/escape.vc"
    # inputFilename = "src/VC/Scanner/longestmatch.vc"
    # inputFilename = "src/VC/Scanner/fib.vc"
    # inputFilename = "src/VC/Scanner/string.vc"
    # inputFilename = "src/VC/Scanner/tab.vc"
    # inputFilename = "src/VC/Scanner/tokens.vc"
    # inputFilename = "src/VC/Scanner/fib.vc"

    # inputFilename = "src/VC/Scanner/mytest01.vc"
    # inputFilename = "src/VC/Scanner/mytest02.vc"
    # inputFilename = "src/VC/Scanner/mytest03.vc"
    # inputFilename = "src/VC/Scanner/mytest04.vc"
    # inputFilename = "src/VC/Scanner/testASCII.vc"

    print("======= The VC compiler =======")

    source = SourceFile(inputFilename)
    print(str(source.reader.read()))

    reporter = ErrorReporter()
    scanner  = Scanner(source, reporter)
    scanner.enableDebugging()
        
    while currentToken.kind != Token.EOF:
        currentToken = scanner.getToken()