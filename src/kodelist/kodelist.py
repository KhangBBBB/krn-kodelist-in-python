#!/usr/bin/env python3
# coding=utf-8


# Author: Khang Bao.
# Since: March 04, 2021
# Version: 0.3



#===== SOURCE CODE OF KODELIST PREPROCESSOR =====#



import re
import sys

# Marker handling
# [x] CODES
# [x] CODEE
# [x] RESULTS
# [x] RESULTE
# [x] CS
# [x] CE

# Cli options
# [x] help
# [x] nonumber
# [x] width


# tokens type
NORMAL = "NORMAL"
CODE_BODY = "CODE_BODY"
CODE_END = "CODE_END"
CS_START="CS_START"
CS_BODY = "CS_BODY"
CS_END = "CE_END"
RESULT_START = "RESULT_START"
RESULT_BODY = "RESULT_BODY"
RESULT_END = "RESULT_END"


# keywords/patterns
MARKER = "."
START_MARKER = "CODES"
END_MARKER = "CODEE"
CS_START_MARKER = "CS"
CS_END_MARKER = "CE"
# not implement yet
RESULT_START_MARKER = "RESULTS"
RESULT_END_MARKER = "RESULTE"


# sessionId = str(lang) + SEPARATOR + str(name)
SEPARATOR = "@"


def split_command_to_token(line):
    """
    Split a line of command (Troff syntax) into tokens
    """

    if MARKER == '.':
        tokenList = ([i for i in re.split(r"(\.|\")|[ |\n]", line) if i])
    elif MARKER == '\\':
        tokenList = ([i for i in re.split(r"(" + ("\\" + MARKER) + "|\")|[ |\n]", line) if i])
    else:
        tokenList = ([i for i in re.split(r"(" + MARKER + "|\")|[ |\n]", line) if i])
    parseList1 = []
    f1 = False
    i = 0
    if len(tokenList) > 2:
       if tokenList[0] == MARKER and tokenList[1] == '\\' and tokenList[2] == '\"': 
           return [MARKER]
       
    for s in tokenList:
        i += 1
        if f1 and s != '"':
            parseList1[len(parseList1) - 1] += s
            continue
        if f1 and s == '"':
            f1 = False
            continue
        if s == '"':
            parseList1.append("")
            f1 = True
            continue
        parseList1.append(s)
    if f1 == True:
        return None

    parseList2 = []
    i = 0
    f1 = False
    for s in parseList1:
        i += 1 
        if f1:
            parseList2[len(parseList2) - 1] += s
            f1 = False
            continue
        if i > 1 and s == MARKER:
            parseList2[len(parseList2) - 1] += s
            f1 = True
            continue
        parseList2.append(s)

    parseList = parseList2
    return parseList


def processStartMarkerList(parseList):
    """
    Process the line that properly contains the startMarker.
    """

    inCodeFlag = True
    lang, name, password = None, None, None

    if len(parseList) > 2:
        if SEPARATOR in parseList[2]:
            sys.exit("Character " +  SEPARATOR + " can't be used for session language.")
        if parseList[2] != "":
            lang = parseList[2]
    if len(parseList) > 3:
        if SEPARATOR in parseList[3]:
            sys.exit("Character " +  SEPARATOR + " can't be used for session name.")
        if parseList[3] != "":
            name = parseList[3]
    if len(parseList) > 4:
        if parseList[4] != "":
            password = parseList[4]

    return (inCodeFlag, lang, name, password)


def processResultStartMarkerList(parseList):
    """
    Process result start marker command
    """

    inResultFlag = True
    lang, name, password = None, None, None

    if len(parseList) > 2:
        if SEPARATOR in parseList[2]:
            sys.exit("Character " +  SEPARATOR + " can't be used for session language.")
        if parseList[2] != "":
            lang = parseList[2]
    if len(parseList) > 3:
        if SEPARATOR in parseList[3]:
            sys.exit("Character " +  SEPARATOR + " can't be used for session name.")
        if parseList[3] != "":
            name = parseList[3]
    if len(parseList) > 4:
        if parseList[4] != "":
            password = parseList[4]

    return (inResultFlag, lang, name, password)


def processResultEndMarkerList(parseList):
    """
    Process result end marker command
    """

    password = None

    if len(parseList) > 2:
        if parseList[2] != "":
            password = parseList[2]

    return password


def processCSStartMarkerList(parseList):
    """
    Process result start marker command
    """

    inResultFlag = True
    lang, name, password = None, None, None

    if len(parseList) > 2:
        if SEPARATOR in parseList[2]:
            sys.exit("Character " +  SEPARATOR + " can't be used for session language.")
        if parseList[2] != "":
            lang = parseList[2]
    if len(parseList) > 3:
        if SEPARATOR in parseList[3]:
            sys.exit("Character " +  SEPARATOR + " can't be used for session name.")
        if parseList[3] != "":
            name = parseList[3]
    if len(parseList) > 4:
        if parseList[4] != "":
            password = parseList[4]

    return (inResultFlag, lang, name, password)


