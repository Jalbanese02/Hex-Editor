#!/usr/bin/env python3

import os

def read_settings_file():
	"""
	Reads the settings file and creates a settings dictionary from it's data.
	It also configures the color scheme values according to the color scheme saved in the data.
	Data in the file is of format <setting1>:<value>;<setting2>:<value2>...
	This function also tries its best to handle any errors the program may encounter when the user
	messes with the settings file.
	

	return: None, if something went wrong and the settings dict if everything went okay. 
	"""
	absolute_settings_file_path = "/tmp/GHE/settings.cfg"

	try:
		settings_file = open(absolute_settings_file_path, 'r')

	except OSError:
		return None

	lines = settings_file.readlines()
	settings_line = ''
	settings_dict = {}

	for line in lines:
		if line[0] != '#':
			settings_line = line

	try:
		for setting in settings_line.split(';'):
			settings_dict[setting.split(':')[0]] = setting.split(':')[1]

	except IndexError:
		settings_file.close()
		return None

	else:
		try:
			if settings_dict['color_scheme'] == 'default':
				settings_dict['btn_color'] = 'gray85'
				settings_dict['bg_color_1'] = 'gray95'
				settings_dict['bg_color_2'] = 'white'
				settings_dict['bg_color_3'] = 'gray70'
				settings_dict['fg'] = 'black'

			elif settings_dict['color_scheme'] == 'dark_1':
				settings_dict['btn_color'] = 'gray12'
				settings_dict['bg_color_1'] = 'gray40'
				settings_dict['bg_color_2'] = 'gray30'
				settings_dict['bg_color_3'] = 'gray70'
				settings_dict['fg'] = 'green2'


			elif settings_dict['color_scheme'] == 'dark_2':
				settings_dict['btn_color'] = 'gray12'
				settings_dict['bg_color_1'] = 'gray40'
				settings_dict['bg_color_2'] = 'gray25'
				settings_dict['bg_color_3'] = 'deep sky blue'
				settings_dict['fg'] = '#0bf'
			else:
				return None


		except KeyError:
			return None

	settings_file.close()

	#Validate all the settings that may break the program when they are corrupted.
	try:
		try:
			if int(settings_dict["line_size"]) < 128 and int(settings_dict["line_size"]) > 0:
				if int(settings_dict["chunk_size"]) < 20 and int(settings_dict["line_size"]) > 0:
					if int(settings_dict["jump_size"]) > 0:
					
						#Get a size for the keypad buttons that somewhat fits into the window properly. The magical number 2 just works.
						settings_dict["keypad_button_width"] = int(settings_dict["line_size"]) // 2 // int(settings_dict["chunk_size"])
						return settings_dict
			
		except ValueError:
			return None

	except KeyError:
		return None
	


def save_settings(save_settings_dict):
	"""
	This function writes a settings dictionary into the file settings.cfg.
	The file has a comment in its first line and after that comes the data. 
	Data is of format <setting1>:<value>;<setting2>:<value2>;...

	param: settings dictionary to be written to the file
	return: 0 if everything went as planned and one if saving the settings failed.
	"""

	absolute_settings_file_path = f"/tmp/GHE/settings.cfg"

	setting_and_value = ''
	settings_list = []

	for setting in save_settings_dict:
		settings_list.append(f"{setting}:{save_settings_dict[setting]}")
	
	try:
		settings_file = open(absolute_settings_file_path, 'w')
	except OSError:
		return 1

	settings_file.write('#WARNING: INCORRECTLY CHANGING THE CONTENTS OF THIS FILE MAY BREAK THE PROGRAM\n' + ';'.join(settings_list))
	settings_file.close()

	return 0
