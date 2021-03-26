#!/usr/bin/python
# coding=utf-8



# Author : Khang Bao.
# Since : March 12, 2021
# Version : 0.4



#===== SOURCE CODE OF KRUN PROGRAM =====#



# # Command/Requests Implementation:
# [x] CODES
# [x] CODEE
# [x] RESULTS
# [x] RESULTE
# [x] RUN
# [x] EVALUATE
# [x] TOFILE
# [x] CAPTURE
# [x] ORDER
# [x] LANGUAGE 
# [x] PROCESSOR
# [x] FILENAME
# [ ] REPLACE : should turn off if redefine again.

# # Cli Options Implementation:
# [x] help
# [x] check
# [x] stat
# [x] run
# [x] evaluate
# [x] tofile
# [x] id
# [x] output (yaml)
# [x] executestdin
# [x] <file-name>

# # Keyword
# [x] STDIN@STDIN@STDIN
# [x] FILENAME

# check option should also show the location of the buffer.


from distutils.spawn import find_executable
import subprocess
import random
import sys
import re
import os
import copy
import platform



class MetaprogramKeywordProcessor:
    """
    This class contain function to process keywords for metaprogramming.
    """

    DELIMETER = ":::"
    STDIN_NAME = "STDIN"


    def makeMetaprogramKeyword(lang = None, name = None, keyword = None):
        """
        Make keyword for a session for metaprogramming.
        """

        return  MetaprogramKeywordProcessor.DELIMETER + \
                str(lang) + \
                sessionIdProcessor.SEPARATOR + \
                str(name) + \
                sessionIdProcessor.SEPARATOR + \
                str(keyword) + \
                MetaprogramKeywordProcessor.DELIMETER


    def getMetaprogramStdinKeyword():
        """
        Return keyword for stdin.
        """

        return  MetaprogramKeywordProcessor.DELIMETER + \
                MetaprogramKeywordProcessor.STDIN_NAME + \
                sessionIdProcessor.SEPARATOR + \
                MetaprogramKeywordProcessor.STDIN_NAME + \
                sessionIdProcessor.SEPARATOR + \
                MetaprogramKeywordProcessor.STDIN_NAME + \
                MetaprogramKeywordProcessor.DELIMETER



class PlatformProcessor():
    """
    This class contains functions to process current platform characteristics.
    """

    def isExecutable(name):
        """
        Check whether a program is on PATH.
        """

        if find_executable(name) == None:
            return False
        else:
            return True


    def checkOS():
        """
        Check which OS is the computer.
        """

        return platform.system() # Linux, Windows, Darwin



class sessionIdProcessor:
    """
    This class contains function to process code session id.
    """

    SEPARATOR = '@' # example: session id is python@example.py


    def makeSessionId(lang = None, name = None):
        """
        Make id for session from lang and name
        """

        return str(lang) + \
               sessionIdProcessor.SEPARATOR + \
               str(name)


    def isCodesSameSession(lang1, name1, lang2, name2):
        """
        Check if 2 pieces of code belong to the same session.
        """

        if sessionIdProcessor.makeSessionId(lang1, name1) == sessionIdProcessor.makeSessionId(lang2, name2):
            return True

        return False


    def getLangFromId(sessionId):
        """
        Extract language from session id
        """

        tokens = sessionId.split(sessionIdProcessor.SEPARATOR)
        if tokens[1] == '':
            lang = None
        else:
            lang = tokens[0]

        return lang


    def getNameFromId(sessionId):
        """
        Extract language from session id
        """

        tokens = sessionId.split(sessionIdProcessor.SEPARATOR)
        if tokens[1] == '':
            name = None
        else:
            name = tokens[1]

        return name



class FileNameProcessor:
    """
    This class contains functions to process file name.
    """

    SEPARATOR = '-'


    def makeFileName(lang = None, name = None, directory = None):
        """
        Return a file name
        """

        if directory == None:
             if name == None:
                 return str(lang) + FileNameProcessor.SEPARATOR + str(name)
             else:
                 return str(name)
        else:
             return str(directory)



class CodeSegment:
    """
    This class stores information about a code segment of a code session.
    """

    def __init__(self, lineNum):
        self.lineNum = lineNum
        self.code = ""


    def addCode(self, code):
        """
        Add code to the segment.
        """

        self.code += code


    def getCode(self):
        """
        Returns the code of the segment.
        """

        return self.code


    def getLineNum(self):
        """
        Return the line number of the top of this code segment.
        """

        return self.lineNum


    def getEndLineNum(self):
        """
        Return total number of line
        """

        return self.lineNum + self.code.count('\n')



class CodeSession:
    """
    This class store information about a code session
    """

    def __init__ (self, lang = None, name = None):
        self.lineNum = -1
        self.lang = lang
        self.name = name
        self.id = sessionIdProcessor.makeSessionId(lang, name)
        self.codeSegmentList = []
        self.isRun = False
        self.runLine = None
        self.isTofile = False
        self.directory = None
        self.isEvaluate = False
        self.evaluateLine = None
        self.isInterpreter = False
        self.interpreter = {"processor" : None, "arguments" : None}
        self.output = None # use for metaprogramming
        self.isCapture = False # use for metaprogramming
        self.captureLine = None
        self.captureKeyword = None
        self.isOrder = None
        self.orderLine = None


    def addCode(self, lineNum, code):
        """
        Add code to the session.
        """

        if (self.lineNum + 1) == lineNum:
            # add to current segment.
            self.codeSegmentList[-1].addCode(code)
            self.lineNum = lineNum
        else:
            # create new segments.
            tempSegment = CodeSegment(lineNum)
            self.codeSegmentList.append(tempSegment)
            self.codeSegmentList[-1].addCode(code)
            self.lineNum = lineNum


    def getCode(self):
        """
        Get code of the session and return as as a string.
        """

        buffer = ""

        for seg in self.codeSegmentList:
            buffer += seg.getCode()

        return buffer


    def getCodeBeforeEvaluateCommand(self):
        """
        Return the code before evaluate command.
        """

        buffer = ""

        for segment in self.codeSegmentList:
            if self.evaluateLine != None:
                if self.evaluateLine > segment.lineNum:
                    buffer += segment.code

        return buffer


    def getCodeAfterRunCommand(self):
        """
        Return the code before evaluate command.
        """

        buffer = ""

        for segment in self.codeSegmentList:
            if self.runLine > segment.lineNum:
                buffer += segment.code

        return buffer


    def getFirstLine(self):
        """
        Return the first line of the block.
        """

        if len(self.codeSegmentList) > 0:
            return self.codeSegmentList[0].lineNum
        else:
            return -1
            return None



