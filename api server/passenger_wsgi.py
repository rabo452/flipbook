import imp
import os
import sys

# these lines need for run the app with python3 interpeter, if server by default run the app as python2, you need to find the folder of python3 in the ROOT of server in /usr/bin/ .... folder
# /usr/bin/python3 - the path for python3 folder,
# but again if server run the app with python2
# if server run app as python3 and higher comment it
INTERP = "/usr/bin/python3"
if sys.executable != INTERP: os.execl(INTERP, INTERP, *sys.argv)

sys.path.insert(0, os.path.dirname(__file__))

wsgi = imp.load_source('wsgi', 'start.py')
application = wsgi.app
