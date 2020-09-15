import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
from py_gzdoom_launcher import variables
from py_gzdoom_launcher.create_profile import CreateProfileWindow
from py_gzdoom_launcher.configure_window import ConfigureWindow
from py_gzdoom_launcher.run_command import backup_profile, detect_profiles
from py_gzdoom_launcher.profile import Profile

class ProfileListbox(tk.Listbox):
    def update(self):
        self.delete(0, tk.END)
        try:
            profile_names = detect_profiles()
            for profile_name in profile_names:
                self.insert(tk.END, profile_name)
            self.select_set(0)
        except:
            print('detect_profiles() failed')
            pass

    def __init__(self, parent):
        super().__init__(
                master          = parent,
                selectmode      = tk.BROWSE,
                exportselection = False
                )

        self.update()

class SelectProfileWindow(tk.Tk):
    def handle_exit(self, event = None):
        quit()

    def delete_profile(self):
        profile_name = self.profile_listbox.get(tk.ACTIVE)

        backup_profile(profile_name)
        self.profile_listbox.delete(tk.ACTIVE)

    def edit_profile(self):
        profile_name = self.profile_listbox.get(tk.ACTIVE)

        CreateProfileWindow(self, profile_name)

    def launch_create_window(self):
        CreateProfileWindow(self)

    def launch_configure_window(self):
        if not variables.variables['set']: 
            variables.set_defaults()

        ConfigureWindow(self)

    def run_gzdoom(self):
        profile_name = self.profile_listbox.get(tk.ACTIVE)
        profile_filename = os.path.join(variables.variables['profile_dir'], profile_name + '.gzd')
        profile = Profile.from_file(profile_filename)

        command = variables.variables['executable']
        command += ' -iwad {}'.format(profile.iwad)

        for wad in profile.wads:
            command += ' -file {}'.format(os.path.join(variables.variables['wad_dirs'], wad))

        command += ' -config {}'.format(profile.config_file)
        command += ' +set dmflags {} +set dmflags2 {}'.format(profile.dmflags, profile.dmflags2)

        print('Running gzdoom with the following command...')
        print(command)

        os.system(command)
        quit()

    def copy_profile(self):
        profile_name = self.profile_listbox.get(tk.ACTIVE)

        new_profile_name = simpledialog.askstring(
                parent  = self,
                title   = 'Copy profile',
                prompt  = 'New profile name: '
                )

        copy_config = messagebox.askyesno(
                master = self,
                title  = "Copy profile",
                message = 'Copy configuration file?'
                )

        profile = Profile.from_name(profile_name)
        profile.copy(new_profile_name, copy_config = copy_config)
        self.profile_listbox.update()

    def launch_about_window(self):
        tk.messagebox.showinfo(
                title   = 'About',
                message = 'Written by Javier Garcia\njavier.garcia.tw@hotmail.com'
                )

    def update(self, event = None):
        self.profile_listbox.update()

    def populate(self):
        #################################
        # Here we configure the menubar #
        #################################

        self.menubar = tk.Menu(self)
        self.config(menu = self.menubar)

        # File menu
        self.filemenu = tk.Menu(self.menubar, tearoff=0)
        self.filemenu.add_command(label = 'New profile...', command = self.launch_create_window)
        self.filemenu.add_separator()
        self.filemenu.add_command(
                label = 'Quit', 
                command = self.handle_exit,
                accelerator = 'Ctrl+Q'
                )
        self.menubar.add_cascade(label = 'File', menu = self.filemenu)

        # Options menu
        self.optionsmenu = tk.Menu(self.menubar, tearoff = 0)
        self.optionsmenu.add_command(label = 'Configure...', command = self.launch_configure_window)
        self.menubar.add_cascade(label = 'Options', menu = self.optionsmenu)

        # Help menu
        self.helpmenu = tk.Menu(self.menubar, tearoff = 0)
        self.helpmenu.add_command(label = 'About...', command = self.launch_about_window)
        self.menubar.add_cascade(label = 'Help', menu = self.helpmenu)

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

        self.copy_button = ttk.Button(
                master  = self.buttons_frame,
                text    = 'Copy',
                command = self.copy_profile
                )

        self.copy_button.pack(pady = (0, 5))

        self.delete_button = ttk.Button(
                master  = self.buttons_frame,
                text    = 'Delete',
                command = self.delete_profile,
                )

        self.delete_button.pack(pady = (0, 5))

        self.separator = ttk.Separator(
                master = self.buttons_frame,
                orient = tk.HORIZONTAL,
                )

        self.separator.pack(
                pady   = 5,
                fill   = tk.X,
                expand = True )

        self.button_refresh = ttk.Button(
                master  = self.buttons_frame,
                text    = 'Refresh',
                command = self.update
                )

        self.button_refresh.pack(pady = (0,5))

        ################################################
        # This frame contains the run and exit buttons #
        ################################################

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

    def __init__(self, found = True):
        super().__init__()

        self.title('GZDoom launcher')
        if os.name != 'nt':
            self.attributes('-type', 'dialog')
        self.grab_set()

        self.bind('<Control-q>', self.handle_exit)

        if not found:
            messagebox.showinfo(
                    title = 'First time?',
                    message = 'It looks like it is the first time you are running py_gzdoom_launcher. Please set the configuration with Options/Configure...'
                    )

        self.populate()

