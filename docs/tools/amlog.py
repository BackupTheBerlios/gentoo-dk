#!/usr/bin/python
## An application to parse IRC log files. The purpose is mainly to
## remember commit messages.
## Made by Arne Mejlholm (aaby@gentoo.org)

import time
import sys

version = '0.3.5'

class Output:
    """ class that handles all io """

    def formatCommit(self, string):
        """ method that handles formatting af a log string. """

        if string[0:14] == '--- Log opened':
            return [string[15:], "---", "---"]
        if string[0:15] == "--- Day changed": #--- Day changed Thu Jan 15 2004
            return [string[16:], "---", "---"]

        time = string[0:5]

        charnr = -1
        startchar = -1
        endchar = -1
        for char in string:
            charnr = charnr + 1
            if char == '<':
                startchar = charnr
            elif char == '>':
                endchar = charnr
        name = string[startchar+1:endchar]
        newname = name
        if name[0] == '@':
            newname = 'Op ' + name[1:]
        if name[0] == '+':
            newname = name[1:]

        action = string[endchar+2:(len(string)-1)]

        return [time, newname, action]

    def writeHtmlFile(self, dataobject):
         """ a method that writes a html file passed as an object. """
         cf = ConfFile()
         outputhtmlfile = cf.parseConfFileString('DIR') + '/output.html'
         file = open(outputhtmlfile, 'w')
         f = file.write
         f('<html>\n')
         f('<meta http-equiv="Content-Type" content="text/html; charset=iso-8859-1">\n')
         f('<head><title>\n')
         f(dataobject.title + '... Generated by AMLog version ' + version + '\n')
         f('</title></head>\n')
         f('<body bgcolor=' + dataobject.backgroundcolor + '>\n')
         f('<h1 align=center>' + dataobject.title + '</h1>\n')
         f('<h2 align=center>Channel summary</h2>\n')
         f('<p align=center>\n')
         f('Log from channel: ' + str(dataobject.channelname) + ' parsed on: ' + str(dataobject.date) + '<br>\n')
         f('The duration of the log file was: ' + str(dataobject.duration[0]) +
                                     ' day(s) ' + str(dataobject.duration[1]) +
                                  ' hours and ' + str(dataobject.duration[2]) + ' minutes<br>\n')
         f('The following people have been active: <br>\n')
         i = -1
         length = len(dataobject.listofnicks) -1
         for nick in dataobject.listofnicks:
            i = i + 1
            if i == 0:
                f(nick)
            elif i == length:
                f(' and ' +nick + '<br>\n')
            elif i % 7 == 0:
                f(', ' +nick + ',<br>\n')
            elif ((i % 7 == 1) and (i != 1)):
                f(nick)
            else:
                f(', ' + nick)
         commitlenght = dataobject.nrcommits
         f('The has been a total of: <b>' + str(commitlenght) + ' commits.</b>\n')
         f('</p>\n')

         f('<h2 align=center>Commit details </h2>\n')
         f('<p align=center>\n')
         f('<table border=1>\n')
         f('<tr><td><b>Nick</b></td><td><b>Time</b></td><td><b>Action</b></td></tr>\n')
         for line in dataobject.commits:
                 list = self.formatCommit(line)
                 f('<tr><td>' + list[1] +'</td><td>' + list[0] + '</td><td>' + list[2] + '</td></tr>\n')

         f('</table>\n')
         f('</p>\n')

         f('<h2 align=center>Commit statistics</h2>\n')
         f('<p align=center>\n')
         f('<table border=1>\n')

         f('<tr>\n')
         f('<td>Period</td>\n')
         f('<td>00-04</td>\n')
         f('<td>05-09</td>\n')
         f('<td>10-14</td>\n')
         f('<td>15-19</td>\n')
         f('<td>20-23</td>\n')
         f('</tr>\n\n')

         f('<tr>\n')
         f('<td>Number</td>\n')
         f('<td>' + str(dataobject.usage[0]) + '</td>\n')
         f('<td>' + str(dataobject.usage[1]) + '</td>\n')
         f('<td>' + str(dataobject.usage[2]) + '</td>\n')
         f('<td>' + str(dataobject.usage[3]) + '</td>\n')
         f('<td>' + str(dataobject.usage[4]) + '</td>\n')
         f('</tr>\n\n')

         f('</table>\n')
         f('</p>\n')

         f('<hr>\n')
         f('<p align=center>Generated by AMLog version ' + version + '</p>')
         f('</body>\n')
         f('</html>\n')
         file.close()

    def writeXMLFile(self, dataobject):
        """ a method that writes an xml file passed as an object. """        
        cf = ConfFile()
        outputxmlfile = cf.parseConfFileString('DIR') + '/output.xml'
        file = open(outputxmlfile, 'w')
        f = file.write

        f('<?xml version="1.0" encoding="'+cf.parseConfFileString('ENCODING')+'"?>\n')
        f('<?xml-stylesheet href="' + cf.parseConfFileString('XSLPATH') + '" type="text/xsl"?>\n')
        f('<!DOCTYPE guide SYSTEM "'+ cf.parseConfFileString('DTDPATH') +'">\n')
        f('<guide>\n')
        f('<title>' + dataobject.title + '</title>\n\n')
        f('<author title="Author">\n')
        f('  <mail link="aaby@gentoo.org">AMLog v.' + version + '</mail>\n')
        f('</author>\n\n')
        f('<version>1.0</version>\n')
        f('<date>' + dataobject.date + '</date>\n\n')
        f('<abstract>\n')
        f('  This document shows stats from ' + dataobject.channelname + '\n')
        f('</abstract>\n\n')
        f('<chapter>\n')        
        f('<title>Channel Summary</title>\n')
        f('<body>\n\n')
        f('<p>\n')
        f('  Log from channel: ' + dataobject.channelname + ' parsed on:' + dataobject.date + '\n')
        f('</p>\n\n')
        f('<p>\n')
        f('  The duration of the log file was: ' +  str(dataobject.duration[0]) +
                                    ' day(s) ' + str(dataobject.duration[1]) +
                                 ' hours and ' + str(dataobject.duration[2]) + ' minutes\n')
        f('</p>\n\n')
        f('<p>\n')
        f('  The following people have been active:\n')
        f('</p>\n')
        i = -1
        length = len(dataobject.listofnicks) - 1
        f('<p>\n')
        f('  ')
        for nick in dataobject.listofnicks:
            i = i + 1
            if i == 0:
                f(nick)
            elif i == length:
                f(' and ' +nick + '\n')
            elif i % 7 == 0:
                f(', ' +nick + ',\n</p>\n\n<p>\n')
            elif ((i % 7 == 1) and (i != 1)):
                f(nick)
            else:
                f(', ' + nick)
        f('</p>\n\n')
        f('<p>\n')
        commitlenght = dataobject.nrcommits
        f('  There has been a total of: <b>' + str(commitlenght) + ' commits</b>.\n')
        f('</p>\n\n')
        f('</body>\n')        
        f('</chapter>\n\n')
        f('<chapter>\n')        
        f('<title>Commit details</title>\n')
        f('<body>\n\n')
        
        f('<table>\n')

        f(' <tr>\n')
        f('  <th>Nick</th>\n')
        f('  <th>Time</th>\n')
        f('  <th>Action</th>\n')
        f(' </tr>\n\n')
        for line in dataobject.commits:
            list = self.formatCommit(line)
            f(' <tr>\n  <ti>' + list[1] +'</ti>\n  <ti>' + list[0] + '</ti>\n  <ti>' + list[2] + '</ti>\n </tr>\n')

        f('</table>\n\n')

        f('</body>\n')        
        f('</chapter>\n\n')

        f('<chapter>\n')        
        f('<title>Commit statistics</title>\n')
        f('<body>\n\n')

        f('<table>\n')

        f(' <tr>\n')
        f('  <th>Period</th>\n')
        f('  <th>00-04</th>\n')
        f('  <th>05-09</th>\n')
        f('  <th>10-14</th>\n')
        f('  <th>15-19</th>\n')
        f('  <th>20-23</th>\n')
        f(' </tr>\n\n')

        f(' <tr>\n')
        f('  <ti>Number</ti>\n')
        f('  <ti>' + str(dataobject.usage[0]) + '</ti>\n')
        f('  <ti>' + str(dataobject.usage[1]) + '</ti>\n')
        f('  <ti>' + str(dataobject.usage[2]) + '</ti>\n')
        f('  <ti>' + str(dataobject.usage[3]) + '</ti>\n')
        f('  <ti>' + str(dataobject.usage[4]) + '</ti>\n')
        f(' </tr>\n\n')
        f('</table>\n\n')

        ### bottom
        f('</body>\n')        
        f('</chapter>\n')        
        f('</guide>\n')
        file.close()
        