class CodeSessionArr:
    """
    This class stores a collection of CodeSession objects.
    """

    def __init__(self):
        self.sessionList = []


    def isInSessionList(self, lang, name):
        """
        Check if there is any session that contains this lang and name.
        """

        for session in self.sessionList:
            if session.id == sessionIdProcessor.makeSessionId(lang, name):
                return True

        return False


    def getSession(self, lang, name):
        """
        Returns the session with the specific lang and name.
        """

        for session in self.sessionList:
            if session.id == sessionIdProcessor.makeSessionId(lang, name):
                return session

        return None


    def addCode(self, lineNum = None, code = "", lang = None, name = None, isRun = None, isTofile = None, isInterpreter = None, isCapture = None, directory = None, evaluateLine = None, runLine = None, interpreter = None, keyword = None, isOrder = None, orderLine = None):
        """
        Add code to the CodeSessionArr object.
        """

        if runLine != None:
            if self.isInSessionList(lang, name):
                # self.getSession(lang, name).isEvaluate = True
                self.getSession(lang, name).isRun = True
            else:
                self.sessionList.append(CodeSession(lang, name))
            self.getSession(lang, name).runLine = runLine
            self.getSession(lang, name).isRun = True
        elif evaluateLine != None:
            if self.isInSessionList(lang, name):
                self.getSession(lang, name).isEvaluate = True
            else:
                self.sessionList.append(CodeSession(lang, name))
            self.getSession(lang, name).isEvaluate = True
            self.getSession(lang, name).evaluateLine = evaluateLine
        elif isTofile == True:
            if self.isInSessionList(lang, name):
                self.getSession(lang, name).isTofile = True
                if directory != None:
                    self.getSession(lang, name).directory = directory
            else:
                self.sessionList.append(CodeSession(lang, name))
                self.getSession(lang, name).isTofile = True
                if directory != None:
                    self.getSession(lang, name).directory = directory
        elif isCapture == True:
            if self.isInSessionList(lang, name) == False:
                self.sessionList.append(CodeSession(lang, name))
            self.getSession(lang, name).isCapture = True
            self.getSession(lang, name).captureKeyword = MetaprogramKeywordProcessor.makeMetaprogramKeyword(lang, name, keyword)

        elif isInterpreter == True:
            if self.isInSessionList(lang, name):
                self.getSession(lang, name).isInterpreter = True
                if interpreter != None:
                    self.getSession(lang, name).interpreter = interpreter
            else:
                self.sessionList.append(CodeSession(lang, name))
                self.getSession(lang, name).isInterpreter = True
                if interpreter != None:
                    self.getSession(lang, name).interpreter = interpreter
        elif isOrder == True:
            if self.isInSessionList(lang, name) == False:
                self.sessionList.append(CodeSession(lang, name))
            self.getSession(lang, name).orderLine = orderLine
            self.getSession(lang, name).isOrder = True
        elif lineNum != None:
            if self.isInSessionList(lang, name):
                self.getSession(lang, name).addCode(lineNum, code)
            else:
                self.sessionList.append(CodeSession(lang, name))
                self.getSession(lang, name).addCode(lineNum, code)


    def getRunSessionList(self):
        """
        Returns a list of run code sessions.
        """

        runSessionList = []

        for session in self.sessionList:
            if session.isRun == True:
                runSessionList.append(session)

        return runSessionList


    def getEvaluateSessionList(self):
        """
        Returns a list of run code sessions.
        """

        evaluateSessionList = []

        for session in self.sessionList:
            if session.isEvaluate == True:
                evaluateSessionList.append(session)

        return evaluateSessionList


    def getTofileSessionList(self):
        """
        Returns a list of specified tofile code sessions.
        """

        tofileSessionList = []

        for session in self.sessionList:
            if session.isTofile == True:
                tofileSessionList.append(session)

        return tofileSessionList


    def sortSession(self):
        orderSessionList = []
        nonorderSessionList = []
        for session in self.sessionList:
            if session.isOrder == True:
                orderSessionList.append(session)
            else:
                nonorderSessionList.append(session)
        orderSessionList.sort(key=lambda x: x.orderLine, reverse=False)
        nonorderSessionList.sort(key=lambda x: x.getFirstLine(), reverse=False)
        self.sessionList = orderSessionList + nonorderSessionList



