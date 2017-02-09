## qdotsync
sync files from qdot-server in the folk lab

### Environment Variables

To use this package you will need to setup three environment variables.

1. QDOTSYNC_CACHE -- this is your cache folder where data can be stored temporarily
2. QDOTSYNC_LOCAL -- this is a more permanent location on your computer where you like to store data
3. QDOTSYNC_USER -- your username on qdot-server

### Usage

The commands below will copy a folder (or file) from the server to a folder (file) of the same name within QDOTSYNC_CACHE or QDOTSYNC_LOCAL.

Sync to QDOTSYNC_CACHE:

```python
srv_dir = '/qdot26/Silvia/fridge_vibration_Feb2017/'
data_dir = qdotsync.sync_now(srv_dir)
    
os.chdir(data_dir)
```

Sync to QDOTSYNC_LOCAL:

```python
srv_dir = '/qdot26/Silvia/fridge_vibration_Feb2017/'
data_dir = qdotsync.sync_now(srv_dir, dest='local')
    
os.chdir(data_dir)
```

Delete the QDOTSYNC_CACHE. This was functionality was added to keep your harddrive clean from old data piling up. Run it at the end of your day of analysis to delete the cache.

```python
qdotsync.clear_cache()
```



