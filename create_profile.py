#!/bin/python

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import run_command
from variables import wad_dirs, default_config_filename, main_dir, profile_dir
from profile import Profile

class CreateProfileWindow(tk.Toplevel):
    def cancel(self):
        self.destroy()

    def get_listbox_selection(self, val):
        sender = val.widget
        inds   = sender.curselection()

        #values.clear()
        for idx in inds:
            values.append(sender.get(idx))

        return(values)

    def select_profile_name(self):
        profile_name = filedialog.asksaveasfilename(
                defaultextension = '.gzd',
                filetypes        = [('py_gzdoom_launcher profile file', '.gzd')],
                initialdir       = profile_dir,
                title            = 'Profile file'
                )
        self.profile_entry.delete(0, tk.END)
        self.profile_entry.insert(0, profile_name)

    def select_config_filename(self):
        config_filename   = filedialog.asksaveasfilename()
        self.config_file_entry.delete(0, tk.END)
        self.config_file_entry.insert(0, config_filename)

    def create_profile(self):
        selected_iwad = self.iwads_listbox.get(self.iwads_listbox.curselection())
        selected_wads_list = [self.wads_listbox.get(x) for x in self.wads_listbox.curselection()]
        profile_name = self.profile_entry.get()
        config_file = self.config_file_entry.get()
        
        profile = Profile(
                wads = selected_wads_list,
                iwad = selected_iwad,
                config_file = config_file,
                dmflags = 0,
                dmflags2 = 0
                )

        profile_filename = os.path.join(profile_dir, profile_name + '.gzd')

        if os.path.exists(profile_filename):
            messagebox.showerror(
                    title   = 'Profile exists', 
                    message = 'ERROR! Profile {} already exists.'.format(profile_name))
        else:
            print('Generating profile: {}'.format(profile_name))
            print(profile.get_info())
            profile.save(profile_filename)
            messagebox.showinfo(
                    title    = 'Profile created', 
                    message  = 'Profile {} created successfully'.format(profile_name)
                    )

    def __init__(self, parent):
        super().__init__(parent)

        #self = tk.Toplevel(parent)
        self.title('Profile generator')
        self.attributes('-type', 'dialog')
        self.grab_set()
    
        ########################################
        # This frame contains the profile name #
        ########################################
        self.frame_profile = ttk.Frame(
                master = self
                )

        self.profile_label = ttk.Label(
                master = self.frame_profile,
                text   = 'Profile name'
                )

        self.profile_entry = ttk.Entry(
                master = self.frame_profile,
                )

        self.profile_label.pack()
        self.profile_entry.pack(fill = tk.X, expand = True, padx = 5)

        self.frame_profile.pack(fill = tk.X, pady = 5)

        #####################################################################
        # The following frame will contain two horizontally located frames. #
        # One for IWADs and another one for WADs.                           #
        #####################################################################
        self.frame_wads = ttk.Frame(
                master = self, 
                )
 
        # This frame occupies the left portion of the top frame
        # and contains a listbox with the available IWADs
        self.frame_wads_iwads = tk.Frame(
                master = self.frame_wads,
                )
 
        self.frame_wads_iwads.pack(
                fill = tk.BOTH,
                expand = True,
                side = tk.LEFT,
                padx = 5
                )
 
        # Label for the IWAD radiobuttons
        self.label_iwad = ttk.Label(
                master = self.frame_wads_iwads,
                text   = "Choose the IWAD",
                )
 
        self.label_iwad.pack()
 
        # Listbox containing the IWADS
        self.iwads_listbox = tk.Listbox(
                master          = self.frame_wads_iwads, 
                selectmode      = tk.BROWSE, 
                exportselection = False
                )
 
        ## Get the list of available wad files
        wad_list, iwad_list = run_command.get_list_of_wad_files(wad_dirs)

        for n, iwad in enumerate(iwad_list):
            self.iwads_listbox.insert(tk.END, iwad) 
 
        self.iwads_listbox.select_set(0)
        self.iwads_listbox.pack(expand = True, fill = tk.BOTH, padx = 5, pady = (0, 5))

        # Here is the frame with available WADs
        self.frame_wads_wads = tk.Frame(
                master = self.frame_wads,
                )

        self.frame_wads_wads.pack(
                fill = tk.BOTH,
                expand = True,
                side = tk.RIGHT,
                padx = 5
                )

        self.wads_listbox = tk.Listbox(
                master          = self.frame_wads_wads,
                selectmode      = tk.MULTIPLE,
                exportselection = False
                )

        for n, wad in enumerate(wad_list):
            self.wads_listbox.insert(tk.END, wad)

        self.label_wad = ttk.Label(
                master = self.frame_wads_wads,
                text   = "Available WADs",
                )

        self.label_wad.pack()
        self.wads_listbox.pack(expand = True, fill = tk.BOTH, padx = 5, pady = (0, 5))


        self.frame_wads.pack(pady = 5, fill = tk.BOTH, expand = True)

        ###############################################################################
        # This frame lets the user choose the configuration file bound to the profile #
        ###############################################################################
        self.frame_config = tk.Frame(
                master = self,
                )
        self.config_label = ttk.Label(
                master = self.frame_config,
                text   = 'Configuration file'
                )
    
        self.config_file_entry = ttk.Entry(
                master = self.frame_config,
                )
    
        self.config_file_entry.insert(0, default_config_filename)
    
        self.browse_config_button = ttk.Button(
                master  = self.frame_config,
                text    = 'Browse...',
                command = self.select_config_filename
                )
    
        self.config_label.pack()
        self.config_file_entry.pack(side = tk.LEFT, fill = tk.X, expand = True, padx = 5)
        self.browse_config_button.pack(side = tk.RIGHT, padx = 5)

        self.frame_config.pack(fill = tk.X, pady = 5)
    
        #############################################################
        # This frame contains the create profile and cancel buttons #
        #############################################################
        self.frame_buttons = ttk.Frame(
                master = self,
                )

        self.profile_button = ttk.Button(
                master  = self.frame_buttons,
                text    = 'Create profile', 
                command = self.create_profile,
                )

        self.profile_button.pack(side = tk.LEFT, expand = True, fill = tk.X, padx = 5)

        self.cancel_button = ttk.Button(
                master  = self.frame_buttons,
                text    = "Cancel",
                command = lambda: self.cancel()
                )

        self.cancel_button.pack(side = tk.RIGHT, expand = True, fill = tk.X, padx = 5)
        self.frame_buttons.pack(fill = tk.X, pady = 5)

