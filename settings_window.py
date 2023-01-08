#!/usr/bin/env python3

from tkinter import * 
import settings_manager, GHE
import tkinter.messagebox


class Settings_Window(): 

	def __init__(self, settings, parent_window):
		"""
		Initializes the settings window class. It takes the previous settings and the main window as an argument.
		It then displays various widgets that allow the user to specify their settigns and save them.

		param1: settings dictionary
		param2: parent window
		"""

		#Configure the settings window
		self.__settings_window = Toplevel()
		self.__settings_window.title("This is title Name")
		self.__settings_window.grab_set()
		self.__settings_window.configure(bg='gray30')
		self.__settings_window.resizable(False, False)
		
		self.__parent = parent_window
		self.__old_settings = settings

		#Create frames for the widgets
		color_scheme_frame = Frame(self.__settings_window, bg="gray70")
		show_keypad_frame = Frame(self.__settings_window, bg="gray60")
		size_frame = Frame(self.__settings_window, bg="gray80")

		#Initiate the variables for the radiobuttons
		self.__color_scheme = StringVar()
		self.__color_scheme.set(self.__old_settings['color_scheme'])

		self.__show_keypad = IntVar()
		self.__show_keypad.set(self.__old_settings['show_keypad'])

		self.__line_size_value = IntVar()
		self.__line_size_value.set(int(self.__old_settings['line_size']))

		self.__chunk_size_value = IntVar()
		self.__chunk_size_value.set(int(self.__old_settings['chunk_size']))


		#Create various widgets
		default_scheme = Radiobutton(color_scheme_frame, text="Default Color Scheme", variable=self.__color_scheme, value='default', bg="gray70")
		dark_scheme_1 = Radiobutton(color_scheme_frame, text="Dark Green Scheme", variable=self.__color_scheme, value='dark_1', bg="gray70")
		dark_scheme_2 = Radiobutton(color_scheme_frame, text="Dark Blue Scheme", variable=self.__color_scheme, value='dark_2', bg="gray70")

		show_keypad = Radiobutton(show_keypad_frame, text="True ", variable=self.__show_keypad, value=1, bg="gray60")
		dont_show_keypad = Radiobutton(show_keypad_frame, text="False", variable=self.__show_keypad, value=0, bg="gray60")

		line_size_menu = OptionMenu(size_frame, self.__line_size_value, 16, 24, 32, 56)
		line_size_menu.configure(bd=0, bg="gray80")
		chunk_size_menu = OptionMenu(size_frame, self.__chunk_size_value, 1, 2, 4, 8)
		chunk_size_menu.configure(bd=0, bg="gray80")

		save_changes_button = Button(self.__settings_window, text="Save Changes", command = self.save_changes, bg='white')
		discard_changes_button = Button(self.__settings_window, text="Discard Changes", command = lambda: self.__settings_window.destroy(), bg='white')

		#Layout creation and labels
		Label(show_keypad_frame, text="Enable keypad:", bg="gray60").grid(row = 0, column = 0)
		Label(color_scheme_frame, text="Color scheme:", bg="gray70").grid(row = 0, column = 0)
		Label(size_frame, text="Hex editor line size in bytes:", bg="gray80").grid(row = 0, column = 0)
		Label(size_frame, text="Hex editor chunk size in bytes:", bg="gray80").grid(row = 1, column = 0)

		show_keypad_frame.grid(row = 0, column = 0, sticky=N+S)
		show_keypad.grid(row = 0, column = 1, sticky=W)
		dont_show_keypad.grid(row = 1, column = 1)

		color_scheme_frame.grid(row = 0, column = 1)
		default_scheme.grid(row = 0, column = 1)
		dark_scheme_1.grid(row = 1, column = 1, sticky=W)
		dark_scheme_2.grid(row = 2, column = 1, sticky=W)

		size_frame.grid(row = 0, column = 2, sticky=N+S)
		line_size_menu.grid(row = 0, column = 1)
		chunk_size_menu.grid(row = 1, column = 1, sticky=W+E)

		save_changes_button.grid(row = 1, column = 1, sticky=W, pady=4)
		discard_changes_button.grid(row = 1, column = 0, sticky=E, pady=4, padx=4)



	def save_changes(self):
		"""
		When the user presses the save changes button, this function is called.
		This program gets the user specified settigns values from the vidgets and creates a new settings dictionary with them.
		Then the dictionary is sent to settings_manager.save_settings() to be saved to the settings.cfg file.
		"""

		new_settings = {}
		new_settings['chunk_size'] = self.__chunk_size_value.get()
		new_settings['line_size'] = self.__line_size_value.get()
		new_settings['color_scheme'] = self.__color_scheme.get()
		new_settings['show_keypad'] = self.__show_keypad.get()
		new_settings["jump_size"] = self.__old_settings["jump_size"]

		flag = settings_manager.save_settings(new_settings)

		if flag:
			tkinter.messagebox.showerror('Error','Unable to save changes.')
		else:
			self.__settings_window.destroy()

			#Restart the program flow if the user wants to restart.
			answer = messagebox.askquestion('Restart Required', 'Do you want to restart the program for the changes to take effect?')
			if answer == 'yes':
				self.__parent.destroy()
				GHE.main()
