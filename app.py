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

'''
Updater Section
'''

@app.route('/checkupdate', methods=['GET'])
def checkupdate(action=None):
	global settings
	update_data = {}
	update_data['version'] = settings['versions']['server']

	avail_updates_struct = get_available_updates()

	if(avail_updates_struct['success']): 
		commits_behind = avail_updates_struct['commits_behind']
	else:
		event = avail_updates_struct['message']
		write_log(event, 'ERROR')
		return jsonify({'result' : 'failure', 'message' : avail_updates_struct['message'] })

	return jsonify({'result' : 'success', 'current' : update_data['version'], 'behind' : commits_behind})

@app.route('/update', methods=['POST','GET'])
def update_page(action=None):
	global settings

	# Populate Update Data Structure
	update_data = {}
	update_data['version'] = settings['versions']['server']
	update_data['branch_target'], error_msg = get_branch()
	if error_msg != '':
		write_log(error_msg, 'ERROR')
	update_data['branches'], error_msg = get_available_branches()
	if error_msg != '':
		write_log(error_msg, 'ERROR')
	update_data['remote_url'], error_msg = get_remote_url()
	if error_msg != '':
		write_log(error_msg, 'ERROR')
	update_data['remote_version'], error_msg = get_remote_version()
	if error_msg != '':
		write_log(error_msg, 'ERROR')

	# Create Alert Structure for Alert Notification
	alert = { 
		'type' : '', 
		'text' : ''
		}

	if(request.method == 'POST'):
		r = request.form 
		print(f'POST Response: {r}')

		if('change_branch' in r):
			if(update_data['branch_target'] in r['branch_target']):
				alert = { 
					'type' : 'success', 
					'text' : f'Current branch {update_data["branch_target"]} already set to {r["branch_target"]}'
				}
				return render_template('updater.html', alert=alert, settings=settings, update_data=update_data)
			else: 
				result, error_msg = set_branch(r['branch_target'])
				if error_msg == '':
					action = 'restart'
					output_html = f'*** Changing from current branch {update_data["branch_target"]} to {r["branch_target"]} ***<br><br>'
					output_html += result 
					restart_scripts()
				else:
					action = ''
					output_html = f'*** Changing from current branch {update_data["branch_target"]} to {r["branch_target"]} Experienced Errors ***<br><br>'
					output_html += error_msg

				return render_template('updater_out.html', settings=settings, action=action, output_html=output_html)				

		if('do_update' in r):
			print('Update Requested')

			result, error_msg = do_update() 
			if error_msg == '':
				action='restart'
				output_html = f'*** Attempting an update on {update_data["branch_target"]} ***<br><br>' 
				output_html += result 
				restart_scripts()
			else:
				action=''
				output_html = f'*** Attempting an update on {update_data["branch_target"]} ***<br><br>' 
				output_html += error_msg
			return render_template('updater_out.html', settings=settings, action=action, output_html=output_html)

		if('show_log' in r):
			print('Log requested')
			if(r['show_log'].isnumeric()):
				action='log'
				result, error_msg = get_log(num_commits=int(r['show_log']))
				if error_msg == '':
					output_html = f'*** Getting latest updates from origin/{update_data["branch_target"]} ***<br><br>' 
					output_html += result
				else: 
					output_html = f'*** Getting latest updates from origin/{update_data["branch_target"]} ERROR Occurred ***<br><br>' 
					output_html += error_msg
			else:
				output_html = '*** Error, Number of Commits Not Defined! ***<br><br>'
				
			return render_template('updater_out.html', settings=settings, action=action, output_html=output_html)

	return render_template('updater.html', alert=alert, settings=settings, update_data=update_data)
'''
End Updater Section
'''

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
