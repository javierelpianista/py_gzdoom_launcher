#!/bin/python

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
import run_command
import variables
from profile import Profile

class CreateProfileWindow(tk.Toplevel):
    def cancel(self):
        self.destroy()

    def select_profile_name(self):
        profile_name = filedialog.asksaveasfilename(
                defaultextension = '.gzd',
                filetypes        = [('py_gzdoom_launcher profile file', '.gzd')],
                initialdir       = profile_dir,
                title            = 'Profile file'
                )
        self.profile_entry.delete(0, tk.END)
        self.profile_entry.insert(0, profile_name)

    # Update this window to reflect the properties of the edited profile
    def read_profile(self):
        self.profile_entry.insert(0, self.profile.name)

        items = list(self.wads_listbox.get(0, tk.END))
        for wad in self.profile.wads:
            ind = items.index(wad)
            self.wads_listbox.select_set(ind)

        self.iwads_listbox.selection_clear(0, tk.END)
        items = list(self.iwads_listbox.get(0, tk.END))
        ind = items.index(self.profile.iwad)
        self.iwads_listbox.select_set(ind)

        self.dmflags1_entry.insert(0, self.profile.dmflags)
        self.dmflags2_entry.insert(0, self.profile.dmflags2)

    def select_config_filename(self):
        config_filename   = filedialog.asksaveasfilename()
        self.config_file_entry.delete(0, tk.END)
        self.config_file_entry.insert(0, config_filename)

    def save_profile(self, parent):
        selected_iwad = self.iwads_listbox.get(self.iwads_listbox.curselection())
        selected_wads_list = [self.wads_listbox.get(x) for x in self.wads_listbox.curselection()]
        profile_name = self.profile_entry.get()
        config_file = os.path.join(variables.variables['config_dir'], profile_name + '.ini')
        
        profile = Profile(
                name = profile_name, 
                wads = selected_wads_list,
                iwad = selected_iwad,
                config_file = config_file,
                dmflags = self.dmflags1_entry.get(),
                dmflags2 = self.dmflags2_entry.get()
                )

        profile_filename = os.path.join(variables.variables['profile_dir'], profile_name + '.gzd')

        ans = True
        if os.path.exists(profile_filename):
            ans = messagebox.askyesno(
                    title   = 'Profile exists', 
                    message = 'WARNING! Profile {} exists. Continue?'.format(profile_name)
                    )

        if ans:
            print('Generating profile: {}'.format(profile_name))
            print(profile.get_info())
            profile.save(profile_filename)
            messagebox.showinfo(
                    title    = 'Profile created', 
                    message  = 'Profile {} created successfully'.format(profile_name)
                    )
            # Update the parent's listbox with the new profile
            parent.profile_listbox.update()

    def __init__(self, parent, profile_name = None):
        super().__init__(
                master = parent
                )

        if profile_name:
            self.profile = Profile.from_file(
                    os.path.join(variables.variables['profile_dir'], profile_name + '.gzd')
                    )
        else:
            self.profile = Profile.default()

        self.title('Create/Edit profile')
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
        wad_list, iwad_list = run_command.get_list_of_wad_files(variables.variables['wad_dirs'])

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

        ##########################################################
        # This frame has the options to set dmflags and dmflags2 #
        ##########################################################
        self.frame_dmflags = tk.Frame(
                master = self,
                )

        self.frame_dmflags1 = tk.Frame(
                master = self.frame_dmflags,
                )

        self.dmflags1_label = ttk.Label(
                master = self.frame_dmflags1,
                text   = 'dmflags'
                )
    
        self.dmflags1_entry = ttk.Entry(
                master = self.frame_dmflags1,
                )

        self.dmflags1_label.pack()
        self.dmflags1_entry.pack(fill = tk.X, expand = True)
        self.frame_dmflags1.pack(side = tk.LEFT, fill = tk.X, expand = True, padx = 5)
    
        self.frame_dmflags2 = tk.Frame(
                master = self.frame_dmflags,
                )

        self.dmflags2_label = ttk.Label(
                master = self.frame_dmflags2,
                text   = 'dmflags2'
                )
    
        self.dmflags2_entry = ttk.Entry(
                master = self.frame_dmflags2,
                )

        self.dmflags2_label.pack()
        self.dmflags2_entry.pack(fill = tk.X, expand = True)
        self.frame_dmflags2.pack(side = tk.RIGHT, fill = tk.X, expand = True, padx = 5)

        self.dmflags2_label.pack()
        self.dmflags2_entry.pack()
    
        self.frame_dmflags.pack(fill = tk.X, pady = 5)
    
        #############################################################
        # This frame contains the create profile and cancel buttons #
        #############################################################
        self.frame_buttons = ttk.Frame(
                master = self,
                )

        self.profile_button = ttk.Button(
                master  = self.frame_buttons,
                text    = 'Save profile', 
                command = lambda: self.save_profile(parent),
                )

        self.profile_button.pack(side = tk.LEFT, expand = True, fill = tk.X, padx = 5)

        self.back_button = ttk.Button(
                master  = self.frame_buttons,
                text    = "Back",
                command = lambda: self.cancel()
                )

        self.back_button.pack(side = tk.RIGHT, expand = True, fill = tk.X, padx = 5)
        self.frame_buttons.pack(fill = tk.X, pady = 5)

        self.read_profile()
