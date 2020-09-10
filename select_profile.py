import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from variables import profile_dir
from create_profile import CreateProfileWindow
from run_command import backup_profile, detect_profiles

class ProfileListbox(tk.Listbox):
    def update(self):
        self.delete(0, tk.END)
        profile_names = detect_profiles()
        for profile_name in profile_names:
            self.insert(tk.END, profile_name)
        self.select_set(0)

    def __init__(self, parent):
        super().__init__(
                master          = parent,
                selectmode      = tk.BROWSE,
                exportselection = False
                )

        self.update()

class SelectProfileWindow(tk.Tk):
    def handle_exit(self, event):
        quit()

    def delete_profile(self):
        profile_name = self.profile_listbox.get(tk.ACTIVE)

        backup_profile(profile_name)
        self.profile_listbox.delete(tk.ACTIVE)

    def edit_profile(self):
        messagebox.showerror(
                title = 'ERROR!',
                message = 'Work in progress'
                )

    def launch_create_window(self):
        window = CreateProfileWindow(self)

    def run_gzdoom(self):
        messagebox.showerror(
                title = 'ERROR!',
                message = 'Work in progress'
                )
        # If the user let the default, we have to generate a ListboxSelect event to use the default
        # value.
        #command = 'gzdoom' 
        #for wad in selected_wads_list:
        #    command += ' -file {}'.format(wad)

        #iwad_name = selected_iwads_list[0]
        #command += ' -iwad {}'.format(iwad_name)

        #config_filename = config_file_entry.get()
        #command += ' -config {}'.format(config_filename)

        #window.destroy()

        #print('Running gzdoom with the following command...')
        #print(command)
        #os.system(command)


    def __init__(self):
        super().__init__()

        self.title('GZDoom launcher')
        self.attributes('-type', 'dialog')
        self.grab_set()
        self.bind('<Control-q>', self.handle_exit)

        #####################################################################
        # This frame will contain a listbox with all the available profiles #
        # to the left and a bunch of buttons to the right                   #
        #####################################################################

        self.upper_frame = ttk.Frame(
                master = self
                )

        self.profile_listbox = ProfileListbox(self.upper_frame)

        self.profile_listbox.pack(
                side   = tk.LEFT,
                fill   = tk.BOTH,
                expand = True, 
                padx   = 5,
                pady   = 5
                )

        self.buttons_frame = ttk.Frame(
                master = self.upper_frame,
                )
        self.buttons_frame.pack(padx = 5, pady = 5)

        self.new_button = ttk.Button(
                master  = self.buttons_frame,
                text    = 'New...',
                command = self.launch_create_window
                )

        self.new_button.pack(pady = (0, 5))

        self.edit_button = ttk.Button(
                master  = self.buttons_frame,
                text    = 'Edit',
                command = self.edit_profile,
                )

        self.edit_button.pack(pady = (0, 5))

        self.delete_button = ttk.Button(
                master  = self.buttons_frame,
                text    = 'Delete',
                command = self.delete_profile,
                )

        self.delete_button.pack(pady = (0, 5))

        self.commands_frame = ttk.Frame(
                master = self
                )

        self.run_button = ttk.Button(
                master  = self.commands_frame,
                text    = 'Run gzdoom', 
                command = self.run_gzdoom
                )

        self.run_button.pack(side = tk.LEFT, expand = True, fill = tk.X, padx = 5)

        self.exit_button = ttk.Button(
                master  = self.commands_frame,
                text    = "Exit",
                command = exit
                )

        self.exit_button.pack(side = tk.RIGHT, expand = True, fill = tk.X, padx = 5)

        self.upper_frame.pack(fill = tk.BOTH, expand = True)
        self.commands_frame.pack(padx = 5, pady = 5)

# Get list of available profiles

# ---------------------------------------------------------------------------------------------------
