#!/usr/bin/env python3

'''
Update support functions to utilize Git/GitHub for live system updates
'''

import os
import json

def default_update_data():
	update_data = {}
	update_data['repo_url'] = ''
	update_data['branch_target'] = ''
	update_data['version'] = ''
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
		if('remotes' not in line):
			branch_list.append(line.strip(' \n *'))
	return(branch_list)

def get_branch():
	command = "git branch --show-current"
	branch = os.popen(command).readline()
	branch = branch.strip(' \n')
	return(branch)

def set_branch(branch_target):
	update_data = read_update_data()
	update_data['branch_target'] = branch_target 
	command = "git checkout branch_target"
	result = os.popen(command).readlines() 
	return(result)

def get_available_updates(branch=''):
	result = {}
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
	return(result)

def do_update():
	command = "git fetch"
	os.popen(command)
	command = "git merge"
	mergeattempt = os.popen(command).readlines()
	for line in mergeattempt:
		print(f'{line}')
		if('Failed' in line):
			print('!!!!!!Failure detected.')
		if('Success' in line):
			print('!!!!!!Success')

def restart_scripts():
	print('Restarting Scripts... ')
	command = "service supervisor restart"
	os.popen(command)