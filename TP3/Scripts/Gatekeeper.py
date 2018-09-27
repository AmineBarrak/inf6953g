#!/usr/bin/python

import socket
import string

#TO DO change to the ip of the proxy
proxy = '172.31.39.71'

host = ''
port = 5001

def error(msg):
    print msg
    exit(0)

#Check if the request type is correct and if the number of fields is normal
def validate_input(input):
    fields = input.split(',')
    if str(fields[0]) == 'INSERT':
        if len(fields) != 12:
            error('incorrect number of fields')
    elif str(fields[0]) == 'SELECT':
        if len(fields) != 1:
            error('incorrect number of fields')
    else:
        error('incorect request type')


def main():
    """Main."""
    s = socket.socket()
    s.bind((host, port))

    s.listen(1)  # Listen to one connection
    c, addr = s.accept()
    print 'connection from: ' + str(addr)


    proxyS = socket.socket()
    proxyS.connect((proxy, port))

    while True:
        data = c.recv(2048)  # Max bytes
        if not data:
            break
        print 'from connected user: ' + str(data)
        validate_input(str(data))
        proxyS.send(data)
        output = proxyS.recv(2048)
        c.send(output)
        
    c.close()
    proxyS.close()

if __name__ == '__main__':
    main()