#
## These lists will contain the selected IWAD and WADs
#
#os.makedirs(main_dir, exist_ok = True)
#
#def cancel(window):
#    window.destroy()
#
## Given a listbox, put all the selected items into the values list
#
## Open a dialog to select the profile file
#def profile_file_browser():
#    global profile_entry
#
#
#def create_profile_window(root):
#    ########################################
#    # This frame contains the profile name #
#    ########################################
#    frame_profile = ttk.Frame(
#            master = window
#            )
#
#    profile_label = ttk.Label(
#            master = frame_profile,
#            text   = 'Profile file'
#            )
#
#    profile_entry = ttk.Entry(
#            master = frame_profile,
#            )
#
#    browse_button = ttk.Button(
#            master  = frame_profile,
#            text    = 'Browse...',
#            command = profile_file_browser
#            )
#    browse_button.pack(side = tk.RIGHT, padx = 5)
#
#    profile_label.pack()
#    profile_entry.insert(0, os.path.join(profile_dir, 'default.gzd'))
#    profile_entry.pack(side = tk.LEFT, fill = tk.X, expand = True, padx = 5)
#
#    #########################################################
#    # This frame occupies the left portion of the top frame #
#    # and contains a listbox with the available WADs        #
#    #########################################################
#
#    ##################################################
#    # These frames contain the buttons at the bottom #
#    ##################################################
#
#    frame_buttons = ttk.Frame(
#            master = window,
#            )
#
#    profile_button = ttk.Button(
#            master  = frame_buttons,
#            text    = 'Create profile', 
#            command = create_profile,
#            )
#
#    profile_button.pack(side = tk.LEFT, expand = True, fill = tk.X, padx = 5)
#
#    cancel_button = ttk.Button(
#            master  = frame_buttons,
#            text    = "Cancel",
#            command = lambda: cancel(window)
#            )
#
#    cancel_button.pack(side = tk.RIGHT, expand = True, fill = tk.X, padx = 5)
#
#    frame_profile.pack(fill = tk.X, pady = 5)
#    frame_wads.pack(pady = 5, fill = tk.BOTH, expand = True
#        )
#
#    return window
#
