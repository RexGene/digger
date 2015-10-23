#!/usr//bin/python

import re
import httplib
import sys

def dig(url, deep) :
    if deep >= 10:
        return

    global record 
    global logFile
    global regex

    index = url.find("/")
    if index != -1 :
      conn = httplib.HTTPConnection(url[:index])
      conn.request("GET", url[index:]) 
    else :
      conn = httplib.HTTPConnection(url)
      conn.request("GET", "") 
    
    respone = conn.getresponse()
    data = respone.read()
    conn.close()

    result = regex.findall(data)
    for suburl in result:
        feild = suburl.split("?")
        if record.get(feild[0]) == None:
            record[feild[0]] = 1
            if len(feild) > 1:
              logFile.write(suburl + "\n")
              logFile.flush()

            try:
              dig(suburl, deep + 1)
            except:
              print suburl + " can not connect" 

def main():
    global record 
    global logFile
    global regex


    record = {}

    if len(sys.argv) != 2:
        print sys.argv[0] + " <url>"
        return

    url = sys.argv[1]

    fields = url.split(".")
        
    logFile = open("log", "w")
    fieldsLen = len(fields)
    if fieldsLen < 2:
        print "domain len invalid"
        return

    regex = re.compile("href=\"http://(\w+?\." + fields[fieldsLen - 2] + "\." + fields[fieldsLen - 1]  + ".*?)\"")
    dig(url, 0)
    logFile.close()
    
main()
