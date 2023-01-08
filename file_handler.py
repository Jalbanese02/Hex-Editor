#!/usr/bin/env python3

import os

def create_dump(offset, file, hex_data):
	"""
	This function takes the contents of the parameter file and writes them
	into a dump file which has the user made changes saved. A temporary file is used to 
	prevent writing to the same file that was given as a parameter and removing everything.
	
	param1: offset of the hex data that will be written
	param2: original file that will be copied into the dump
	param3: the hex data that will replace the old data in the given offset

	return: dump file for the program to now open
	"""
	try:
		tmp_file = open('/tmp/GHE/tmp', 'wb')
	
	except OSError:
		return


	file.seek(0)
	tmp_file.write(file.read())
	file.close()

	try:
		tmp_file = open(f"/tmp/GHE/tmp", 'rb')
	
	except OSError:
		return

	dump_file_path = "/tmp/GHE/dmp"

	#Turn the hex editor bytes into a bytes object
	binary_data = bytes.fromhex(hex_data.replace('\n',' ').replace(' ', ''))
	
	try:
		dump_file = open(dump_file_path, "wb")	

	except OSError:
		return

	if dump_file == file:
		print("bruh")

	#Write the contents of the temporary file into the dump file whit the made changes.
	tmp_file.seek(0)
	dump_file.write(tmp_file.read())
	dump_file.seek(offset)
	dump_file.write(binary_data)
	
	tmp_file.close()
	os.remove("/tmp/GHE/tmp")
	
	dump_file.close()

	dump_file = open(dump_file_path, "rb")	

	return dump_file



def get_text(binary_data, line_size=16):
	"""
	This function turns the parameter binary data into human readable
	ascii text. If the data is not meaningful, it will be represented
	as a dot.

	param: binary data to be read
	param2: frequency in which a newline will be inserted.
	"""


	text_representation = []

	for index in range(len(binary_data)):

		if index % (line_size) == 0 and index > 0:
			text_representation.append('\n')


		if binary_data[index] < 128 and binary_data[index] > 31:
			text_representation.append(chr(binary_data[index]))

		else:
			text_representation.append('.')

	return ''.join(text_representation)


def draw_editor_view(offset, file, chunk_size = 2, line_size=16):
	"""
	Reads from the given offset in the given file and creates the hexadecimal
	view of the data to be fed into the program editor. It also creates the address
	view. 

	param: offset to read from
	param2: file to read
	param3: chunk size specifies the frequency in bytes that a space will be inserted
	param4: frequency in which a newline will be inserted.:   
	"""

	file.seek(offset)
	binary_data = file.read(24 * line_size)

	hex_data = []
	address_list = [hex(offset) + ': ']
	ascii_data = []

	for index in range(chunk_size, len(binary_data) + chunk_size, chunk_size):

		if index % line_size == 0 and index != len(binary_data):
			hex_data.append(binary_data[index - chunk_size:index].hex().upper() + '\n')
			address_list.append(hex(offset + index) + ': ')

		else:
			hex_data.append(binary_data[index - chunk_size:index].hex().upper() + ' ')

	return ''.join(hex_data), '\n'.join(address_list), ''.join(get_text(binary_data, line_size))