def processCSEndMarkerList(parseList):
    """
    Process result end marker command
    """

    password = None

    if len(parseList) > 2:
        if parseList[2] != "":
            password = parseList[2]

    return password


def processEndMarkerList(parseList):
    """
    Process the line that properly contains the endMarker.
    """

    password = None

    if len(parseList) > 2:
        if parseList[2] != "":
            password = parseList[2]

    return password


def kodelistLexAnalyzer(lineList):
    """
    Lexical analyzer for the list of lines
    """

    numLine = 0
    tokens = []
    lineTokList = []

    # For code
    inCodeFlag = False
    lang = None
    name = None
    password = None
    endPassword = None

    # For result
    inResultFlag = False
    resultLang = None
    resultName = None
    resultPassword = None
    resultEndPassword = None

    # For CS
    inCSFlag = False
    CSLang = None
    CSName = None
    CSPassword = None
    CSEndPassword = None

    for line in lineList:
        numLine += 1
        if line[0] == MARKER:
            lineTokList = split_command_to_token(line)
            if lineTokList == None and inCodeFlag == False and inResultFlag == False and inCSFlag == False:
                # sys.exit("Missing quote at line " + str(numLine))
                lineTokList = []
            if lineTokList == None:
                lineTokList = []
        if len(lineTokList) > 1:
            # Result start marker
            if lineTokList[1] == RESULT_START_MARKER and inCodeFlag == False and inResultFlag == False and inCSFlag == False:
                inResultFlag, resultLang, resultName, resultPassword = processResultStartMarkerList(lineTokList)
                tokens.append([RESULT_START, line])
            # Result end marker
            elif lineTokList[1] == RESULT_END_MARKER and inCodeFlag == False and inResultFlag == True and inCSFlag == False:
                resultEndPassword = processResultEndMarkerList(lineTokList)
                if resultPassword == resultEndPassword:
                    inResultFlag = False
                    tokens.append([RESULT_END, line])
                else:
                    tokens.append([RESULT_BODY, line])
            # CS start marker
            elif lineTokList[1] == CS_START_MARKER and inCodeFlag == False and inResultFlag == False and inCSFlag == False:
                inCSFlag, csLang, csName, csPassword = processResultStartMarkerList(lineTokList)
                tokens.append([CS_START, line])
            # CE end marker
            elif lineTokList[1] == CS_END_MARKER and inCodeFlag == False and inResultFlag == False and inCSFlag == True:
                csEndPassword = processResultEndMarkerList(lineTokList)
                if resultPassword == resultEndPassword:
                    inCSFlag = False
                    tokens.append([CS_END, line])
                else:
                    tokens.append([CS_BODY, line])
            # Code start line
            elif lineTokList[1] == START_MARKER and inCodeFlag == False and inResultFlag == False and inCSFlag == False:
                inCodeFlag, lang, name, password = processStartMarkerList(lineTokList)
                sessionId = str(lang) + SEPARATOR + str(name)
                tokens.append([sessionId, line])
            # Code end line
            elif lineTokList[1] == END_MARKER and inCodeFlag == True and inResultFlag == False and inCSFlag == False:
                endPassword = processEndMarkerList(lineTokList)
                if password == endPassword:
                    inCodeFlag = False
                    tokens.append([CODE_END, line])
                else:
                    tokens.append([CODE_BODY, line])
            # Code body line
            elif inCodeFlag == True and inResultFlag == False and inCSFlag == False:
                tokens.append([CODE_BODY, line])
            # Result body line
            elif inCodeFlag == False and inResultFlag == True and inCSFlag == False:
                tokens.append([RESULT_BODY, line])
            # CS body line
            elif inCodeFlag == False and inResultFlag == False and inCSFlag == True:
                tokens.append([CS_BODY, line])
            # Normal line
            elif inCodeFlag == False and inResultFlag == False and inCSFlag == False:
                tokens.append([NORMAL, line])
            lineTokList = [] 
        # Code body line
        elif inCodeFlag == True and inResultFlag == False and inCSFlag == False:
            tokens.append([CODE_BODY, line])
        # Result body line
        elif inCodeFlag == False and inResultFlag == True and inCSFlag == False:
            tokens.append([RESULT_BODY, line])
        # CS body line
        elif inCodeFlag == False and inResultFlag == False and inCSFlag == True:
            tokens.append([CS_BODY, line])
        else:
            tokens.append([NORMAL, line])

    return tokens


def formatCodeWidth(line, maxWidth, startSpace, tabSize):
    """
    Break the line into multiples lines according to the maxWidth.
    """

    width = 0
    nLine = ""

    if tabSize != None:
        line = line.expandtabs(tabsize = tabSize)
    for c in line:
        width += 1
        if width == maxWidth:
            nLine += '\n' +  '       ' + startSpace + c
            width = 1
        else:
           nLine += c

    return nLine


