#!/usr/bin/python
"""Python module that receives TCP requests."""
""" Warning THIS SCRIPT ASSUMES mysql-client is installed on the instance running the proxy"""
# to create user/permission : https://www.digitalocean.com/community/tutorials/how-to-create-a-new-user-and-grant-permissions-in-mysql
#don't forget to allow connexion from remote host, to open port from amazon security group (create/grant)
#The proxy must be allowed to connect on all nodes!!! (except gatekeeper and trusted host)
#IN case of connexion error:
#http://www.tecmint.com/fix-error-2003-hy000-cant-connect-to-mysql-server-on-127-0-0-1-111/
# https://www.tutorialspoint.com/mysql/mysql-create-database.htm
#NOTE private ip adr seem unaffected by reboot


#TO DO use threads to deal with several connexions

import socket
import string
import subprocess
import random

host = ''
port = 5001

#TO CHANGE : one must change the adresses of the master and
#slave nodes to match the current installation
masterAdr = '172.31.40.125'
slavesAdr = ['127.0.0.1', '127.0.0.1', '127.0.0.1']

#Mysql use the port 3306 by default
sqlPrt = '3306'

#TO CHANGE : please configure the username and pass of the user
#beware that this user must be remotly accessible
#must be the same on all nodes
username = 'test'
password = 'pass'
database = "tp3"


"""Assume we are working with a table such as data.csv"""
"""the database must be named tp3 and the table must be transactions as required by the lab"""
def buildInsert(memberID, date, country, gender, ip_address, amount, vip, product_id, card_type, serial, zone):
    sqlRequest = "INSERT INTO transactions (member_id, date, country, gender, ip_address, amount, vip, product_id, card_type, serial, zone) VALUES "
    values = "(\"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\", \"%s\")" % (memberID, date, country, gender, ip_address, amount, vip, product_id, card_type, serial, zone)
    return sqlRequest + str(values)

#TO DO
#This request was approuved by the lab instructor
def buildSelect():
    sqlRequest = "SELECT * FROM  transactions"
    return sqlRequest

#Build the command to run mysql process. a mysql client must be present on
#the machine (sudo apt-get mysql-client)
#TO DO use a python library to perform the connection
def buildCommand(username, ip_address, sqlRequest, password):
    #WARNING the "'" are important as they prevent the shell from interpreting """ and "$"
    command = "mysql -u %s -p%s -h %s -e\'%s\' %s" % (username, password, ip_address, sqlRequest, database)
    return command

def launchCommand(command):
    res = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    return res

def hitmaster(slqCommand):
    cmd = buildCommand(username, masterAdr, slqCommand, password)
    return launchCommand(cmd)

#use this function to apply the direct hit pattern
def directHit(slqCommand):
    return hitmaster(slqCommand)

#use this function to apply the random hit pattern
def randomHit(slqCommand):
    node_index = random.randint(0,len(slavesAdr) - 1)
    cmd = buildCommand(username, slavesAdr[node_index], slqCommand, password)
    return launchCommand(cmd)


def evaluateRTT(IPadr):
    number = 1
    #we ping the adr
    command = "ping -c %i %s" % (number, IPadr)
    output = subprocess.check_output(command, stderr=subprocess.STDOUT, shell=True)
    lines = output.split("\n")
    #the last output is actually a blank line
    #so we are interested in the one before
    res = lines[-2]
     # assuse the format is : rtt min/avg/max/mdev = 130.582/197.893/259.241/52.693 ms
    minAvgMax = res.split("=")[-1].split("/")

    return minAvgMax[1]

#use this function to apply the customized hit pattern
def customHit(slqCommand):
    min = 0
    is_init = True
    index = 0
    for curr_index, node_adr in enumerate(slavesAdr):
        rtt = evaluateRTT(node_adr)
        if is_init:
            index = curr_index
            is_init = False
        if rtt <= min:
            min = rtt
            index = curr_index

    print slavesAdr[index]
    cmd = buildCommand(username, slavesAdr[index], slqCommand, password)
    return launchCommand(cmd)

def main():
    """Main."""
    s = socket.socket()
    s.bind((host, port))

    s.listen(1)  # Listen to one connection
    c, addr = s.accept()
    print 'connection from: ' + str(addr)

    while True:
        data = c.recv(2048)  # Max bytes
        if not data:
            break
        print 'from connected user: ' + str(data)
        data = str(data)
        type, slqCommand = parse_data(data)
        # We need to detect INSERT or SELECT
        # In case of "INSERT", we hit Master node in MySQL Cluster
        # In case of "SELECT", we call the
        output = ""
        if type == 'insert':
            output = hitmaster(slqCommand)
        else:
            output = my_pattern(slqCommand)
        c.send(output)
        
    c.close()


def parse_data(data):
    """Function that takes the data and parses it."""
    command = ''
    #TO DO faire un traitement plus intelligent?
    #utiliser data pour avoir plus d'info?
    command = str(data)
    type = ''
    #TO DO ameliorer le test
    #si l'utilisateur utilise select
    #si un champ de la table est select
    if string.find(command,'INSERT') != -1:
        type = 'insert'
        fields = command.split(',')
        command = buildInsert(*fields[1:])
    elif string.find(command,'SELECT') != -1:
        type = 'select'
        command = buildSelect()

    return type, command


def my_pattern(slqCommand):
    """Implement algorithm of the pattern here."""
    # Connect to MySQL Cluster
    # Hit the database based on the algorithm
    # TO CHANGE : use the good algorithm
    return directHit(slqCommand)
    #return randomHit(slqCommand)
    #return customHit(slqCommand)


if __name__ == '__main__':
    main()