class CodeSessionArrProcessor:
    """
    This class grouups different functions to process CodeSessionArr object.
    """

    def __init__(self, codeSessionArr, interpreterDict = {"python" : ["python"]}):
        self.codeSessionArr = codeSessionArr
        self.interpreterDict = interpreterDict


    # working lang and name handling.
    def runInterpreter(self, interpreter, argList, s, returnOutput = False, lang = None, name = None):
        """
        Run the interpreter as a subprocess.
        """

        FILE_KEYWORD = "FILE_NAME"
        currentSystem = platform.system()
        if currentSystem == "Linux":
            DIR = str(os.environ['HOME']) + "/.cache/krun/"
        else:
            DIR = ""

        if argList !=  None:
            if FILE_KEYWORD in argList:
                path = DIR + str(lang)
                fileName = path + "/" + str(name)
                if not os.path.exists(path):
                    os.makedirs(path)
                f = open(fileName, "w")
                f.write(s)
                f.close()
                copyArgList = [fileName if arg == FILE_KEYWORD else arg for arg in argList]
            else:
                copyArgList = copy.deepcopy(argList)
        else:
            copyArgList = copy.deepcopy(argList)

        if returnOutput == True:
            if copyArgList == None:
                command = [str(interpreter)]
            else:
                command = [str(interpreter)] + copyArgList
            if argList != None:
                if FILE_KEYWORD in argList:
                    p = subprocess.run(command, encoding='ISO-8859-1', stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
                else:
                    p = subprocess.run(command, encoding='ISO-8859-1', input=s, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            else:
                p = subprocess.run(command, encoding='ISO-8859-1', input=s, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
            return p.stdout
        else:
            if copyArgList == None:
                command = [str(interpreter)]
            else:
                command = [str(interpreter)] + copyArgList
            if FILE_KEYWORD in argList:
                p = subprocess.run(command, encoding='ISO-8859-1')
            else:
                p = subprocess.run(command, encoding='ISO-8859-1', input=s)

        if FILE_KEYWORD in argList:
            os.remove(fileName)

        return None


    def substituteKeywordInCodeSessionArr(self, captureKeyword, replaceText):
        """
        Substitute keyword for CodeSegment of CodeSession of CodeSessionArr.
        """

        runSessionList = self.codeSessionArr.getRunSessionList()
        for session in runSessionList:
            if session.captureKeyword != captureKeyword:
                for segment in session.codeSegmentList:
                    segment.code = segment.code.replace(captureKeyword, replaceText)


    def operateRunSession(self, sessionId = None):
        """
        Run run session/sessions.
        """

        runSessionList = self.codeSessionArr.getRunSessionList()

        if sessionId == None:
            for session in runSessionList:
                if session.interpreter["processor"] == None:
                    if str(session.lang) in self.interpreterDict:
                        if session.interpreter["arguments"] != None:
                            if session.isCapture == True:
                                output = self.runInterpreter(self.interpreterDict[str(session.lang)][0], session.interpreter["arguments"], session.getCodeAfterRunCommand(), returnOutput = True, lang = session.lang, name = session.name)
                                self.substituteKeywordInCodeSessionArr(captureKeyword = session.captureKeyword, replaceText = output)
                            else:
                                self.runInterpreter(self.interpreterDict[str(session.lang)][0], session.interpreter["arguments"], session.getCodeAfterRunCommand(), lang = session.lang, name = session.name)

                        else:
                            if session.isCapture == True:
                                output = self.runInterpreter(self.interpreterDict[str(session.lang)][0], self.interpreterDict[str(session.lang)][1:], session.getCodeAfterRunCommand(), returnOutput = True, lang = session.lang, name = session.name)
                                self.substituteKeywordInCodeSessionArr(captureKeyword = session.captureKeyword, replaceText = output)

                            else:
                                if session.isCapture == True:
                                    output = self.runInterpreter(self.interpreterDict[str(session.lang)][0], self.interpreterDict[str(session.lang)][1:], session.getCodeAfterRunCommand(), returnOutput = True, lang = session.lang, name = session.name)
                                    self.substituteKeywordInCodeSessionArr(captureKeyword = session.captureKeyword, replaceText = output)
                                else:
                                    self.runInterpreter(self.interpreterDict[str(session.lang)][0], self.interpreterDict[str(session.lang)][1:], session.getCodeAfterRunCommand(), lang = session.lang, name = session.name)

                    else:
                        sys.exit("krun doesn't run this language " + str(session.lang))

                elif session.isInterpreter == True:
                        if session.interpreter["arguments"] != None:
                            self.runInterpreter(session.interpreter["processor"], session.interpreter["arguments"], session.getCodeAfterRunCommand(), lang = session.lang, name = session.name)

                        else:
                            self.runInterpreter(session.interpreter["processor"], self.interpreterDict[str(session.lang)][1:], session.getCodeAfterRunCommand(), lang = session.lang, name = session.name)

        else:
            for session in runSessionList:
                if session.id == sessionId:
                    if session.isCapture == True:
                        output = self.runInterpreter(self.interpreterDict[str(session.lang)][0], self.interpreterDict[str(session.lang)][1:], session.getCodeAfterRunCommand(), returnOutput = True, lang = session.lang, name = session.name)
                        self.substituteKeywordInCodeSessionArr(captureKeyword = session.captureKeyword, replaceText = output)
                    else:
                        self.runInterpreter(self.interpreterDict[str(session.lang)][0], self.interpreterDict[str(session.lang)][1:], session.getCodeAfterRunCommand(), lang = session.lang, name = session.name)
                    return
            sys.exit("id does not found to execute. id was " + str(sessionId))


    def outputFileSession(self, sessionId = None):
        """
        Print to standard output session/sessions code.
        """

        output = ""

        if sessionId == None:
            for session in self.codeSessionArr.sessionList:
                output += session.getCode()
            print(output, end='')
            return
        else:
            for session in self.codeSessionArr.sessionList:
                if session.id == sessionId:
                    output += session.getCode()
                    print(output, end='')
                    return
            sys.exit("id does not found to output. id was " + str(sessionId))


    def writeFile(self, filename, s):
        """
        Write a string to file.
        """

        f = open(filename, "w")
        f.write(s)
        f.close()


    def writeFileTofileSession(self, sessionId = None):
        """
        Write to file the sessions/session that specified as tofile.
        """

        tofileSessionList = self.codeSessionArr.getTofileSessionList()

        if sessionId == None:
            for session in tofileSessionList:
                if session.directory == None:
                    if self.checkFileNameValid(session.name) == False:
                        sys.exit(str(session.name) + " as a file name is invalid. Session id was " + str(session.id))
                    self.writeFile(str(session.name), session.getCode())
                else:
                    if self.checkFileNameValid(session.directory) == False:
                        sys.exit(str(session.directory) + " as a file name is invalid. Session id was " + str(session.id))
                    self.writeFile(str(session.directory), session.getCode())
        else:
            for session in tofileSessionList:
                if session.id == sessionId:
                    if session.directory == None:
                        if self.checkFileNameValid(session.name) == False:
                            sys.exit(str(session.name) + " as a file name is invalid. Session id was "+ str(session.id))
                        self.writeFile(str(session.name), session.getCode())
                    else:
                        if self.checkFileNameValid(session.directory) == False:
                            sys.exit(str(session.directory) + " as a file name is invalid. Session id was " + str(session.id))
                        self.writeFile(str(session.directory), session.getCode())
                    return
            sys.exit("id does not found to write to file. id was " + str(sessionId))


    def isSessionLangValid(self):
        """
        Check if language of run code sessions are valid.
        """

        for session in self.codeSessionArr.sessionList:
            if session.isRun == True:
                if str(session.lang) not in self.interpreterDict:
                    sys.exit("Language " + str(session.lang) + " can't be executed.")


    def getLangStatistic(self):
        """
        Return statistic about the languages.
        """
        
        s = ""
        s += "--- # default-language\n"

        for name in self.interpreterDict:
            s += str(name) + ":\n"
            # s += ("    %-20s%s") % ("default-processor:", ("'" +  str(self.interpreterDict[name][0]) + "'\n"))
            s += ("    %-20s%s") % ("default-processor:", "{processor:" + "'" +  str(self.interpreterDict[name][0]) + "', arguments: " + str(self.interpreterDict[name][1:]) + "}\n")

        return s


    def formatDictToYaml(self, myDict):
        """
        Format dictionary data type to yaml format for printStatistic for statistic option.
        """

        s = "{"
        i = 0
        for key in myDict:
            i += 1
            if myDict[key] == None:
                s += key + ": 'default'"
            else:
                if isinstance(myDict[key], list):
                    s += key + ": " + str(myDict[key]) + ""
                else:
                    s += key + ": '" + str(myDict[key]) + "'"
            if i < len(myDict):
                s += ", "
        s += "}"
        return s
        s += "}"


    def getSessionStatistic(self, session):
        """
        Return statistic about the code sessions.
        """
        
        s = ""
        s += session.id + ":\n"
        s += ("    %-20s%s") % ("line count:", str(session.getCode().count('\n')))
        s += "\n"
        s += ("    %-20s%s") % ("segments:", "[")
        for i in range(len(session.codeSegmentList)):
            s += "[" + str(session.codeSegmentList[i].lineNum) + ", " + str(session.codeSegmentList[i].getEndLineNum()) + "]"
            if i + 1 < len(session.codeSegmentList):
                s += ","
        s += "]"
        s += "\n"
        if session.isRun:
            s += ("    %-20s%s") % ("run at:", str(session.runLine))
        else:
            s += ("    %-20s%s") % ("run at:", "none")
        s += "\n"
        if session.isEvaluate:
            s += ("    %-20s%s") % ("evaluate at:", str(session.evaluateLine))
        else:
            s += ("    %-20s%s") % ("evaluate at:", "none")
        s += "\n"
        if session.isTofile:
            if session.directory != None:
                s += ("    %-20s%s") % ("tofile name:", session.directory)
            else:
                if session.name != None:
                    s += ("    %-20s%s") % ("tofile name:", session.name)
                else:
                    s += ("    %-20s%s") % ("tofile name:", (str(session.lang) + "-" + str(session.name)))
        else:
            s += ("    %-20s%s") % ("tofile :", "none")
        s += "\n"
        if session.isOrder:
            s += ("    %-20s%s") % ("order at:", str(session.orderLine))
        else:
            s += ("    %-20s%s") % ("order at:", "none")
        s += "\n"
        if session.isCapture:
            s += ("    %-20s%s") % ("capture keyword:", "'" + str(session.captureKeyword[3:len(session.captureKeyword)-3]) + "'")
        else:
            s += ("    %-20s%s") % ("capture keyword:", "none")
        s += "\n"
        if session.isInterpreter:
            s += ("    %-20s%s") % ("custom-processor:", self.formatDictToYaml(session.interpreter))
        else:
            s += ("    %-20s%s") % ("custom-processor:", "none")
        s += "\n"

        return s


    def printStatistic(self, sessionId = None):
        """
        Print out to the standard output the statistical information of the session/sessions.
        """

        self.isSessionLangValid()
        if sessionId == None:
            print(self.getLangStatistic())
            print("--- # session")
            for session in self.codeSessionArr.sessionList:
                print(self.getSessionStatistic(session), end='')
        else:
            for session in self.codeSessionArr.sessionList:
                if sessionId == session.id:
                    print(self.getSessionStatistic(session), end='')
                    return
            sys.exit("id does not found to make statistic. id was " + str(sessionId))


    def checkFileNameValid(self, fileName):
        """
        Check if the file name is valid to use.
        """

        if str(fileName)[-1] == "/" or str(fileName)[-1] == "\\":
            return False

        return True


    def checkOverlapFile(self, sessionId = None):
        """
        Check if files exists in the directory.
        """

        tofileSessionList = self.codeSessionArr.getTofileSessionList()
        # scan for all sessions in the array
        print("--- # check file existence")
        if sessionId == None:
            for session in tofileSessionList:
                print(str(session.id) + ":")
                fileName = FileNameProcessor.makeFileName(session.lang, session.name, session.directory)
                if self.checkFileNameValid(fileName) == False:
                    sys.exit(fileName + " as a file name is invalid")
                if os.path.isfile("./" + fileName) == True:
                    print(("    %-20s%s") % ((fileName + ":"), "YES"))
                else:
                    print(("    %-20s%s") % ((fileName + ":"), "NO"))
        else:
            for session in tofileSessionList:
                if session.id == sessionId:
                    print(str(session.id) + ":")
                    fileName = FileNameProcessor.makeFileName(session.lang, session.name, session.directory)
                    if self.checkFileNameValid(fileName) == False:
                        sys.exit(fileName + " as a file name is invalid")
                    if os.path.isfile("./" + fileName) == True:
                        print(("    %-20s%s") % ((fileName + ":"), "YES"))
                    else:
                        print(("    %-20s%s") % ((fileName + ":"), "NO"))
                    return
            sys.exit("id does not found to check if file exists. id was " + str(sessionId))


    def checkPlatformInterpreter(self, interpreterDict):
        """
        Check if platform interpreter exists.
        """

        print("--- # check default-interpreter available")
        for lang in interpreterDict:
            s = str(lang) + ":\n"
            if PlatformProcessor.isExecutable(interpreterDict[lang][0]):
                print(("    %-20s%s") % (str(interpreterDict[lang][0]) + ":", "YES"))
            else:
                print(("    %-20s%s") % (str(interpreterDict[lang][0]) + ":", "NO"))


    def formatResultBlock(self, lang = None, name = None, s = None):
        """
        Formatting the source code block for EVALUATE command.
        """

        randomNum = random.randint(100,1000000)
        myPassword = "resultPassword123" + str(randomNum)
        result = ""
        result += ".RESULTS " + str(lang) + " " + str(name) + " " + str(myPassword) + "\n"
        result += s
        result += "\n.RESULTE " + str(myPassword) + "\n"
        return result


    def getEvaluateList(self, sessionId = None, lineList = []):
        """
        Return a complete list of evaluate lines.
        """

        evaluateOutputDict = {}
        evaluateSessionList = self.codeSessionArr.getEvaluateSessionList()

        if sessionId == None:
            for session in evaluateSessionList:
                if str(session.lang) in self.interpreterDict:
                    if session.interpreter["processor"] == None:
                        # if session.isInterpreter == False:
                        if session.isCapture == True:
                            if session.interpreter["arguments"] == None:
                                output = self.runInterpreter(self.interpreterDict[str(session.lang)][0], self.interpreterDict[str(session.lang)][1:], session.getCodeBeforeEvaluateCommand(), returnOutput = True, lang = session.lang, name = session.name)
                                session.output = output
                            else:
                                output = self.runInterpreter(self.interpreterDict[str(session.lang)][0], session.interpreter["arguments"], session.getCodeBeforeEvaluateCommand(), returnOutput = True, lang = session.lang, name = session.name)
                            self.substituteKeywordInCodeSessionArr(captureKeyword = session.captureKeyword, replaceText = output)
                        else:
                            if session.interpreter["arguments"] == None:
                                output = self.runInterpreter(self.interpreterDict[str(session.lang)][0], self.interpreterDict[str(session.lang)][1:], session.getCodeBeforeEvaluateCommand(), returnOutput = True, lang = session.lang, name = session.name)
                            else:
                                output = self.runInterpreter(self.interpreterDict[str(session.lang)][0], session.interpreter["arguments"], session.getCodeBeforeEvaluateCommand(), returnOutput = True, lang = session.lang, name = session.name)
                            evaluateOutputDict[session.evaluateLine] = self.formatResultBlock(session.lang, session.name, output)
                    else:
                        if session.isCapture == True:
                            output = self.runInterpreter(session.interpreter["processor"], session.interpreter["arguments"], session.getCodeBeforeEvaluateCommand(), returnOutput = True, lang = session.lang, name = session.name)
                            session.output = output
                            self.substituteKeywordInCodeSessionArr(captureKeyword = session.captureKeyword, replaceText = output)
                        else:
                            output = self.runInterpreter(session.interpreter["processor"], session.interpreter["arguments"], session.getCodeBeforeEvaluateCommand(), returnOutput = True, lang = session.lang, name = session.name)
                            evaluateOutputDict[session.evaluateLine] = self.formatResultBlock(session.lang, session.name, output)
                else:
                    sys.exit("krun doesn't evaluate this language " + str(session.lang))
        else:
            for session in evaluateSessionList:
                if session.id == sessionId:
                    if session.isCapture == True:
                        output = self.runInterpreter(self.interpreterDict[str(session.lang)][0], self.interpreterDict[str(session.lang)][1:], session.getCodeBeforeEvaluateCommand(), returnOutput = True, lang = session.lang, name = session.name)
                        self.substituteKeywordInCodeSessionArr(captureKeyword = session.captureKeyword, replaceText = output)
                        session.output = output
                    else:
                        output = self.runInterpreter(self.interpreterDict[str(session.lang)][0], self.interpreterDict[str(session.lang)][1:], session.getCodeBeforeEvaluateCommand(), returnOutput = True, lang = session.lang, name = session.name)
                        evaluateOutputDict[session.evaluateLine] = self.formatResultBlock(session.lang, session.name, output)
                    return evaluateOutputDict
            sys.exit("id does not found to evaluate. id was " + str(sessionId))

        return evaluateOutputDict


    def operateExecuteSession(self, commandlineId, isGetStdin):
        """
        Operate execute option
        """

        replaceText = ""

        if isGetStdin == True:
            for line in sys.stdin:
                replaceText += line
        else:
            replaceText = ""
        self.substituteKeywordInCodeSessionArr(captureKeyword = MetaprogramKeywordProcessor.getMetaprogramStdinKeyword(), replaceText = replaceText)
        self.operateRunSession(commandlineId)


    def substituteStdin(self, getStdinFlag):
        """
        Operate execute option
        """

        replaceText = ""

        if getStdinFlag == True:
            for line in sys.stdin:
                replaceText += line
        self.substituteKeywordInCodeSessionArr(captureKeyword = MetaprogramKeywordProcessor.getMetaprogramStdinKeyword(), replaceText = replaceText)


    def substituteLineList(self, lineList):
        """
        Perform substitution for lineList for metaprogramming.
        """

        evaluateSessionList = self.codeSessionArr.getEvaluateSessionList()

        i = 0
        for line in lineList:
            for session in evaluateSessionList:
                if session.isCapture == True and session.captureKeyword in line:
                    lineList[i] = line.replace(session.captureKeyword, str(session.output))
            i += 1

        return lineList



class KdocCodeProcessor():
    """
    This class processes the kdoc document.
    """

    def __init__(self, startMarker = "CODES", endMarker = "CODEE", tofileMarker = "TOFILE", runMarker = "RUN", evaluateMarker = "EVALUATE", interpreterMarker = "PROCESSOR", captureMarker = "CAPTURE", orderMarker = "ORDER", languageMarker = "LANGUAGE", markup = "."):
        self.markup = markup
        self.startMarker = startMarker
        self.endMarker = endMarker
        self.interpreterMarker = interpreterMarker
        self.tofileMarker = tofileMarker
        self.runMarker = runMarker
        self.evaluateMarker = evaluateMarker
        self.captureMarker = captureMarker
        self.orderMarker = orderMarker
        self.languageMarker = languageMarker


    def splitTroffLinetoToken(self, line):
        """
        Break the line into a list of token
        """

        return ([i for i in re.split(r"(\.|\")|[ |\n]", line) if i])


    def parseToken(self, tokenList):
        """
        Process the list of tokens further
        """

        parseList1 = []
        f1 = False
        i = 0

        if len(tokenList) > 2:
           if tokenList[0] == '.' and tokenList[1] == '\\' and tokenList[2] == '\"': 
               return ['.']
           
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
            if i > 1 and s == '.':
                parseList2[len(parseList2) - 1] += s
                f1 = True
                continue
            parseList2.append(s)
        parseList = parseList2

        return parseList


    def processStartCode(self, parseList):
        """
        Process the line that properly contains the startMarker.
        """

        inCodeFlag = True
        lang, name, password = None, None, None

        if len(parseList) > 2:
            if parseList[2] != '':
                if sessionIdProcessor.SEPARATOR in parseList[2]:
                    sys.exit("Character " + sessionIdProcessor.SEPARATOR + " can't be used for session language")
                lang = parseList[2]
            else:
                lang = None
            if len(parseList) > 3:
                if parseList[3] != '':
                    if sessionIdProcessor.SEPARATOR in parseList[3]:
                        sys.exit("Character " + sessionIdProcessor.SEPARATOR + " can't be used for session name.")
                    name = parseList[3]
                else: 
                    name = None
        if len(parseList) > 4:
            password = parseList[4]

        return (inCodeFlag, lang, name, password)


    def processEndCode(self, parseList):
        """
        Process the line that properly contains the endMarker.
        """

        password = None

        if len(parseList) > 2:
            password = parseList[2]

        return password


    def processRunCode(self, parseList):
        """
        Process the line that properly contains the runMarker.
        """

        isRun = True

        if len(parseList) > 2:
            if parseList[2] != '':
                lang = parseList[2]
            else:
                lang = None
            if len(parseList) > 3:
                if parseList[3] != '':
                    name = parseList[3]
                else:
                    name = None
            else:
                name = None
        else:
            lang = None
            name = None

        return (isRun, lang, name)


    def processEvaluateCode(self, parseList):
        """
        Process the line that properly contains the runMarker.
        """

        isEvaluate = True

        if len(parseList) > 2:
            if parseList[2] != '':
                lang = parseList[2]
            else:
                lang = None
            if len(parseList) > 3:
                if parseList[3] != '':
                    name = parseList[3]
                else:
                    name = None
            else:
                name = None
        else:
            lang = None
            name = None

        return (isEvaluate, lang, name)


    def processTofileCode(self, parseList):
        """
        Process the line that properly contains the tofileMarker.
        """

        isTofile = True
        lang = None
        name = None
        directory = None

        if len(parseList) > 2:
            if parseList[2] != "":
                lang = parseList[2]
            if len(parseList) > 3:
                if parseList[3] != '':
                    name = parseList[3]
                if len(parseList) > 4:
                    if parseList[4] != '':
                        directory = parseList[4]
            else:
                name = None
        else:
            lang = None
            name = None

        return (isTofile, lang, name, directory)


    def processInterpreterCode(self, parseList):
        """
        Process the line that properly contains the IntperterMarker.
        """

        isInterpreter = True
        lang = None
        name = None
        interpreter = {"processor" : None, "arguments" : None}

        if len(parseList) > 2:
            if parseList[2] != "":
                lang = parseList[2]
            if len(parseList) > 3:
                if parseList[3] != '':
                    name = parseList[3]
                if len(parseList) > 4:
                    if parseList[4] != '':
                        interpreter["processor"] = parseList[4]
                    if len(parseList) > 5:
                        interpreter["arguments"] = []
                        interpreter["arguments"].append(parseList[5])
                        for item in parseList[6:]:
                            interpreter["arguments"].append(item)
            else:
                name = None
        else:
            lang = None
            name = None

        return (isInterpreter, lang, name, interpreter)    


    def processCaptureMarker(self, parseList):
        """
        Process the line that properly contains the captureMarker.
        """

        isCapture = True
        lang = None
        name = None
        keyword = None

        if len(parseList) > 2:
            if parseList[2] != "":
                lang = parseList[2]
            if len(parseList) > 3:
                if parseList[3] != '':
                    name = parseList[3]
                if len(parseList) > 4:
                    if parseList[4] != '':
                        keyword = parseList[4]
            else:
                name = None
        else:
            lang = None
            name = None

        return (isCapture, lang, name, keyword)


    def processOrderCode(self, parseList):
        """
        Process the line that properly contains the orderMarker.
        """

        isOrder = True
        lang = None
        name = None

        if len(parseList) > 2:
            if parseList[2] != "":
                lang = parseList[2]
            if len(parseList) > 3:
                if parseList[3] != '':
                    name = parseList[3]
        return (isOrder, lang, name)


    def processLanguageCode(self, parseList, language):
        """
        Process the line that properly contains the languageMarker.
        """

        args = []

        if len(parseList) > 2:
            if parseList[2] != "":
                language[parseList[2]] = []
            for item in parseList[3:]:
                language[parseList[2]].append(item)
        return language


    def processCode(self, lineList, getLineListCopy = False):
        """
        Evaluate code and append to lineList
        """

        copyLineList = []
        codeSessionArr = CodeSessionArr()
        lineNum = 0
        inCodeFlag = False
        password = None
        lang = None
        name = None
        parseList = []
        directory = None
        language = {}

        for line in lineList:
            lineNum += 1
            if getLineListCopy == True:
                copyLineList.append(line)
            if line[0] == self.markup:
                tokenList = self.splitTroffLinetoToken(line)
                parseList = self.parseToken(tokenList)
                if parseList == None and inCodeFlag == False:
                    # sys.exit("Error: missing quote at line " + str(lineNum))
                    parseList = []
                if parseList == None:
                    parseList = []
            if len(parseList) > 1:
                # EVALUATE command
                if parseList[1] == self.evaluateMarker and inCodeFlag == False:
                    isEvaluate, lang, name = self.processEvaluateCode(parseList)
                    codeSessionArr.addCode(lang = lang, name = name, evaluateLine = lineNum)
                # CODES command
                elif parseList[1] == self.startMarker and inCodeFlag == False:
                    inCodeFlag, lang, name, password = self.processStartCode(parseList)
                    continue
                # CODEE command
                elif parseList[1] == self.endMarker and inCodeFlag == True:
                    endPassword = self.processEndCode(parseList)
                    if endPassword == password:
                        parseList = []
                        inCodeFlag = False
                        password = None
                        lang = None
                        name = None
                        continue
                    else:
                        codeSessionArr.addCode(lineNum = lineNum, lang = lang, name = name, code = line)
                        continue
                # RUN command
                elif parseList[1] == self.runMarker and inCodeFlag == False:
                    isRun, lang, name = self.processRunCode(parseList)
                    codeSessionArr.addCode(lang = lang, name = name, isRun = isRun, runLine = lineNum)
                # TOFILE command
                elif parseList[1] == self.tofileMarker and inCodeFlag == False:
                    isTofile, lang, name, directory = self.processTofileCode(parseList)
                    codeSessionArr.addCode(lang = lang, name = name, isTofile = isTofile, directory = directory)
                # PROCESSOR command
                elif parseList[1] == self.interpreterMarker and inCodeFlag == False:
                    isInterpreter, lang, name, interpreter = self.processInterpreterCode(parseList)
                    codeSessionArr.addCode(lang = lang, name = name, isInterpreter = isInterpreter, interpreter = interpreter)
                # CAPTURE command
                elif parseList[1] == self.captureMarker and inCodeFlag == False:
                    isCapture, lang, name, keyword = self.processTofileCode(parseList)
                    codeSessionArr.addCode(lang = lang, name = name, isCapture = isCapture, keyword = keyword)
                # ORDER command
                elif parseList[1] == self.orderMarker and inCodeFlag == False:
                    isOrder, lang, name = self.processOrderCode(parseList)
                    codeSessionArr.addCode(lang = lang, name = name, isOrder = isOrder, orderLine = lineNum)
                # LANGUAGE command
                elif parseList[1] == self.languageMarker and inCodeFlag == False:
                    language = self.processLanguageCode(parseList, language)
                # block inside CODES and CODEE
                elif inCodeFlag == True:
                    codeSessionArr.addCode(lineNum = lineNum, lang = lang, name = name, code = line)
                    continue
                parseList = []
            # block inside CODES and CODEE
            elif inCodeFlag == True:
                codeSessionArr.addCode(lineNum = lineNum, lang = lang, name = name, code = line)
                continue
        if getLineListCopy == True:
            return (codeSessionArr, copyLineList, language)
        else:
            return (codeSessionArr, language)
                    

class CommandlineProcessor:
    """
    This class groups functions that process commandline options.
    """
    
    # alias keywords for the same option. Not implement yet.
    HELP_OPTION_ALIAS 			= 	["-help", 		"-h", 	"?"	]
    ID_OPTION_ALIAS 			= 	["-id", 		"-i"		]
    TOFILE_OPTION_ALIAS 		= 	["-tofile", 		"-t"		]
    EVALUATE_OPTION_ALIAS 		= 	["-evaluate", 		"-e"		]
    RUN_OPTION_ALIAS	 		= 	["-run", 		"-r"		]
    OUTPUT_OPTION_ALIAS 		= 	["-output", 		"-o"		]
    STASTISTIC_OPTION_ALIAS 		= 	["-stat", 		"-s"		]
    CHECK_OPTION_ALIAS 			= 	["-check", 		"-c"		]
    EXECUTE_OPTION_ALIAS		=	["-execute",		"-x"		]
    EXECUTE_AND_STDIN_OPTION_ALIAS	=	["-executesdin",	"-xs"		]
    GET_STDIN_OPTION_ALIAS		=	["-getstdin",		"-g"		]


    def printHelpMsg():
        """
        Print out the help message for the program.
        """

        print(
"""
krun - a simple filter supporting literate programming for kdoc or any plain text file.

Usage: krun [option[arg]] [option[arg]] ...

Options:

    ?
    -h
    -help
        print this help message
    -o
    -output
        print all sessions codes
    -t
    -tofile
        write specified sessions to files
    -s
    -stat
        print out the statistic.
    -c
    -check
        check if file to be written exists in the directory.
    -r
    -run
        execute the specified code with RUN command.
    -e
    -evaluate
        evaluate code and combine with the stream as a preprocessor for Troff
    -xs <filename>
    -executestdin <filename>
        execute the document as a program and get stdin.
    -i
    -id <session_id>
        select the session has <session_id>
        may combine with other options

Example file:

    .PROCESSOR "" "" "python"
    .TOFILE python test.py MyTest.py
    .CODES python test.py pass123
    print("Hello World")
    .CODEE pass123
    .RUN python test.py
    .EVALUATE python test.py

Example:

    cat file.kdoc | krun -r
    cat file.kdoc | krun -e

About:

    Version: 0.3
    Author: Khang Bao
    Since: March 13, 2021
""", end='')

    def processOption(args):
        """
        Process the commandline options.
        """

        argc = len(args)
        commandlineId = None
        outputFlag = False
        tofileFlag = False
        statisticFlag = False
        checkFlag = False
        runFlag = False
        evaluateFlag = False
        executeFlag = False
        executeStdinFlag = False
        fileName = None
        getStdinFlag = False

        if argc > 1:
            if args[1] in CommandlineProcessor.HELP_OPTION_ALIAS:
                CommandlineProcessor.printHelpMsg()
                sys.exit()
            elif args[1] in CommandlineProcessor.TOFILE_OPTION_ALIAS:
                tofileFlag = True
            elif args[1] in CommandlineProcessor.OUTPUT_OPTION_ALIAS:
                outputFlag = True
            elif args[1] in CommandlineProcessor.EXECUTE_OPTION_ALIAS:
                if argc > 2:
                    executeFlag = True
                    fileName = args[2]
                else:
                    sys.exit("krun: missing filename after -execute option.")
            elif args[1] in CommandlineProcessor.EXECUTE_AND_STDIN_OPTION_ALIAS:
                if argc > 2:
                    executeStdinFlag = True
                    fileName = args[2]
                else:
                    sys.exit("krun: missing filename after -execute option.")
            elif args[1] in CommandlineProcessor.STASTISTIC_OPTION_ALIAS:
                statisticFlag = True
            elif args[1] in CommandlineProcessor.CHECK_OPTION_ALIAS:
                checkFlag = True
            elif args[1] in CommandlineProcessor.EVALUATE_OPTION_ALIAS:
                evaluateFlag = True
            elif args[1] in CommandlineProcessor.RUN_OPTION_ALIAS:
                runFlag = True
            elif args[1] in CommandlineProcessor.ID_OPTION_ALIAS:
                if argc > 2:
                    commandlineId = args[2]
                    if argc > 3:
                        if args[3] in CommandlineProcessor.OUTPUT_OPTION_ALIAS:
                            outputFlag = True
                        elif args[3] in CommandlineProcessor.TOFILE_OPTION_ALIAS:
                            tofileFlag = True
                        elif args[3] in CommandlineProcessor.STASTISTIC_OPTION_ALIAS:
                            statisticFlag = True
                        elif args[3] in CommandlineProcessor.CHECK_OPTION_ALIAS:
                            checkFlag = True
                        elif args[3] in CommandlineProcessor.EVALUATE_OPTION_ALIAS:
                            evaluateFlag = True
                        elif args[3] in CommandlineProcessor.RUN_OPTION_ALIAS:
                            runFlag = True
                        else:
                            sys.exit("Unappropriate option after id value.")
                else:
                    sys.exit("Missing value after -id.")
            # getstdin mode
            elif args[1] in CommandlineProcessor.GET_STDIN_OPTION_ALIAS:
                getStdinFlag = True
                if argc > 2:
                    fileName = args[2]
                    if argc > 3:
                        if args[3] in CommandlineProcessor.HELP_OPTION_ALIAS:
                            CommandlineProcessor.printHelpMsg()
                            sys.exit()
                        elif args[3] in CommandlineProcessor.TOFILE_OPTION_ALIAS:
                            tofileFlag = True
                        elif args[3] in CommandlineProcessor.OUTPUT_OPTION_ALIAS:
                            outputFlag = True
                        elif args[3] in CommandlineProcessor.EXECUTE_OPTION_ALIAS:
                            if argc > 4:
                                executeFlag = True
                                fileName = args[3]
                            else:
                                sys.exit("krun: missing filename after -execute option.")
                        elif args[1] in CommandlineProcessor.EXECUTE_AND_STDIN_OPTION_ALIAS:
                            if argc > 4:
                                executeStdinFlag = True
                                fileName = args[3]
                            else:
                                sys.exit("krun: missing filename after -execute option.")
                        elif args[3] in CommandlineProcessor.STASTISTIC_OPTION_ALIAS:
                            statisticFlag = True
                        elif args[3] in CommandlineProcessor.CHECK_OPTION_ALIAS:
                            checkFlag = True
                        elif args[3] in CommandlineProcessor.EVALUATE_OPTION_ALIAS:
                            evaluateFlag = True
                        elif args[3] in CommandlineProcessor.RUN_OPTION_ALIAS:
                            runFlag = True
                        elif args[3] in CommandlineProcessor.ID_OPTION_ALIAS:
                            if argc > 4:
                                commandlineId = args[4]
                                if argc > 5:
                                    if args[5] in CommandlineProcessor.OUTPUT_OPTION_ALIAS:
                                        outputFlag = True
                                    elif args[5] in CommandlineProcessor.TOFILE_OPTION_ALIAS:
                                        tofileFlag = True
                                    elif args[5] in CommandlineProcessor.STASTISTIC_OPTION_ALIAS:
                                        statisticFlag = True
                                    elif args[5] in CommandlineProcessor.CHECK_OPTION_ALIAS:
                                        checkFlag = True
                                    elif args[5] in CommandlineProcessor.EVALUATE_OPTION_ALIAS:
                                        evaluateFlag = True
                                    elif args[5] in CommandlineProcessor.RUN_OPTION_ALIAS:
                                        runFlag = True
                                    else:
                                        sys.exit("Unappropriate option after id value.")
                            else:
                                sys.exit("Missing value after -id.")
                else:
                    sys.exit("Missing argument. Try -h for usage.")
            # handling as a filename
            else:
                fileName = args[1]
                if argc > 2:
                    if args[2] in CommandlineProcessor.HELP_OPTION_ALIAS:
                        CommandlineProcessor.printHelpMsg()
                        sys.exit()
                    elif args[2] in CommandlineProcessor.TOFILE_OPTION_ALIAS:
                        tofileFlag = True
                    elif args[2] in CommandlineProcessor.OUTPUT_OPTION_ALIAS:
                        outputFlag = True
                    elif args[2] in CommandlineProcessor.EXECUTE_OPTION_ALIAS:
                        if argc > 3:
                            executeFlag = True
                            fileName = args[3]
                        else:
                            sys.exit("krun: missing filename after -execute option.")
                    elif args[1] in CommandlineProcessor.EXECUTE_AND_STDIN_OPTION_ALIAS:
                        if argc > 3:
                            executeStdinFlag = True
                            fileName = args[3]
                        else:
                            sys.exit("krun: missing filename after -execute option.")
                    elif args[2] in CommandlineProcessor.STASTISTIC_OPTION_ALIAS:
                        statisticFlag = True
                    elif args[2] in CommandlineProcessor.CHECK_OPTION_ALIAS:
                        checkFlag = True
                    elif args[2] in CommandlineProcessor.EVALUATE_OPTION_ALIAS:
                        evaluateFlag = True
                    elif args[2] in CommandlineProcessor.RUN_OPTION_ALIAS:
                        runFlag = True
                    elif args[2] in CommandlineProcessor.ID_OPTION_ALIAS:
                        if argc > 3:
                            commandlineId = args[3]
                            if argc > 4:
                                if args[4] in CommandlineProcessor.OUTPUT_OPTION_ALIAS:
                                    outputFlag = True
                                elif args[4] in CommandlineProcessor.TOFILE_OPTION_ALIAS:
                                    tofileFlag = True
                                elif args[4] in CommandlineProcessor.STASTISTIC_OPTION_ALIAS:
                                    statisticFlag = True
                                elif args[4] in CommandlineProcessor.CHECK_OPTION_ALIAS:
                                    checkFlag = True
                                elif args[4] in CommandlineProcessor.EVALUATE_OPTION_ALIAS:
                                    evaluateFlag = True
                                elif args[4] in CommandlineProcessor.RUN_OPTION_ALIAS:
                                    runFlag = True
                                else:
                                    sys.exit("Unappropriate option after id value.")
                        else:
                            sys.exit("Missing value after -id.")
        else:
            print("Try krun -h for usage.")
            sys.exit()

        return (commandlineId, statisticFlag, outputFlag, tofileFlag, checkFlag, runFlag, evaluateFlag, executeFlag, executeStdinFlag, fileName, getStdinFlag)



class MainDriver():
    """
    This class is the main driver for the program.
    """

    def updateInterpreterDict(interpreterDict, language):
        """
        Update language for interpreterDict.
        """

        copyInterpreterDict = copy.deepcopy(interpreterDict)
        for lang in language:
            copyInterpreterDict[lang] = language[lang]
        return copyInterpreterDict


    def runDriver():
        """
        Run the program.
        """

        # It's okay to change this to suit your need.
        # Make sure they are availabe on your computer when in use, otherwise comment it out or avoid using it.
        # PROCESSOR_DICT = {
        #    "<language name>" : ["<processor command>", [optional commandline arguments]],
        #    }
        PROCESSOR_DICT = {
            "None" 		: 	["python",			],
            "python" 		: 	["python",			],
            "ipython" 		: 	["ipython",			],
            "bash" 		: 	["bash",			],
            "zsh" 		: 	["zsh",				],
            "cmd" 		: 	["cmd",				],
            "awk" 		: 	["awk",				],
            "perl" 		: 	["perl",			],
            "R" 		: 	["R",				],
            "kdoc" 		:	["krun",	"-r"		],
            "C" 		:	["tcc",		"FILE_NAME",	],
            "java" 		:	["javac",	"FILE_NAME"	],
            "yacc" 		:	["yacc",	"FILE_NAME"	],
            "lex" 		:	["lex",		"FILE_NAME"	],
            }

        # process the commandline options
        commandlineId, statisticFlag, outputFlag, tofileFlag, checkFlag, runFlag, evaluateFlag, executeFlag, executeStdinFlag, fileName, getStdinFlag = CommandlineProcessor.processOption(sys.argv)

        kdocCodeProcessor = KdocCodeProcessor()

        # if option is -execute or its alias
        if 1 == 0:
            pass
        # if option is -executewithstdin or its alias
        elif executeFlag == True:
            f = open(fileName, "r")
            buffer = f.read()
            lineList = buffer.split("\n")
            f.close()
            i = 0
            for line in lineList:
                lineList[i] += "\n"
                i += 1
            codeSessionArr, language = kdocCodeProcessor.processCode(lineList)
            codeSessionArr.sortSession()
            updatedInterpreterDict = MainDriver.updateInterpreterDict(PROCESSOR_DICT, language)
            # codeSessionArrProcessor = CodeSessionArrProcessor(codeSessionArr, PROCESSOR_DICT)
            codeSessionArrProcessor = CodeSessionArrProcessor(codeSessionArr, updatedInterpreterDict)
            codeSessionArrProcessor.operateExecuteSession(commandlineId, False)
        # if option is -executewithstdin or its alias
        elif executeStdinFlag == True:
            f = open(fileName, "r")
            buffer = f.read()
            lineList = buffer.split("\n")
            f.close()
            i = 0
            for line in lineList:
                lineList[i] += "\n"
                i += 1
            codeSessionArr, language = kdocCodeProcessor.processCode(lineList)
            codeSessionArr.sortSession()
            updatedInterpreterDict = MainDriver.updateInterpreterDict(PROCESSOR_DICT, language)
            # codeSessionArrProcessor = CodeSessionArrProcessor(codeSessionArr, PROCESSOR_DICT)
            codeSessionArrProcessor = CodeSessionArrProcessor(codeSessionArr, updatedInterpreterDict)
            codeSessionArrProcessor.operateExecuteSession(commandlineId, True)
        # if option is -evaluate or its alias
        elif evaluateFlag == True:
            if fileName == None:
                codeSessionArr, lineList, language = kdocCodeProcessor.processCode(sys.stdin, getLineListCopy = True)
            else:
                f = open(fileName, "r")
                buffer = f.read()
                lineList = buffer.split("\n")
                f.close()
                i = 0
                for line in lineList:
                    lineList[i] += "\n"
                    i += 1
                codeSessionArr, language = kdocCodeProcessor.processCode(lineList)
            codeSessionArr.sortSession()
            updatedInterpreterDict = MainDriver.updateInterpreterDict(PROCESSOR_DICT, language)
            # codeSessionArrProcessor = CodeSessionArrProcessor(codeSessionArr, PROCESSOR_DICT)
            codeSessionArrProcessor = CodeSessionArrProcessor(codeSessionArr, updatedInterpreterDict)
            codeSessionArrProcessor.substituteStdin(getStdinFlag)
            evaluateOutputDict = codeSessionArrProcessor.getEvaluateList(commandlineId, lineList)
            lineNum = 0

            lineList = codeSessionArrProcessor.substituteLineList(lineList)
            # print the evaluated code (include original stream) to standard output
            lineListSize = len(lineList)
            for line in lineList:
                lineNum += 1
                print(line, end='')
                if evaluateOutputDict != None:
                    if lineNum in evaluateOutputDict:
                        print(evaluateOutputDict[lineNum], end='')
        else:
            if fileName == None:
                codeSessionArr, lineList, language = kdocCodeProcessor.processCode(sys.stdin, getLineListCopy = True)
            else:
                f = open(fileName, "r")
                buffer = f.read()
                lineList = buffer.split("\n")
                f.close()
                i = 0
                for line in lineList:
                    lineList[i] += "\n"
                    i += 1
                codeSessionArr, language = kdocCodeProcessor.processCode(lineList)
            # sorting the session
            codeSessionArr.sortSession()
            updatedInterpreterDict = MainDriver.updateInterpreterDict(PROCESSOR_DICT, language)
            # codeSessionArrProcessor = CodeSessionArrProcessor(codeSessionArr, PROCESSOR_DICT)
            codeSessionArrProcessor = CodeSessionArrProcessor(codeSessionArr, updatedInterpreterDict)
            codeSessionArrProcessor.substituteStdin(getStdinFlag)

            # execute the selected commandline option
            if outputFlag == True:
                codeSessionArrProcessor.outputFileSession(commandlineId)
            elif checkFlag == True:
                codeSessionArrProcessor.checkOverlapFile(commandlineId)
                # codeSessionArrProcessor.checkPlatformInterpreter(interpreterDict = PROCESSOR_DICT)
                codeSessionArrProcessor.checkPlatformInterpreter(interpreterDict = updatedInterpreterDict)
            elif statisticFlag == True:
                codeSessionArrProcessor.printStatistic(commandlineId)
            elif tofileFlag == True:
                codeSessionArrProcessor.writeFileTofileSession(commandlineId)
            elif runFlag == True:
                codeSessionArrProcessor.operateRunSession(commandlineId)
            else:
                sys.exit("No flag detected.");



if __name__ == "__main__":

    MainDriver.runDriver()