def formatCodeChar(s):
    """
    Turn special character into Troff character set.
    """

    result = ""

    for c in s:
        if c == '\\':
            result += '\\[rs]'
        elif c == '"':
            result += '\\[quotedbl]'
        elif c == '\'':
            result += '\\[quotesingle]'
        elif c == '#':
            result += '\\[numbersign]'
        elif c == '$':
            result += '\\[dollar]'
        elif c == '|':
            result += '\\[bar]'
        else:
            result += c

    return result


def processTokens(tokens, maxWidth = 70, startSpace = ' ', numberFlag = True, tabSize = 8, numLineColor = "\\*[codeNumColor]", codeColor = "\\*[codeColor]"):
    """
    Process tokens.
    """

    buffer = ''
    lineNumDict = {}
    currentId = ''

    for token in tokens:
        if token[0] == NORMAL:
            buffer += token[1]
        elif token[0] == CODE_END:
            buffer += token[1]
        elif token[0] == CODE_BODY:
            lineNumDict[currentId] += 1
            temp = token[1]
            temp = formatCodeWidth(temp, maxWidth, startSpace, tabSize = tabSize)
            temp = formatCodeChar(temp)
            if numberFlag == True:
                s = (numLineColor + '%7d' + codeColor + startSpace) % (lineNumDict[currentId])
                s += temp
            else:
                s = '       ' + startSpace + temp
            buffer += s
        elif token[0] == RESULT_START:
            buffer += token[1]
        elif token[0] == RESULT_BODY:
            temp = token[1]
            temp = formatCodeWidth(temp, maxWidth, startSpace, tabSize = tabSize)
            temp = formatCodeChar(temp)
            s = "      " + numLineColor + "|" + codeColor + startSpace + temp
            buffer += s
        elif token[0] == RESULT_END:
            buffer += token[1]
        elif token[0] == CS_START:
            buffer += token[1]
        elif token[0] == CS_BODY:
            temp = token[1]
            temp = formatCodeWidth(temp, maxWidth, startSpace, tabSize = tabSize)
            temp = formatCodeChar(temp)
            s = "      " + numLineColor + "+" + codeColor + startSpace + temp
            buffer += s
        elif token[0] == CS_END:
            buffer += token[1]
        else:
            buffer += token[1]
            currentId = token[0]
            if token[0] not in lineNumDict:
                lineNumDict[token[0]] = 0

    return buffer


def print_help_msg():
    """
    Print the help message.
    """

    print(
"""
kodelist - a preprocessor to format source code for Troff typesetting engine.

Usage:

    kodelist [option] [option]

Options:

    -h
    -help
        print this help message.
    -nonumber
        turn off numbering.
    -w
    -width
        set maximum width for the code body.

Example:

    Run kodelist with default option:
        cat file.mk | kodelist | troff -mkdoc -x | hdpost | ps2pdf - file.pdf
    Run kodelist with no numbering:
        cat file.mk | kodelist -nonumber | troff -mkdoc -x | hdpost | ps2pdf - file.pdf
    Run kodelist with maximum code line width = 70 and no numbering:
        cat file.mk | kodelist -nonumber -width 70 | troff -mkdoc -x | hdpost | ps2pdf - file.pdf

Note:

    kodelist should be used before tbl, eqn, pic, klean, klush preprocessors.

About

    Author: Khang Bao
    Version: 0.3
    Since: March 04, 2021
""", end='')


def processCommandlineOptions(args):
    """
    Process the commandline arguments.
    """

    argc = len(args)
    maxWidth = None
    numberFlag = True

    if argc > 1:
        if args[1] == "-help" or args[1] == "-h":
            print_help_msg()
            sys.exit()
        elif args[1] == '-nonumber':
            numberFlag = False
            if argc > 2:
                if args[2] == '-width' or args[2] == "-w":
                    if argc > 2:
                        if args[3].isnumeric():
                            maxWidth = int(args[3])
                        else:
                            sys.exit("Argument after -width option must be an integer.")
                    else:
                        sys.exit("Missing argument after -width option.")
                else:
                    sys.exit("Option not found. Use -help for help message.")
        elif args[1] == '-width' or args[1] == "-w":
            if argc > 2:
                if args[2].isnumeric():
                    maxWidth = int(args[2])
                    if argc > 3:
                        if args[3] == '-nonumber' or args[3] == "-n":
                            numberFlag = True
                        else:
                            sys.exit("Argument after -width option must be an integer.")
                else:
                    sys.exit("Argument after -width option must be an integer.")
            else:
                sys.exit("Missing argument after -width option.")
        else:
            sys.exit("Option not found. Use -help for help message.")

    return (maxWidth, numberFlag)
     

def processKdocMain(lineList):
    """
    Main function that process the list of lines and print to standard output.
    """

    maxWidth, numberFlag = processCommandlineOptions(sys.argv)

    if maxWidth != None:
        tokens = kodelistLexAnalyzer(lineList)
        s = processTokens(tokens, maxWidth = maxWidth, numberFlag = numberFlag)
        print(s)
    else:
        tokens = kodelistLexAnalyzer(lineList)
        s = processTokens(tokens, maxWidth = 70, numberFlag = numberFlag)
        print(s)


if __name__ == "__main__":
    processKdocMain(sys.stdin)
