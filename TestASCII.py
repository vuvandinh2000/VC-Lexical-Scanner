if __name__ == "__main__":
    fileWriter = open("D:\Study\HK8\Compiler\BTL\VC-Scanner/test_res/testASCII.vc", 'w+')
    cbuf = ''
    cbuf += chr(7)
    cbuf += chr(66)
    cbuf += chr(67)
    cbuf += chr(68)

    string = "\n234\n"
    print(string)

    fileWriter.write(cbuf)
    fileWriter.write("\n")
    fileWriter.write("\"!!\"")
    fileWriter.write("\nend")
    print("done.")
    fileWriter.flush()
    fileWriter.close()