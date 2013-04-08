"""
The top level Python file which Reads the quora URL and posts the top level 
answer
"""
import urllib
import urllib2
import sys
import re
from bs4 import BeautifulSoup, NavigableString
from sys import argv

#This requires Beautiful soup library installed.

def readQuoraURL(url):
    """
    Reads the quora URL and returns the soup object
    """
    response = urllib2.urlopen(url)
    page = response.read()
    soup = BeautifulSoup(page)    
    return soup

def readSoupFromFile(file_name):
    """
    Debug function for testing quora parsing. 
    Used so that Quora does not throw too many request
    """
    file = open(file_name)
    txt = file.read()
    soup = BeautifulSoup(txt)    
    return soup

def findQuestion(soup):
    """
    Gets the question text
    """
    return soup.title.contents[0]


def findTopAnswer(soup):
    """
    Gets the top level answer
    """
    firsttag = soup.find_all(id=re.compile("answer_content$"))[0]
    answerchild = firsttag.contents[1]
    return answerchild.contents[0].contents[0]

def textifytag(tag):
    """
    Returns tag lists of the answer content, the answer can contain
    HTMl tags
    """
    length =  len(tag.contents)
    textlist =  tag.contents[:length-2]
    return textlist

def formatstring(tag):
    #Total hack, need to re-write
    # does not handle a href in answers
    length =  len(tag.contents)
    if length > 1:
        string = ""
        if tag.name == "b":
            string = " **"
        if tag.name == "i":
            string = " *"
        for content in tag.contents:
            if isinstance(content, NavigableString) :
                string += content.string
            else:
                string += formatstring(content)
        if tag.name == "b":
            return string + " **"
        if tag.name == "i":
            return string + " *"

    if tag.name == 'br':
        return "\n"
    if tag.name == "b":
        if tag.string != None:
            return " **" + tag.string + "** "
        else:
            return " **"
    if tag.name == "i":
        if tag.string != None:
            return " *" + tag.string + "* "
        else:
            return " *"
    if tag.name == "wbr":
        if tag.string != None:
            return tag.string
        else:
            return ""
    
    if tag.name == "a":
        return tag.string

def markdownify(textlist):
    
    string = ""    
    for tag in textlist:
        if hasattr(tag, 'name'):
            text = formatstring(tag)
        else:
            text = tag.string
        if text != None :
            string += text
    print string,


if __name__ == "__main__":
    script, url = argv
    reload(sys)
    sys.setdefaultencoding("utf-8")
    soup = readQuoraURL(url)
    #soup = readSoupFromFile()
    question = findQuestion(soup)
    print "Question asked is :  " + question
    print ""
    tag = findTopAnswer(soup)
    textlist = textifytag(tag)
    markdownify(textlist)