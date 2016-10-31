#!/usr/bin/python

"""This script uses paramiko to handle the SSH connection and rsync to copy files from the server.
User needs to specify 'path_local', 'path_remote', 'server_dress' and 'username'.
qdotsync will promt for the password every time unless a passwordless rsa key is created."""
 
import os, shutil
import time
import datetime
import paramiko
 
#### setup global/environmental variables ####

__SERVER__ = 'qdot-server.phas.ubc.ca' # qdot-server
__SRVDATA__ = '/srv/measurement-data/' # data directory on qdot-server
__EXTENSIONS__ = ['.ibw', '.pxp', '.winf'] # these are the only file types in measurement-data

if os.environ.get('QDOTSYNC_CACHE'):
    __CACHE__ = os.environ.get('QDOTSYNC_CACHE')
else:
    raise OSError('no envitonmental variable found for cache directory')
    
if os.environ.get('QDOTSYNC_LOCAL'):
    __LOCAL__ = os.environ.get('QDOTSYNC_LOCAL')
else:
    raise OSError('no envitonmental variable found for cache directory')

if os.environ.get('QDOTSYNC_USER'):
    __USER__ = os.environ.get('QDOTSYNC_USER')
else:
    raise OSError('no envitonmental variable found for cache directory')  

#### local and cache sync functions ####
 
def sync_now(path_remote, dest='cache'):
    """ sync the specified path_remote to the local data directory """
    
    client = open_ssh_connection() # open SSH connection

    # check if the path leads to a directory or file
    is_file = any(substring in path_remote for substring in __EXTENSIONS__)
    
    # setup full path to data on server
    if path_remote[0] == '/':
        path_remote = path_remote[1:]
    if not is_file:
        if not path_remote.endswith('/'):
            path_remote += '/'
    path_srv = __SRVDATA__ + path_remote 

    # setup local path
    if dest.lower()=='cache':
        __DEST__ = __CACHE__
    else:
        __DEST__ = __LOCAL__
    machine, user_dir, *sync_path = path_remote.split('/')

    if is_file:
        # path_remote = '/qdot26/Nik/mgaas1_Oct2016/dat10.ibw' 
        # copies dat10.ibw into __LOCAL__/mgaas1_2016/
        path_local = os.path.join(__DEST__, '/'.join(sync_path[:-1])) + '/'
        os.makedirs(path_local, exist_ok = True) # make sure it exists
    else:
        # '/qdot26/Nik/mgaas1_Oct2016/'
        # copies all files in mgaas1_Oct2016 into __LOCAL__/mgaas1_Oct2016
        path_local = os.path.join(__DEST__, '/'.join(sync_path))
        os.makedirs(path_local, exist_ok = True)

    do_sync(path_local,path_srv); # run rsync
    close_ssh_connection(client) # close connection
# 
    if is_file:
        return os.path.join(path_local, sync_path[-1])
    else:
        return path_local

def clear_cache():
    """ remove all files and folders from the cache directory """
    
    # make sure this directory is setup correctly and exists
    try:
        cache_dir = os.environ.get('QDOTSYNC_CACHE')
        if not os.path.isdir(cache_dir):
            raise OSError('cache directory not found')
    except Exception as e: 
        print('cannot clear cache: {0}'.format(e))
        return False
        
    for the_file in os.listdir(__CACHE__):
        file_path = os.path.join(__CACHE__, the_file)
        try:
            if os.path.isfile(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path): 
                shutil.rmtree(file_path)
        except Exception as e:
            print(e)
    print('cache directory cleared')
    return True
    
    
#### run rsync commmand ####

def do_sync(path_local, path_remote, flag = '-azp'):

    # build command: "rsync [flag] source destination"
    command = 'rsync %s %s@%s:%s %s' % (flag,__USER__,__SERVER__,path_remote,path_local)
    print(command)
    try:
        os.system(command) # execute command
    except Execption as e:
        print('rsync with qdot-server failed: {0}'.format(e))
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print('%s, Remote folder synced' % (timestamp))
    return None
    
#### ssh connection ####

def open_ssh_connection():
    client = paramiko.SSHClient();
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(__SERVER__, username = __USER__);
    return client
 
def close_ssh_connection(client):
    client.close()