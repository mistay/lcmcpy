
import atexit
import datetime
import os
import signal
import sys
import time
import socket
import myweb

class Daemon(object):

	version = "v0.1"

	if __name__ == '__main__':
		print( "lcmc %s starting...." % version)

		w = myweb.MyWebserver()
		w.run()


		