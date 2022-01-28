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
import os 
from p_logging import write_log

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
		]
	}

	settings['versions'] = {
		'server' : '1.1.6'
	}

	return settings

def read_settings(filename='settings.json'):
	"""
		# Read settings from JSON
	"""
	# Get latest settings format
	settings = default_settings()

	try:
		json_data_file = os.fdopen(os.open(filename, os.O_RDONLY))
		json_data_string = json_data_file.read()
		settings_struct = json.loads(json_data_string)
		json_data_file.close()

	except(IOError, OSError):
		# Issue with reading states JSON, so create one/write new one
		write_settings(settings)
		return(settings)
	except(ValueError):
		# A ValueError Exception occurs when multiple accesses collide, this code attempts a retry.
		event = 'ERROR: Value Error Exception - JSONDecodeError reading settings.json'
		write_log(event, logtype='ERROR')
		json_data_file.close()
		# Retry Reading Settings
		settings_struct = read_settings(filename=filename) 

	# Overlay the read values over the top of the default settings
	#  This ensures that any NEW fields are captured.  
	update_settings = False # set flag in case an update needs to be written back

	# If default version is different from what is currently saved, update version in saved settings
	if('versions' not in settings_struct.keys()):
		settings_struct['versions'] = {
			'server' : settings['versions']['server']
		}
		update_settings = True
	elif(settings_struct['versions']['server'] != settings['versions']['server']):
		settings_struct['versions']['server'] = settings['versions']['server']
		update_settings = True	

	for key in settings.keys():
		if key in settings_struct.keys():
			for subkey in settings[key].keys():
				if subkey not in settings_struct[key].keys():
					update_settings = True
			settings[key].update(settings_struct.get(key, {}))
		else: 
			update_settings = True 

	if (update_settings) or (filename != 'settings.json'): # If any of the keys were added, then write back the changes 
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

def restart_scripts():
	print('[DEBUG MSG] Restarting Scripts... ')
	command = "sleep 3 && sudo service supervisor restart &"
	if(is_raspberrypi()):
		os.popen(command)