import os 
import sys
import paramiko
import scpclient
from contextlib import closing
import time

ssh = paramiko.SSHClient()
ssh.load_system_host_keys()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())

pt = 22
uname = 'kddev'
pwd = 'Kuan123-deng'

def checkfile(release_path, server):
        filename = release_path + server
        if os.path.exists(filename):
                print ("right way : " +release_path + filename)
        else:
                print ("you enter a wrong path")
                sys.exit(1)

def stop_cmd(ip , krs_sh, krs_jar, krs_jar_bak,release_path):
	print("now stopping the host :" + ip)
	ssh.connect(ip, pt, username=uname, password=pwd)
	stdin, stdout, stderr = ssh.exec_command('sudo rm -rf %s' %krs_jar_bak)

	err_list = stderr.readlines()
        stdout_list = stdout.readlines()
        print err_list
        print stdout_list

	stdin, stdout, stderr = ssh.exec_command('sudo %s stop' %krs_sh)
	err_list = stderr.readlines()
        stdout_list = stdout.readlines()
        print err_list
        print stdout_list
	
	print ('sudo %s stop' %krs_sh)
	time.sleep(10)
	stdin, stdout, stderr = ssh.exec_command('sudo mv %s %s' %(krs_jar, krs_jar_bak))
	err_list = stderr.readlines()
        stdout_list = stdout.readlines()
        print err_list
        print stdout_list

def release_service(ip , krs_sh, krs_jar, krs_jar_bak,release_path, lib_path, server):
	jar_file = release_path + server
	print("now distribution to the host :" + ip)
	ssh.connect(ip, port=pt, username=uname, password=pwd)
	with closing(scpclient.Write(ssh.get_transport(), remote_path=lib_path)) as scp:
		scp.send_file(jar_file, preserve_times=True)
	print ("file has arrive :" + lib_path)
	time.sleep(10)

def start_cmd(ip, krs_sh):
	print("now start the host :" + ip)
	ssh.connect(ip, pt, username=uname, password=pwd)	
	stdin, stdout, stderr = ssh.exec_command('sudo %s start' %krs_sh)
	err_list = stderr.readlines()
        stdout_list = stdout.readlines()
        print err_list
        print stdout_list
	print ("process is starting,wait a momunt")
	print ('sudo %s start' %krs_sh)


if __name__=='__main__':
	release_path = sys.argv[1]
	print ("release_path :" + release_path)
	for line in sys.stdin:
		ip , krs_sh, krs_jar, krs_jar_bak, lib_path ,server  = line.strip().split()
		checkfile(release_path, server)
		stop_cmd(ip , krs_sh, krs_jar, krs_jar_bak,release_path)
		release_service(ip , krs_sh, krs_jar, krs_jar_bak,release_path, lib_path, server)
		start_cmd(ip, krs_sh)
#		test_krs_info(ip , krs_sh, krs_jar, krs_jar_bak,release_path, lib_path)
