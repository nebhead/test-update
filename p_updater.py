#!/usr/bin/env python3

'''
Update support functions to utilize Git/GitHub for live system updates
'''

import os
import json

def default_update_data(version='2022.1.0'):
	update_data = {}
	update_data['remote_url'] = get_remote_url()
	update_data['branch_target'] = get_branch()
	update_data['version'] = version
	update_data['branches'] = get_available_branches()
	return update_data

def read_update_data():
	"""
		# Read update data/settings from JSON
	"""
	try:
		json_data_file = open("updater.json", "r")
		json_data_string = json_data_file.read()
		update_data = json.loads(json_data_string)
		json_data_file.close()

	except(IOError, OSError):
		# Issue with reading settings JSON, so create one/write new one
		update_data = default_update_data()
		write_update_data(update_data)

	return(update_data)

def write_update_data(update_data):
	"""
		# Write settings from JSON
	"""
	json_data_string = json.dumps(update_data, indent=2, sort_keys=True)
	with open("updater.json", 'w') as data_file:
	    data_file.write(json_data_string)

def get_available_branches():
	command = "git branch -a"
	branches = os.popen(command).readlines()
	branch_list = []
	for line in branches:
		line = line.strip(' \n *')
		if('origin/main' in line):
			# Skip this line
			pass
		elif('remotes/origin/' in line):
			line = line.replace('remotes/origin/', '')
			if (line not in branch_list):
				branch_list.append(line)
		else:
			branch_list.append(line)
	return(branch_list)

def get_branch():
	command = "git branch --show-current"
	branch = os.popen(command).readline()
	branch = branch.strip(' \n')
	return(branch)

def set_branch(branch_target):
	update_data = read_update_data()
	update_data['branch_target'] = branch_target 
	command = f'git checkout {branch_target}'
	result = os.popen(command).readlines() 
	return(result)

def get_remote_url():
	command = "git config --get remote.origin.url"
	remote = os.popen(command).readline()
	if(remote):
		return(remote.strip(' \n'))
	else:
		return('ERROR: Remote URL not specified in git config.')

def get_available_updates(branch=''):
	result = {}
	remote = get_remote_url()
	if('ERROR' not in remote):
		if(branch == ''):
			branch = get_branch()
		command = "git fetch"
		os.popen(command)
		command = f"git rev-list --left-only --count origin/{branch}...@"
		response = os.popen(command).readline()
		response = response.strip(' \n')
		if(response.isnumeric()):
			result['success'] = True 
			result['commits_behind'] = int(response)
		else: 
			result['success'] = False 
			result['message'] = response 
	else: 
		result['success'] = False 
		result['message'] = 'ERROR: No remote defined.' 
	return(result)

def do_update():
	'''
	Forced Update
	git fetch
	git reset --hard HEAD
	git merge '@{u}'
	'''
	command = "git fetch"
	os.popen(command)
	command = "git reset --hard HEAD"
	os.popen(command)
	command = "git merge '@\{u\}'"
	output = os.popen(command).readlines()
	return(output)

def restart_scripts():
	print('[DEBUG MSG] Restarting Scripts... ')
	command = "sleep 3 && service supervisor restart &"
	#os.popen(command)

