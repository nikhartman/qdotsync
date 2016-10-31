#!/anaconda/bin/python3

"""This script uses paramiko to handle the SSH connection and rsync to copy files from the server.
User needs to specify 'path_local', 'path_remote', 'server_adress', 'username' and 'password' (for the server).
Rsync will promt for the password every time unless a passwordless rsa key is created."""

import os
import time
import datetime
import paramiko

def InitRsync():
	path_local = '/Users/Christian/Documents/Chrede/UBC/Data';
	# add '/' to remote path unless you want the folder as well
	path_remote = '/srv/measurement-data/qdot26/Nik/';
	server_adress = 'qdot-server.phas.ubc.ca';
	username = 'colsen';
	# add --delete to flag for true sync. This will delete local files if they are deleted at source
	flag = '-azp';
	LocateLocalFolder(path_local);
	while True:
		# Open SSH connection
		client = OpenSSHConnection(server_adress,username);
		# Sync folder
		DoSync(server_adress,username,path_local,path_remote,flag);
		# Close connection
		CloseSSHConnection(client);
		# Wait 3 minutes
		time.sleep(3*60);

def LocateLocalFolder(path_local):
	# Checks if path_local exists
	# Creates a folder on path_local if it doesn't exist
	os.makedirs(path_local, exist_ok = True);

def DoSync(server_adress, username, path_local, path_remote, flag):
	# rsync [flag] source destination
	command = 'rsync %s %s@%s:%s %s' % (flag,username,server_adress,path_remote,path_local);
	os.system(command);
	timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S");
	print('%s, Remote folder synced' % (timestamp));

def OpenSSHConnection(server_adress,username):
	client = paramiko.SSHClient();
	client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	client.connect(server_adress, username = username);
	return client

def CloseSSHConnection(client):
	client.close();

InitRsync();