class ConfFile:
    """ class that handles the configuration file"""

    conffile = '/usr/amfusk/amlog.conf'

    def readConfFile(self):
        """ a method that reads a config file """
        confs = []
        file = open(self.conffile, 'r')
        for line in file.readlines():
            for char in line:
                if char == '#':
                    break
                elif char == '\n':
                    break
                else:
                    confs.append(line)
                    break

        file.close()
        return confs

    def parseConfFileString(self, string):
        """ a method that searches throgh a log file. It recieves a string representing
        what to look for and returns what is after the equals sign. """
        returner = 'default'
        list = self.readConfFile()
        for line in list:
            variable = line[0:len(string)]
            if variable == string: 
                returner = line[(len(string)+1):(len(line)-1)]
                break
            else:
                returner = 'failure'
        return returner

class LogFile:
    """ class that handles reading the log file """

    cf = ConfFile()
    logfile = str(cf.parseConfFileString('DIR'))+'/' + str(cf.parseConfFileString('LOGFILE'))

    def read(self):
        """ a method that reads the log file to be parsed. Returns a list
        of lines in the logfile. """
        log = []
        file = open(self.logfile, 'r')
        for line in file.readlines():
            log.append(line)
        file.close()
        return log
    
class DataFile:
    """ the main class that is manipulated with.
        Holds all the information that the html file should contain at the end """

    def getChannelName():
        lf = LogFile()
        list = lf.read()
        charnr = 0
        for line in list:
            for char in line:
                if line[charnr:charnr+10] == 'has joined':
                    return line[charnr+11:(len(line)-1)]
                else:
                    charnr = charnr +1

    def getDate():
        """ a method that makes a pretty data and time output """
        gmt = time.gmtime(time.time())
        fmt = '%a, %d %b %Y %H:%M:%S GMT'
        str = time.strftime(fmt, gmt)
        return str
    def getCommits():
        lf = LogFile()
        cf = ConfFile()
        commitstring = cf.parseConfFileString('COMMIT_STRING')
        commits = []
        log = lf.read()
        for string in log:
            charnr = 0
            if string[0:3] == "---":
                commits.append(string)
            for char in string:
                if str(string[charnr:charnr+14]) == commitstring:
                    commits.append(string)
                    charnr = charnr +1
                else:
                    charnr = charnr +1
        return commits

    def getNrCommits(): 
        lf = LogFile()
        cf = ConfFile()
        commitstring = cf.parseConfFileString('COMMIT_STRING')
        commits = []
        log = lf.read()
        for string in log:
            charnr = 0
            for char in string:
                if str(string[charnr:charnr+14]) == commitstring:
                    commits.append(string)
                    charnr = charnr +1
                else:
                    charnr = charnr +1
        nr = len(commits)
        return nr

    def getTitle():
        cf = ConfFile()
        title = cf.parseConfFileString('TITLE')
        return title

    def getActiveNicks():
        lf = LogFile()
        log = lf.read()
        listofnicks = []
        for string in log:
            charnr = -1
            startchar = -1
            endchar = -1
            for char in string:
                charnr = charnr + 1
                if char == '<':
                    startchar = charnr
                    continue
                elif char == '>':
                    endchar = charnr
                    break
            if '<' in string:
                name = string[startchar+1:endchar]
                newname = name
                if name[0] == '@':
                    newname = name[1:]
                if name[0] == '+':
                    newname = name[1:]
                if newname in listofnicks:
                    continue
                else:
                    listofnicks.append(newname)

        return listofnicks

    def getDurationTime():
        day = 0
        lf = LogFile()
        log = lf.read()
        for string in log:
            if string[0:3] == '---':
                if string[4:14] == 'Log opened':
                    starthr = string[26:28]
                    startmi = string[29:31]
                if string[4:15] == 'Day changed':
                    day = day + 1
            else:
                if string[2] == ':':
                    endhr = string[0:2]
                    endmi = string[3:5]
        hours = int(endhr) - int(starthr)
        min = int(endmi) - int(startmi)
        if min < 0:
            hours = hours - 1
            min = 60 +  min
        if hours < 0:
            day = day - 1
            hours = hours + 24
        duration = [day, hours, min]
        return duration

    def getUsage(com):

        use = []
        interval00_04 = 0
        interval05_09 = 0
        interval10_14 = 0
        interval15_19 = 0
        interval20_23 = 0
        for string in com:
            if string[0:3] == '---':
                continue
            else:
                use.append(int(string[0:2]))
        for ints in use:
            if ints <= 4:
                interval00_04 = interval00_04 + 1
                continue
            elif ints <= 9:
                interval05_09 = interval05_09 + 1
                continue
            elif ints <= 14:
                interval10_14 = interval10_14 + 1
                continue
            elif ints <= 19:
                interval15_19 = interval15_19 + 1
                continue
            elif ints >= 20:
                interval20_23 = interval20_23 + 1
                continue
            else:
                print error
        return [interval00_04, interval05_09, interval10_14, interval15_19, interval20_23]
        
    backgroundcolor = 'white'
    title = getTitle()
    channelname = getChannelName()
    date = getDate()
    commits = getCommits()
    nrcommits = getNrCommits()
    listofnicks = getActiveNicks()
    duration = getDurationTime()
    usage = getUsage(commits)

def __main__():
    op = Output()
    data = DataFile()
    arguments = sys.argv
    if len(arguments) == 1:
        print 'Writing output XML file...'
        op.writeXMLFile(data)
        print '\tDone...'
    elif len(arguments) > 2:
        print 'Too many commandline arguments'
        exit
    elif arguments[1] == 'html':
        print 'Writing output HTML file...'
        op.writeHtmlFile(data)
        print '\tDone...'
    elif arguments[1] == 'xml':
        print 'Writing output XML file...'
        op.writeXMLFile(data)
        print '\tDone...'
    else:
        print 'No recognized commandline arguments'
    print 'Thank you for using AMLog'
    
__main__()
