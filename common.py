#!/usr/bin/env python3

"""
 *****************************************
 	Common Script
 *****************************************

 Description: Common functions used by multiple scripts.  

 *****************************************
"""

import datetime
import json
import io

def default_settings():
	settings = {}

	settings['globals'] = {
		'public_url': '',
		'theme': 'bootstrap-darkly.css', # default to base theme, bootstrap-yeti.css is my second favorite 
		'themelist': [
			{
				'name' : 'Bootstrap',
			 	'filename' : 'bootstrap.css'
			},
			{
				'name' : 'Darkly (Default)',
			 	'filename' : 'bootstrap-darkly.css'
			},
			{
				'name' : 'Flatly',
			 	'filename' : 'bootstrap-flatly.css'
			},
			{
				'name' : 'Litera',
			 	'filename' : 'bootstrap-litera.css'
			},
			{
				'name' : 'Lumen',
			 	'filename' : 'bootstrap-lumen.css'
			},
			{
				'name' : 'Lux',
			 	'filename' : 'bootstrap-lux.css'
			},
			{
				'name' : 'Sandstone',
			 	'filename' : 'bootstrap-sandstone.css'
			},
			{
				'name' : 'Slate',
			 	'filename' : 'bootstrap-slate.css'
			},
			{
				'name' : 'Superhero',
			 	'filename' : 'bootstrap-superhero.css'
			},
			{
				'name' : 'Yeti (Best Light Theme)',
			 	'filename' : 'bootstrap-yeti.css'
			},
			{
				'name' : 'Zephyr',
			 	'filename' : 'bootstrap-zephyr.css'
			}
		],
		'version': '2022.1.7' 
	}

	return settings

def read_settings():
	"""
		# Read settings from JSON
	"""
	try:
		json_data_file = open("settings.json", "r")
		json_data_string = json_data_file.read()
		settings = json.loads(json_data_string)
		json_data_file.close()

	except(IOError, OSError):
		# Issue with reading settings JSON, so create one/write new one
		settings = default_settings()
		write_settings(settings)

	return(settings)

def write_settings(settings):
	"""
		# Write settings from JSON
	"""
	json_data_string = json.dumps(settings, indent=2, sort_keys=True)
	with open("settings.json", 'w') as settings_file:
	    settings_file.write(json_data_string)

def get_unique_id():
	"""
		# Create a unique ID based on the time
	"""
	now = str(datetime.datetime.now())
	now = now[0:19] # Truncate the microseconds

	ID = ''.join(filter(str.isalnum, str(datetime.datetime.now())))
	return(ID)

'''
is_raspberrypi() function borrowed from user https://raspberrypi.stackexchange.com/users/126953/chris
  in post: https://raspberrypi.stackexchange.com/questions/5100/detect-that-a-python-program-is-running-on-the-pi
'''
def is_raspberrypi():
	try:
		with io.open('/sys/firmware/devicetree/base/model', 'r') as m:
			if 'raspberry pi' in m.read().lower(): return True
	except Exception: pass
	return False