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
				settings['misc']['theme'] = theme['filename']
				write_settings(settings)
				alert['type'] = 'success'
				alert['text'] = 'Theme updated to ' + theme['name'] + "."

	return render_template('settings.html', alert=alert, settings=settings)

@app.route('/checkupdate', methods=['GET'])
def checkupdate(action=None):
	global settings
	update_data = read_update_data()

	commits_behind = get_available_updates()
	return jsonify({'result' : 'success', 'current' : update_data['version'], 'behind' : commits_behind})

@app.route('/admin/<action>', methods=['POST','GET'])
@app.route('/admin', methods=['POST','GET'])
def admin(action=None):
	global settings

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

	return render_template('admin.html', alert=alert, uptime=uptime, cpuinfo=cpuinfo, settings=settings)

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
