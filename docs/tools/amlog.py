#!/usr/bin/python
## An application to parse IRC log files. The purpose is mainly to
## remember commit messages.
## Made by Arne Mejlholm (aaby@gentoo.org)
 
import time
import sys

version = '0.3.6.6'

class Output:
    """ class that handles all io """

    def formatCommit(self, string):
        """ method that handles formatting af a log string. """

        if string[0:14] == '--- Log opened':
            return [string[15:], "---", "---"]
        if string[0:15] == "--- Day changed": 
            return [string[16:], "---", "---"]

        time = string[0:5]

        charnr = -1
        startchar = -1
        endchar = -1
        lcount = 0
        rcount = 0
        for char in string:
            charnr = charnr + 1
            if char == '<' and charnr < 8 and lcount < 1:
                startchar = charnr
                lcount = lcount +1
            elif char == '>' and charnr < (len(string) - (len(string)/2)) and rcount < 1:
                endchar = charnr
                rcount = rcount +1
        name = string[startchar+1:endchar]
        newname = name
        if name[0] == '@':
            newname = 'Op ' + name[1:]
        if name[0] == '+':
            newname = name[1:]

        action = string[endchar+2:(len(string)-1)]
        newaction1 = action.replace('<', '-')
        newaction2 = newaction1.replace('>', '-')
        return [time, newname, newaction2]

    def writeHtmlFile(self, dataobject):
         """ a method that writes a html file passed as an object. """
         cf = ConfFile()
         outputhtmlfile = cf.parseConfFileString('DIR') + 'output.html'
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
         f('Log from channel: <b>' + str(dataobject.channelname) + '</b> parsed on: <b>' + str(dataobject.date) + '</b><br>\n')
         f('The duration of the log file was: <b>' + str(dataobject.duration[0]) +
                                     ' day(s) ' + str(dataobject.duration[1]) +
                                  ' hours and ' + str(dataobject.duration[2]) + ' minutes</b><br>\n')
         f('<b>The following '+ str(len(dataobject.listofnicks)) +' people have been active: </b><br>\n')
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
         f('<p align=center>\n')
         f('The most active day was: <b>' + dataobject.maxdate[0] + '</b> with: <b>' + str(dataobject.maxdate[1]) + '</b> commits.\n')
         f('</p>\n')
         f('<h2 align=center>Statistics</h2>\n')
         f('<h3 align=center>Chat</h3>\n')
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
         f('<td>' + str(dataobject.chatting[0]) + '</td>\n')
         f('<td>' + str(dataobject.chatting[1]) + '</td>\n')
         f('<td>' + str(dataobject.chatting[2]) + '</td>\n')
         f('<td>' + str(dataobject.chatting[3]) + '</td>\n')
         f('<td>' + str(dataobject.chatting[4]) + '</td>\n')
         f('</tr>\n\n')

         f('<tr>\n')
         f('<td>Percentile</td>\n')
         f('<td>' + str((100 * dataobject.chatting[0])/dataobject.chatting[5]) + '%</td>\n')
         f('<td>' + str((100 * dataobject.chatting[1])/dataobject.chatting[5]) + '%</td>\n')
         f('<td>' + str((100 * dataobject.chatting[2])/dataobject.chatting[5]) + '%</td>\n')
         f('<td>' + str((100 * dataobject.chatting[3])/dataobject.chatting[5]) + '%</td>\n')
         f('<td>' + str((100 * dataobject.chatting[4])/dataobject.chatting[5]) + '%</td>\n')
         f('</tr>\n\n')

         f('</table>\n')
         f('</p>\n')


         f('<h3 align=center>Commits</h3>\n')
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

         f('<tr>\n')
         f('<td>Percentile</td>\n')
         f('<td>' + str((100 * dataobject.usage[0])/commitlenght) + '%</td>\n')
         f('<td>' + str((100 * dataobject.usage[1])/commitlenght) + '%</td>\n')
         f('<td>' + str((100 * dataobject.usage[2])/commitlenght) + '%</td>\n')
         f('<td>' + str((100 * dataobject.usage[3])/commitlenght) + '%</td>\n')
         f('<td>' + str((100 * dataobject.usage[4])/commitlenght) + '%</td>\n')         
         f('</tr>\n\n')

         f('</table>\n')
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

         f('<hr>\n')
         f('<p align=center>Generated by AMLog version ' + version + '</p>')
         f('<p align=center>Future plans for amlog <a href="http://www.cs.auc.dk/~mejlholm/roadmap.txt">here</a>')
         f('</body>\n')
         f('</html>\n')
         file.close()

    def writeXMLFile(self, dataobject):
        """ a method that writes an xml file passed as an object. """        
        cf = ConfFile()
        outputxmlfile = cf.parseConfFileString('DIR') + 'output.xml'
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
        f('  This document shows stats from <b>' + dataobject.channelname + '</b>\n')
        f('</abstract>\n\n')
        f('<chapter>\n')        
        f('<title>Channel Summary</title>\n')
        f('<body>\n\n')
        f('<p>\n')
        f('  Log from channel: <b>' + dataobject.channelname + '</b> parsed on: <b>' + dataobject.date + '</b>\n')
        f('</p>\n\n')
        f('<p>\n')
        f('  The duration of the log file was: <b>' +  str(dataobject.duration[0]) +
                                    ' day(s) ' + str(dataobject.duration[1]) +
                                 ' hours and ' + str(dataobject.duration[2]) + ' minutes</b>\n')
        f('</p>\n\n')
        f('<p>\n')
        f('  <b>The following '+ str(len(dataobject.listofnicks)) +' people have been active:</b>\n')
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
        commitlength = dataobject.nrcommits
        f('  There has been a total of: <b>' + str(commitlength) + ' commits</b>.\n')
        f('</p>\n\n')

        f('<p>\n')

        f('The most active day was: <b>' + dataobject.maxdate[0] + '</b> with: <b>' + str(dataobject.maxdate[1]) + '</b> commits.\n')
        #f('The most active comitter was: <b>' + dataobject.maxcommits[0] + '</b> with: <b>'
         # + dataobject.maxcommits[1] + '</b> on the: <b>' + dataobject.maxcommits[2] + '</b>\n')
        f('</p>\n\n')
        f('</body>\n')        
        f('</chapter>\n\n')

        f('<chapter>\n')
        f('<title>Statistics</title>\n')
        f('<section>\n')
        f('<title>Chat</title>\n')
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
        f('  <ti>' + str(dataobject.chatting[0]) + '</ti>\n')
        f('  <ti>' + str(dataobject.chatting[1]) + '</ti>\n')
        f('  <ti>' + str(dataobject.chatting[2]) + '</ti>\n')
        f('  <ti>' + str(dataobject.chatting[3]) + '</ti>\n')
        f('  <ti>' + str(dataobject.chatting[4]) + '</ti>\n')
        f(' </tr>\n\n')
        f(' <tr>\n')

        f('  <ti>Percentile</ti>\n')
        f('  <ti>' + str((100 * dataobject.chatting[0])/dataobject.chatting[5]) + '%</ti>\n')
        f('  <ti>' + str((100 * dataobject.chatting[1])/dataobject.chatting[5]) + '%</ti>\n')
        f('  <ti>' + str((100 * dataobject.chatting[2])/dataobject.chatting[5]) + '%</ti>\n')
        f('  <ti>' + str((100 * dataobject.chatting[3])/dataobject.chatting[5]) + '%</ti>\n')
        f('  <ti>' + str((100 * dataobject.chatting[4])/dataobject.chatting[5]) + '%</ti>\n')

        f(' </tr>\n\n')

        f('</table>\n\n')
        f('</body>\n')        
        f('</section>\n\n')
   
        f('<section>\n')        
        f('<title>Commits</title>\n')
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
        f(' <tr>\n')

        f('  <ti>Percentile</ti>\n')
        f('  <ti>' + str((100 * dataobject.usage[0])/commitlength) + '%</ti>\n')
        f('  <ti>' + str((100 * dataobject.usage[1])/commitlength) + '%</ti>\n')
        f('  <ti>' + str((100 * dataobject.usage[2])/commitlength) + '%</ti>\n')
        f('  <ti>' + str((100 * dataobject.usage[3])/commitlength) + '%</ti>\n')
        f('  <ti>' + str((100 * dataobject.usage[4])/commitlength) + '%</ti>\n') 
        f(' </tr>\n\n')

        f('</table>\n\n')
        f('</body>\n')
        f('</section>\n')
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

        f('<p>\n')
        f('Future plans for amlog <uri link="http://www.cs.auc.dk/~mejlholm/roadmap.txt">here</uri>\n')
        f('</p>\n')
        
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

    def getMaxDate(commits): 
        activedate = [commits[0][18:-1], 0]
        maxdate = ["", 0]
        for string in commits:
            if string[0:15] == '--- Day changed':
                if maxdate[0] == '':
                    maxdate[0] = string[16:-1]
                activedate[0] = string[16:-1]
                activedate[1] = 0
            if string[6] == '<':
                activedate[1] = activedate[1] + 1
            if activedate[1] > maxdate[1]:
                maxdate[0] = activedate[0]
                maxdate[1] = activedate[1]
        if ':' in maxdate[0]:
            tmp = maxdate[0][1:8]
            tmp2 = maxdate[0][-4:]
            maxdate[0] = tmp + tmp2
        return maxdate

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
                if string[4:7] == 'Log':
                    commits.append(string)
                else:
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
            if string[6:9] == '-!-':
                continue
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

        newlist = []
        for nick in listofnicks:
            newnick = nick.lower()
            if newnick[0] == ' ':
                newnick = newnick[1:]
            newnick = newnick[0].upper() + newnick[1:]
            if newnick in newlist:
                pass
            else:
                newlist.append(newnick)
        newlist.sort()
        return newlist

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
        return [interval00_04, interval05_09, interval10_14, interval15_19, interval20_23, len(com)]

    def getChatting():

        lf = LogFile()
        log = lf.read()
        temp = []
        interval00_04 = 0
        interval05_09 = 0
        interval10_14 = 0
        interval15_19 = 0
        interval20_23 = 0
        for string in log:
            if string[2] == ':' and string[5] != '!':
                temp.append(int(string[0:2]))
        for number in temp:
            if number <= 4:
                interval00_04 = interval00_04 + 1
                continue
            elif number <= 9:
                interval05_09 = interval05_09 + 1
                continue
            elif number <= 14:
                interval10_14 = interval10_14 + 1
                continue
            elif number <= 19:
                interval15_19 = interval15_19 + 1
                continue
            elif number >= 20:
                interval20_23 = interval20_23 + 1
                continue
            else:
                print error
        return [interval00_04, interval05_09, interval10_14, interval15_19, interval20_23, len(temp)]

    backgroundcolor = 'white'
    title = getTitle()
    channelname = getChannelName()
    date = getDate()
    commits = getCommits()
    nrcommits = getNrCommits()
    listofnicks = getActiveNicks()
    duration = getDurationTime()
    usage = getUsage(commits)
    chatting = getChatting()
    maxdate = getMaxDate(commits)
    maxcommits = ["Aaby", "25", "2nd feb 2004"] #getMaxCommits(commits)

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
