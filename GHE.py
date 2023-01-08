#!/usr/bin/env python3


from tkinter import *
from tkinter.filedialog import askopenfilename, asksaveasfilename
import os, tkinter.messagebox, sys
import file_handler, settings_manager, settings_window

DEFAULT_SETTINGS = {'chunk_size': '4', 'line_size': '32', 'color_scheme': 'default', 'show_keypad': '0',\
'btn_color': 'gray85', 'bg_color_1': 'gray95', 'bg_color_2': 'white', 'bg_color_3': 'gray70', 'fg': 'black', 'keypad_button_width': 2, 'jump_size' : 100}


class GUI:

	def __init__(self):

		self.__mainw = Tk()
		self.__mainw.resizable(False, False)
		self.__mainw.title("Ghetto Hex Editor")
		self.__mainw.protocol("WM_DELETE_WINDOW", self.closing_program)


		settings = self.get_settings()
			
		if settings == DEFAULT_SETTINGS:
			self.__mainw.title("Ghetto Hex Editor (DEFAULT SETTINGS)")

		
		self.__mainw.configure(bg=settings['bg_color_1'])
		self.__line_size = int(settings["line_size"])
		self.__chunk_size = int(settings["chunk_size"])
		self.__big_offset_jump = int(settings["jump_size"])


		#Split the GUI into frames
		text_area_frame = Frame(self.__mainw)
		keypad_frame = Frame(self.__mainw, bg=settings['bg_color_1'], bd=10)
		scrollbar_frame = Frame(self.__mainw, bg=settings['bg_color_1'])
		functions_frame = Frame(self.__mainw, bg=settings['bg_color_1'])
		label_frame = Frame(self.__mainw)


		if int(settings["show_keypad"]) == 1:
			keypad_frame.grid(row = 1, column = 1, columnspan = 2, padx=10, sticky=W+E)
		
		text_area_frame.grid(row = 0, columnspan=2, column = 0)
		scrollbar_frame.grid(row = 0, column = 2, sticky=N+S)
		functions_frame.grid(row = 1, column = 0, sticky="nswe")
		label_frame.grid(row=2, column=0, columnspan=3, sticky="ew")
		self.__mainw.columnconfigure(0, weight=3)
		self.__mainw.rowconfigure(2, weight=4)


		#Initialize each widget in each frame
		self.__hex_box = Text(text_area_frame, width = self.__line_size * 2 + (self.__line_size // self.__chunk_size) + 2, bg=settings['bg_color_2'], fg = settings['fg'])
		self.__text_box = Text(text_area_frame, width = self.__line_size + 2, bg=settings['bg_color_2'], fg = settings['fg'])
		self.__address_box = Text(text_area_frame, width=11, bg=settings['bg_color_2'], fg = settings['fg'])

		move_up_button = Button(scrollbar_frame, text="▲", command = lambda move_amount = -1: self.offset_move(move_amount), bg=settings['btn_color'], fg = settings['fg'])
		move_down_button = Button(scrollbar_frame, text="▼", command = lambda move_amount = 1: self.offset_move(move_amount), bg=settings['btn_color'], fg = settings['fg'])
		self.__scrollbar_slider = Scale(scrollbar_frame, orient=VERTICAL, from_=0, command=self.scroll, showvalue=False, troughcolor=settings['bg_color_1'], bg=settings['bg_color_1'], width = 35)

		seek_offset_button = Button(functions_frame, text="Go to offset:", command=self.seek_offset, relief=RIDGE, bg=settings['btn_color'], fg = settings['fg'])
		self.__edit_hex_button = Button(functions_frame, text="Edit Hex", command=self.hex_edit, relief=RIDGE, width=17, bg=settings['btn_color'], fg = settings['fg'])
		nop_replace_button = Button(functions_frame, text="Replace with NOP", command= self.replace_with_nop, relief=RIDGE, fg = settings['fg'], width=17, bg=settings['btn_color'])
		replace_with_byte_button = Button(functions_frame, text="Replace With Byte..", command=self.choose_replace_byte, relief=RIDGE, fg = settings['fg'], width=17, bg=settings['btn_color'])
		self.__offset_entry = Entry(functions_frame, bg=settings['bg_color_2'], fg=settings['fg'])

		self.__status_label = Label(label_frame, text="Please open a file to start editing.  ", relief=SUNKEN, bg=settings['bg_color_3'], padx=10)
		self.__file_name_label = Label(label_frame, text="No file opened", bg=settings['bg_color_3'], anchor=E, relief=SUNKEN, width=20)

		#Create the menu and assing commands.
		root_menu = Menu(self.__mainw)
		self.__mainw.config(menu=root_menu)
		file_menu = Menu(root_menu,  tearoff=False)
		root_menu.add_cascade(label="File", menu=file_menu)
		file_menu.add_command(label="Open File...", command=self.open_file)
		file_menu.add_command(label="Save", command=self.save_changes)
		file_menu.add_command(label="Save As...", command=lambda save_as = True: self.save_changes(save_as))
		root_menu.add_command(label="Preferences...", command = lambda settings_dict = settings: self.start_settings_window(settings_dict))
		root_menu.add_command(label="Help", command = self.show_keybinds)

		#Initialize the layout of the gui using grid()
		self.__hex_box.grid(row = 0, column = 1)
		self.__address_box.grid(row = 0, column = 0, sticky=W)		
		self.__text_box.grid(row = 0, column = 2, sticky=E)

		#If the setting "show kepyad" is set, intialize the keypad and the layout accordingly.
		if int(settings["show_keypad"]) == 1:
			self.__edit_hex_button.grid(row = 0, column = 0, sticky=N+S+E+W)
			nop_replace_button.grid(row = 1, column = 0, sticky=N+S+E+W)
			replace_with_byte_button.grid(row = 2, column = 0, sticky=N+S+E+W)
			self.__offset_entry.grid(row = 2, column = 2, sticky=N+S+E+W, padx=1, pady=4)
			seek_offset_button.grid(row = 2, column = 1, sticky=N+S+E+W, padx=20)
			functions_frame.grid_rowconfigure(0, weight=1)
			functions_frame.grid_rowconfigure(1, weight=1)
			functions_frame.grid_rowconfigure(2, weight=1)

		else:
			self.__edit_hex_button.grid(row = 0, column = 0, sticky=N+S+E+W, pady=4)
			nop_replace_button.grid(row = 0, column = 1, sticky=N+S+E+W, pady=4)
			replace_with_byte_button.grid(row = 0, column = 2, sticky=N+S+E+W, pady=4)
			self.__offset_entry.grid(row = 0, column = 4, sticky=E, padx=1)
			seek_offset_button.grid(row = 0, column = 3, sticky=E, padx=2, pady=4)
			seek_offset_button.config(width=10)	
			self.__offset_entry.config(width=14)
			functions_frame.columnconfigure(3, weight=2)


		self.__status_label.grid(row = 0, column = 0, sticky=W)
		self.__file_name_label.grid(row = 0, column = 1, sticky=W+E)
		label_frame.grid_columnconfigure(1, weight=1000)
		label_frame.grid_columnconfigure(0, weight=1)

		move_up_button.pack()
		self.__scrollbar_slider.pack(expand = 1, fill = BOTH)
		move_down_button.pack(side = BOTTOM)

		self.__hex_box.config(state=DISABLED)
		self.__text_box.config(state=DISABLED)
		self.__address_box.config(state=DISABLED)
		self.__offset_entry.insert(INSERT, '0x00')


		#Initialize some class attributes
		#This variable is None until a file is opened, after which the current file under editing is stored in this variable.
		self.__current_file = None

		#This variable allows navigation of self.__hex_box. Format is [<row>, <column>]
		self.__hex_cursorpos = ['1', '0']

		#This variable is responsible for allowing the user to edit the hex text and update the file.
		#When this is True, the user may change selected characters.
		self.__allow_typing = False

		#Initiate the keypad buttons and keybinds for typing into self.__hex_box, when typing is allowed.
		keychars_list = ["0123", "4567", "89ab", "cdef"]

		for level in range( len(keychars_list) ):
			for index in range( len( keychars_list[level] ) ):		
				self.__mainw.bind( keychars_list[level][index], self.key_press_event )
				Button( keypad_frame, width=settings['keypad_button_width'], bd=5, activebackground="gray", bg=settings['btn_color'],\
						relief=GROOVE, text = keychars_list[level][index].upper(), fg=settings['fg'], \
					    command = lambda char = keychars_list[level][index]: self.type(char) ).grid( column = index, row = level, padx=2, pady=2)

		#Bind all the main functionality
		self.__mainw.bind('j', self.seek_bind_event)
		self.__mainw.bind('k', self.seek_bind_event)
		self.__mainw.bind('J', self.seek_bind_event)
		self.__mainw.bind('K', self.seek_bind_event)
		self.__mainw.bind('<Return>', self.other_binds)
		self.__mainw.bind('<Control-n>', self.other_binds)
		self.__mainw.bind('/', self.other_binds)
		self.__mainw.bind('i', self.hex_edit)
		self.__mainw.bind('r', self.choose_replace_byte)
		self.__mainw.bind('n', self.replace_with_nop)


	def closing_program(self):
		"""
		Attempts to close the opened file and remove the dump file when exiting the program.
		"""
		if self.__current_file:
			self.__current_file.close()

		#Try to clean the directory from unnessessary files.
		try:
			os.remove(f"/tmp/GHE/dump")

		except:
			pass
		self.__mainw.destroy()


	def start_settings_window(self, settings_dict):
		"""
		Initializes the setting window when the user presses "Preferences".

		param: settings dictionary to send to the settings window
		"""
		#settings_changed_succesfully = settings_window.Settings_Window(settings_dict).change_succesful

		#print(settings_changed_succesfully)

		settings_window.Settings_Window(settings_dict, self.__mainw)
		#self.__mainw.destroy()


	def get_settings(self):
		"""
		Initializes the settings dictionary on program start.
		"""
		settings_dict = settings_manager.read_settings_file()

		if settings_dict:
			return settings_dict

		else:
			return DEFAULT_SETTINGS


	def start(self):
		"""
		Starts the program GUI
		"""
		self.__mainw.mainloop()


	def scroll(self, *args):
		"""
		Handles scrolling through the file by getting the scrollbar value, and calling self.update_view().
		Every time the scrollbar value is updated, this function is called.
		"""
		if self.__current_file:
			new_offset = self.__scrollbar_slider.get() * self.__line_size
			self.update_view(new_offset, self.__current_file)


	def seek_offset(self):
		"""
		When the user presses the Seek button, this function validates the address stored in self.__offset_entry
		and updates the scrollbar value to that address. 
		"""

		if self.__current_file:

			new_offset = self.__offset_entry.get()

			#The offset should be hexadecimal and smaller than the file size. Reset the offset entry when an error occurs.
			try:
				new_offset = int(new_offset, 16)

			except ValueError:	
				tkinter.messagebox.showerror('Error','Invalid Offset. Offset must be hexadecimal.\nExample: 0x1234')
				self.__offset_entry.delete('0', END)
				self.__offset_entry.insert(INSERT, '0x00')
				return

			if new_offset > self.__current_file_size:
				tkinter.messagebox.showerror('Error','Offset larger than file')
				self.__offset_entry.delete('0', END)
				self.__offset_entry.insert(INSERT, '0x00')
				return

			#Update the scrollbar value
			self.__scrollbar_slider.set(new_offset / self.__line_size)


	def offset_move(self, amount):
		"""
		Increments or decrements the scrollbar value. 
		"""

		previous_offset = self.__scrollbar_slider.get()
		self.__scrollbar_slider.set(previous_offset + amount)


	def key_press_event(self, event):
		"""
		This function catches a binded key that is meant for typing when one is pressed and sends the key value to self.type()
		"""
		self.type(event.char) 


	def seek_bind_event(self, event):
		"""
		This function catches a binded key that is meant for navigating the view and sends the key value to self.offset_move()
		"""
		if event.char == "j":
			self.offset_move(1)

		elif event.char == "k":
			self.offset_move(-1)

		elif event.char == "J":
			self.offset_move(self.__big_offset_jump)

		elif event.char == "K":
			self.offset_move(-1 * self.__big_offset_jump)


	def other_binds(self, event):
		"""
		This function handles rest of the binds.
		"""

		#Enter for seeking to offset
		if ord(event.char) == 13:
			if self.__offset_entry.get() != '0x00':
				self.seek_offset()

		#Slash for getting focus for the offset Entry
		if event.char == '/':
			self.__offset_entry.delete('0', END)
			self.__offset_entry.focus_set()

		#Ctrl-n for opening files.
		if ord(event.char) == 14:
			self.open_file()

	def show_keybinds(self):



		keybind_prompt = Toplevel(self.__mainw)
		keybind_prompt.title("Keys")
		keybind_prompt.resizable(False, False)

		#Grab the focus from the main window until exiting the editor
		keybind_prompt.grab_set()

		Label(keybind_prompt, text = "j / k to increment the view", width = 28).pack()
		Label(keybind_prompt, text = "J / K to jump 100 bytes (configurable)", width = 28).pack()
		Label(keybind_prompt, text = "/ to seek to offset", width = 28).pack()
		Label(keybind_prompt, text = "n to replace with NOP", width = 28).pack()
		Label(keybind_prompt, text = "r to replace with byte...", width = 28).pack()
		Label(keybind_prompt, text = "i for insert mode", width = 28).pack()
		Label(keybind_prompt, text = "Ctrl + n to open a new file", width = 28).pack()
		Button(keybind_prompt, text="OK", command = lambda: keybind_prompt.destroy(), relief=RIDGE).pack( fill = X)



	def type(self, key):
		"""
		Handles editing the hex view on screen. It retreives the current cursor position and types the parameter key into that position.
		When it finds whitespace, it skips so that the user can not write bad data.
		Again, this only works when self.__allow_typing == True. 

		param: key to be written.
		"""

		def replace_character(position, new_character):
			"""
			Replaces a character in the hex editor box in a given position with a given character.

			param 1: current cursor position in the hex box
			param 2: character to be written
			"""

			#Delete the old character and insert the new character.
			self.__hex_box.delete('.'.join(position))
			self.__hex_box.insert('.'.join(position), new_character)

			#Update the cursor position.
			self.__hex_cursorpos[1] = str(int(position[1]) + 1)


		#Cursor position in tkinter Text() is of format '<row>.<column>', which is why
		#we need to call '.'.join(self.__hex_cursorpos), to get correct coordinates from our coordinate list.
		pos = self.__hex_cursorpos

		if self.__allow_typing == True:
			
			self.__hex_box.config(state=NORMAL)

			while True:		

				#Skip over space
				if self.__hex_box.get('.'.join(pos)) == ' ':
					replace_character(pos, ' ')

				#Skip over new lines and update the line number of the cursor position
				elif self.__hex_box.get('.'.join(pos)) == '\n':
					replace_character(pos, '\n')
					self.__hex_cursorpos[0] = str(int(pos[0]) + 1)
					self.__hex_cursorpos[1] = '0'

				else:
					break

			replace_character(pos, key.upper())
			self.__hex_box.config(state=DISABLED)



	def hex_edit(self, event = None):
		"""
		Responds when the user presses the "Edit Hex/Save Edit" button. After the press, the user may type
		over selected text (if there is any selection and if there exists a file to edit) and the button turns into the "Save Edit" button.
		After the user saves their changes, the program calls update_current_file() and resets the state of the hex box. 
		"""

		if self.__allow_typing == False and self.__current_file:
			
			#If the user has highlighted text
			if self.__hex_box.tag_ranges("sel"):
				
				self.__edit_hex_button.config(text="Save Edit")
				self.__hex_cursorpos = self.__hex_box.index(SEL_FIRST).split('.')
				self.__allow_typing = True

				#Handle the fancy highlihgting over the selected text
				highligth_start = self.__hex_cursorpos
				highligth_stop = self.__hex_box.index(SEL_LAST).split('.')
				self.__hex_box.tag_add("edit_tag", '.'.join(highligth_start), '.'.join(highligth_stop))
				self.__hex_box.tag_config("edit_tag", background="darkblue", foreground="white")

			else:
				return
			

		#When the user presses "Save Edit", reset the state of the hex editor to not allow editing and update the file to show changes.
		else:
			self.__edit_hex_button.config(text="Edit Hex")
			self.__allow_typing = False						
			self.update_current_file()


	def replace_with_byte(self, byte, sel = None, sel_coord = None):
		"""
		This function repeatedly types a given byte over the user highlighted text.

		"""

		self.__allow_typing = True
		self.__hex_box.config(state=NORMAL)

		#If the user has highlighted text
		if len(sel) != 0:

			first_nibble = byte[0]
			second_nibble = byte[1]

			#Get the lenght of the higlighted text, not including whitespace and set the cursor to the beginning of the higlighted text.
			selected_hex_length = len(sel.replace('\n',' ').replace(' ', ''))
			self.__hex_cursorpos = sel_coord

			#Each nibble will be typed alternating through the length of the selected hex
			for index in range(selected_hex_length):
				if index % 2 == 0:
					self.type(first_nibble)
				else:
					self.type(second_nibble)
			
		#Reset the state of the hex editor to not allow editing and update the file to show changes.
		self.__allow_typing = False
		self.__hex_box.config(state=DISABLED)
		self.update_current_file()


	def replace_with_nop(self, event = None):
		"""
		This function repeatedly types a NOP, or no operation instruction over the user highlighted text.
		Really handy for reversing binaries.
		"""
		self.replace_with_byte('90')



	def choose_replace_byte(self, event = None):
		"""
		When the user presses the "Replace With Byte" button, this function creates a pop-up
		window in which they can choose a byte to then be repeatedly typed over the user
		highlighted text with the help of the self.replace_with_byte(byte) function. 
		"""

		def validate_byte(selected_text = None, sel_coord = None):
			"""
			This function validates the user input typed into byte_entry.
			If the input is a valid hexadecimal byte, it will be written over the selected text.
			Bad input clears the entry text.
			"""
			byte = byte_entry.get()
		
			try:
				int(byte, 16)

				if len(byte) == 2:
					byte_entry.delete('0', END)
					byte_prompt.destroy()
					self.replace_with_byte(byte, selected_text, sel_coord)

				else:
					byte_entry.delete('0', END)
					label.config(text = "Error: bad value. Example value: 41")

			except ValueError:
				byte_entry.delete('0', END)
				label.config(text = "Error: bad value. Example value: 41")

		selected_text = self.__hex_box.get(SEL_FIRST, SEL_LAST)
		sel_coord = self.__hex_box.index(SEL_FIRST).split('.')

		#Create the pop-up window
		byte_prompt = Toplevel(self.__mainw)
		byte_prompt.title("Enter Hexadecimal Byte")
		byte_prompt.resizable(False, False)

		#Grab the focus from the main window until exiting the editor
		byte_prompt.grab_set()

		label = Label(byte_prompt, text = "Example value: 41", width = 28)
		byte_entry = Entry(byte_prompt)
		byte_entry.insert(INSERT, '00')
		ok_button = Button(byte_prompt, text="OK", command = lambda text = selected_text, coord = sel_coord: validate_byte(text, sel_coord), relief=RIDGE)

		label.grid(row = 0, column = 0)
		byte_entry.grid(row = 0, column = 1)
		ok_button.grid(row = 1, column = 0, columnspan=2, sticky=W+E)


	def update_view(self, offset, file):
		"""
		This function handles drawing the hex view, the address view and the ascii representation view. 
		It gets an offset and a file as parameters. It then calls draw_editor_view(offset, file, chunk_size, line_size)
		and receives the correctly formatted text to be written to each Text box.

		param: offset in the file to be read
		file: the file to be read.
		"""

		hex_view, address_view, text_view = file_handler.draw_editor_view(offset, file, self.__chunk_size, self.__line_size)

		#Set the states of the text boxes, and replace their text with new text.
		self.__hex_box.config(state=NORMAL)
		self.__text_box.config(state=NORMAL)
		self.__address_box.config(state=NORMAL)

		self.__hex_box.delete(1.0, END)
		self.__text_box.delete(1.0, END)
		self.__address_box.delete(1.0, END)

		self.__hex_box.insert(INSERT, hex_view)
		self.__address_box.insert(INSERT, address_view)
		self.__text_box.insert(INSERT, text_view)

		self.__hex_box.config(state=DISABLED)
		self.__text_box.config(state=DISABLED)
		self.__address_box.config(state=DISABLED)


	def save_changes(self, save_as = False):
		"""
		This function writes the contents of self.__current_file into either a user specified file
		or into the original opened file. After it writes into the file it opens the new file 
		for further editing.
		
		param: True if the user wants to specify a new file name.
		"""

		if self.__current_file:

			if not save_as:
				save_file_path = self.__current_file_path
			else:
				save_file_path = asksaveasfilename()

			try:
				save_file = open(save_file_path, 'wb')
			except OSError:
				tkinter.messagebox.showerror('Error', f'Unable to write to file {save_file_path}\nPlease specify another file name.')
				return

			#If the save file opens, write the contents of the current file into the save file.
			self.__current_file.seek(0)
			save_file.write(self.__current_file.read())
			save_file.close()
			self.__current_file.close()

			#Try to open the now saved file.
			try:
				self.__current_file = open(save_file_path, 'rb')

			except OSError:
				tkinter.messagebox.showerror('Error','Unable to open file ' + save_file_path)
				return

			self.__current_file_path = save_file_path
			self.update_current_file()
			self.__file_name_label.config(text = self.__current_file_path)


	def update_current_file(self):
		"""
		This function handles displaying the edited session. If there is a file, it updates
		self.__current_file into a dump file that contains the edited data for later saving.
		It then updates the program view to show the dumpfile data. This way we don't have
		to write to the save file and display the changes unless the user wants to.
		"""
		if self.__current_file:

			#The dump file is saved into self.__current_file as if the program was editing the original file
			self.__current_file = file_handler.create_dump(self.__scrollbar_slider.get() * self.__line_size, self.__current_file, self.__hex_box.get('1.0', END))

			#Update the view to show the contents of the dump file
			self.update_view(self.__scrollbar_slider.get() * self.__line_size, self.__current_file)


	def open_file(self):
		"""
		Opens a file that the user chose in the askopenfilename() prompt. It then initiates
		the class attributes to show the represented the relevant info of the newly opened file.
		"""
		if self.__current_file:
			self.__current_file.close()

		new_file_path = askopenfilename()

		if new_file_path:

			try:
				self.__current_file = open(new_file_path, 'rb')

			except OSError:
				tkinter.messagebox.showerror('Error','Unable to open file ' + new_file_path)
				return
		
			self.__current_file_path = new_file_path
			self.__current_file_size = os.stat(self.__current_file_path).st_size 
			self.__scrollbar_slider.configure(to = ((self.__current_file_size - self.__line_size) / self.__line_size))
			self.update_view(0, self.__current_file)
			self.__status_label.config(text = 'Highlight text to edit    ')
			self.__file_name_label.config(text = self.__current_file_path)

def main():


	gui = GUI()
	gui.start()
	
if __name__ == "__main__":
	main()
