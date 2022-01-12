#!/usr/bin/env python3

"""
 *****************************************
 	Flask Script
 *****************************************

 Description: WebUI for the project.  

 *****************************************
"""

from flask import Flask, request, render_template, make_response, redirect, jsonify, abort
from common import *
from p_logging import *
from p_updater import *
import os

"""
Globals
"""
app = Flask(__name__)
settings = read_settings()


"""
App Route Functions Begin
"""
@app.route('/', methods=['POST','GET'])
def index():
	global settings

	# Create Alert Structure for Alert Notification
	alert = { 
		'type' : '', 
		'text' : ''
		}

	return render_template('index.html', settings=settings, alert=alert)

@app.route('/settings', methods=['POST','GET'])
def settings_base(action=None):
	global settings

	# Create Alert Structure for Alert Notification
	alert = { 
		'type' : '', 
		'text' : ''
		}

	# Update the system theme
	if('theme' in request.form):
		for theme in settings['globals']['themelist']:
			if theme['name'] == request.form['theme']:
				settings['globals']['theme'] = theme['filename']
				write_settings(settings)
				alert['type'] = 'success'
				alert['text'] = 'Theme updated to ' + theme['name'] + "."

	return render_template('settings.html', alert=alert, settings=settings)

@app.route('/checkupdate', methods=['GET'])
def checkupdate(action=None):
	global settings
	update_data = read_update_data()
	print(f'Version: {settings["globals"]["version"]}')
	if(update_data['version'] == ''):
		update_data['version'] = settings['globals']['version']
		write_update_data(update_data)
	if(update_data['branch_target'] == ''):
		update_data['branch_target'] = get_branch()
		write_update_data(update_data)
	if(update_data['remote_url'] == ''):
		remote_url = get_remote_url()
		if('ERROR' in remote_url):
			print('f{remote_url}')
		else:
			update_data['remote_url'] = remote_url
			write_update_data(update_data)

	avail_updates_struct = get_available_updates()

	if(avail_updates_struct['success']): 
		commits_behind = avail_updates_struct['commits_behind']
	else:
		return jsonify({'result' : 'failure'})

	return jsonify({'result' : 'success', 'current' : update_data['version'], 'behind' : commits_behind})

@app.route('/update', methods=['POST','GET'])
def update_page(action=None):
	global settings
	update_data = read_update_data()

	# Update the information in the updater.json file	
	update_data['version'] = settings['globals']['version']
	update_data['branch_target'] = get_branch()
	update_data['branches'] = get_available_branches()
	update_data['remote_url'] = get_remote_url()
	write_update_data(update_data)

	# Create Alert Structure for Alert Notification
	alert = { 
		'type' : '', 
		'text' : ''
		}

	return render_template('updater.html', alert=alert, settings=settings, update_data=update_data)


@app.route('/admin/<action>', methods=['POST','GET'])
@app.route('/admin', methods=['POST','GET'])
def admin(action=None):
	global settings
	update_data = read_update_data()

	# Create Alert Structure for Alert Notification
	alert = { 
		'type' : '', 
		'text' : ''
		}

	if action == 'reboot':
		event = "Reboot Requested."
		write_log(event, logtype="REBOOT")
		os.system("sleep 3 && sudo reboot &")

		#Show Reboot Splash
		return render_template('shutdown.html', action=action, settings=settings)

	if action == 'shutdown':
		event = "Shutdown Requested."
		write_log(event, logtype="SHUTDOWN")
		os.system("sleep 3 && sudo shutdown -h now &")

		#Show Shutdown Splash
		return render_template('shutdown.html', action=action, settings=settings)

	uptime = os.popen('uptime').readline()

	cpuinfo = os.popen('cat /proc/cpuinfo').readlines()

	return render_template('admin.html', alert=alert, uptime=uptime, cpuinfo=cpuinfo, settings=settings, update_data=update_data)

@app.route('/manifest')
def manifest():
    res = make_response(render_template('manifest.json'), 200)
    res.headers["Content-Type"] = "text/cache-manifest"
    return res

"""
Supporting Functions
"""

"""
Run Flask App
"""
if __name__ == '__main__':
	if is_raspberrypi():
		app.run(host='0.0.0.0')
	else:
		app.run(host='0.0.0.0', debug=True)
