#!/usr/bin/python
"""Python module that sends TCP requests to AWS instance."""

import socket
import time
import sys
import getopt
#WARNING DNS change at reboot 
host = ''
port = 5001
insertreqType = 'INSERT'
selectreqType = 'SELECT'

inputFile = ''
count = 0
# TO DO ...
# Add either "INSERT" OR "SELECT" strings to the data being sent

# type = 'INSERT'

def usage():
	print "-i input file|-s number -p proxyIP"
	exit(0)

def handling(argv):
    global host
    global inputFile
    global count
    global port
    reqType = ''
    try:
        opts, args = getopt.getopt(argv,"hi:s:p:",["ifile=","selectCount=","ip="])
    except getopt.GetoptError as e:
        usage()
    for opt, arg in opts:
        if opt == '-h':
            usage()
        elif opt in ("-i", "--ifile"):
            reqType = insertreqType
            inputFile = arg
        elif opt in ("-p", "--ip"):
            host = arg
        elif opt in ("-s", "--selectCount"):
            reqType = selectreqType
            count = int(arg)
    return reqType

def doInsert(reqType):
    global host
    global inputFile
    global port
    s = socket.socket()
    s.connect((host, port))

    with open(inputFile, 'r') as f:
        lines = f.readlines()
        for line in lines[1:]:
            clean_line = line.rstrip()
        	#We need to remove $ as it cause issues 
        	#with mysql cluster
            clean_line = clean_line.replace("$","")
            data = reqType + ',' + str(clean_line)
            print 'Sending data: ' + str(data)
            s.send(data)
            result = s.recv(2048)
            print 'output:' + result
            time.sleep(0.1)
    s.close()

def doSelect(reqType):
    global host
    global count
    global port
    s = socket.socket()
    s.connect((host, port))

    for i in range(count):
        data = reqType
        print 'Sending data: ' + str(data)
        s.send(data)
        print 'after send'
        result = s.recv(2048)
        print 'output:' + result
        time.sleep(0.1)
    s.close()


def main(argv):
    """Main."""

    reqType = handling(argv)

    if reqType == selectreqType:
    	doSelect(reqType)
    elif reqType == insertreqType:
    	doInsert(reqType)



if __name__ == '__main__':
   main(sys.argv[1:])
