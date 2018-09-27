#!/usr/bin/python

#attention le script necessite d'avoir aws cli installe ainsi que boto
#apt-get install awscli
#Faire des identifiants IAM via la console amazon web
#aws configure
#pip install -U boto
#pour de l'aide voir : https://aws.amazon.com/articles/3998

import boto.ec2
import commands
import sys, getopt
import threading
import logging


sshKey = ""
sshKeyFile = ""
bench = ""
my_security_group = "" 
install_bench = "install_"
base_cmd = "./bench.sh"
known_bench = ["cpu", "io", "iops"]
known_install_cmd = ["install_cpu", "install_io", "install_iops"]
install_needed = ["cpu", "iops"]
#instance types needed for the benchmark
instanceTypes = ["t2.small", "m4.2xlarge", "c4.4xlarge"]
region = "us-west-2"
#AMI for amazon
ami = "ami-b7a114d7"
is_full_test = False

def usage():
	print "%s -i privateKeyName (without .pem) -b benchmark to use -g security group" % sys.argv[0]

def create_instances():
	#Create a connection to the distant management control
	myConnection = boto.ec2.connect_to_region(region) #we always connect ourselves to the same region
	#we create the instances
	instances = []
	for instanceType in instanceTypes:
		reservation = myConnection.run_instances(
        	ami,
        	key_name=sshKey,
        	instance_type=instanceType,
        	security_groups=[my_security_group])
		#we need to wait for the machine to boot in order to ssh
		status = reservation.instances[0].update()
		while  status != "running": #We wait for the machine to be up
			status = reservation.instances[0].update()
		instances.append(reservation.instances[0]) #we get the only instance we create throught the previous cmd
	return (myConnection, instances)

def terminate_instances(ec2_connect, instances):
	instances_ids = []
	for instance in instances:
		instances_ids.append(instance.id)
	ec2_connect.terminate_instances(instance_ids = instances_ids)

#Warning blocking call!!!!!
def remote_run(barec_md, bench, instances):
	print barec_md, bench
	for instance in instances:
		dns = instance.public_dns_name
		complete_cmd = "%s -i %s -t %s  -m ubuntu@%s -o %s%s" % (barec_md, sshKeyFile,  bench, dns, bench, instance.instance_type)
		print complete_cmd
		remote_cout = commands.getoutput(complete_cmd)
		print remote_cout

def async_remote_run(barec_md, bench, instances):
	threads = []
	for instance in instances:
		dns = instance.public_dns_name
		complete_cmd = "%s -i %s -t %s  -m ubuntu@%s -o %s%s" % (barec_md, sshKeyFile,  bench, dns, bench, instance.instance_type)
		async_cmd = threading.Thread(name=instance.instance_type, target=cmd_worker,args=(complete_cmd,))
		threads.append(async_cmd)
		async_cmd.start()
	return threads

def cmd_worker(full_cmd):
	print "Starting : %s" % (threading.currentThread().getName()) 
	remote_out = commands.getoutput(full_cmd)
	print "Exiting : %s => %s" % (threading.currentThread().getName(), remote_out)

def wait_for_threads(mythreads):
	for thd in mythreads:
		thd.join()




#start of the script
if len(sys.argv) <= 1:
	usage()
	sys.exit(0)


opts, args = getopt.getopt(sys.argv[1:],"hi:b:ag:")
for opt, arg in opts:
	if opt == '-i':
		sshKey = arg
		sshKeyFile = "%s.pem" % sshKey
	elif opt == '-g':
		my_security_group = arg
	elif opt == '-b':
		bench = arg
	elif opt == '-a':
		is_full_test = True
	else:
		usage()
		sys.exit(0)

ec2_co, instances = create_instances()
allthreads = []
if is_full_test:
	for install in known_install_cmd:
		remote_run(base_cmd, install_bench, instances)
	for bench in known_bench:
		allthreads.extend(async_remote_run(base_cmd, bench, instances))
		wait_for_threads(allthreads)
		allthreads = []
		terminate_instances(ec2_co, instances)
else:
	if bench in install_needed:
		install_bench = "%s%s" % (install_bench, bench)	
		remote_run(base_cmd, install_bench, instances)
	allthreads.extend(async_remote_run(base_cmd, bench, instances))
	wait_for_threads(allthreads)
	terminate_instances(ec2_co, instances)