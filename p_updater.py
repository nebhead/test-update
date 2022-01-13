#!/usr/bin/env python3

'''
Update support functions to utilize Git/GitHub for live system updates
'''

import os
import time

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
	command = f'git checkout {branch_target}'
	result = os.popen(command).readlines() 
	time.sleep(1)
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
		time.sleep(1)
		response = response.strip(' \n')
		if(response.isnumeric()):
			result['success'] = True 
			result['commits_behind'] = int(response)
		else: 
			result['success'] = False 
			result['message'] = response 
	else: 
		result['success'] = False 
		result['message'] = 'ERROR: No remote repository defined.  You may need to re-install from the remote repository.' 
	return(result)

def do_update():
	'''
	Forced Update
	git fetch
	git reset --hard HEAD
	git merge '@{u}'
	'''
	remote = get_remote_url()
	if('ERROR' not in remote):
		command = "git fetch"
		os.popen(command)
		command = "git reset --hard HEAD"
		os.popen(command)
		command = "git merge \'@{u}\'"
		output = os.popen(command).readlines()
		time.sleep(1)
	else:
		output = ['ERROR: No remote configured.']
	return(output)

def restart_scripts():
	print('[DEBUG MSG] Restarting Scripts... ')
	command = "sleep 3 && service supervisor restart &"
	#os.popen(command)

def get_log(num_commits=10):
	branch = get_branch()
	command = f'git log origin/{branch} -{num_commits} --pretty="%h - %cr : %s"'
	output = os.popen(command).readlines()
	return(output)
