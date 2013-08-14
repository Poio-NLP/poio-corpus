import os

bind = "127.0.0.1:8200"
workers = (os.sysconf("SC_NPROCESSORS_ONLN") * 2) + 1
#loglevel = "error"
proc_name = "poio"
logfile = '/home/sites/poio/site/flask-app/debug.log'
loglevel = 'debug'
