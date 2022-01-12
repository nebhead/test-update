#!/usr/bin/env python3

"""
 *****************************************
 	Control Script
 *****************************************

 Description: This script runs as a separate process from the Flask / Gunicorn
  implementation which handles the web interface.

 *****************************************
"""

"""
 *****************************************
 	Imported Libraries
 *****************************************
"""
import time
from common import *
from p_logging import write_log

"""
 *****************************************
 	Init Variables
 *****************************************
"""
settings = read_settings()  # Get initial settings

event = 'Control Script Starting.'
write_log(event, logtype='STARTUP')

"""
 *****************************************
 	Main Function
 *****************************************
"""
def main():
	global settings

	# Main Loop
	while True:
		print('... looping ...')
		time.sleep(0.1)
"""
 *****************************************
 	Supporting Functions
 *****************************************
"""

"""
 *****************************************
 	Run Main
 *****************************************
"""
if __name__ == "__main__":
	main()

event = 'Control Script Exiting.'
write_log(event, logtype='EXIT')
exit()