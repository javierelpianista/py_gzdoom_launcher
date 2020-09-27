#!/bin/python

import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import os
from py_gzdoom_launcher import run_command
from py_gzdoom_launcher import variables
from py_gzdoom_launcher.profile import Profile
from py_gzdoom_launcher.gameplay_options import get_flags

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

    def read_profile(self):
        self.profile_entry.insert(0, self.profile.name)

        #items = list(self.wads_listbox.get(0, tk.END))
        for wad in self.profile.wads:
            self.wads_listbox.insert(tk.END, wad)

        self.iwads_listbox.selection_clear(0, tk.END)
        items = list(self.iwads_listbox.get(0, tk.END))
        ind = items.index(self.profile.iwad)
        self.iwads_listbox.select_set(ind)

        self.dmflags1_entry.insert(0, self.profile.dmflags)
        self.dmflags2_entry.insert(0, self.profile.dmflags2)

    def save_profile(self, parent):
        selected_iwad = self.iwads_listbox.get(self.iwads_listbox.curselection())
        selected_wads_list = [self.wads_listbox.get(x) for x in self.wads_listbox.curselection()]
        profile_name = self.profile_entry.get()
        config_file = os.path.join(variables.variables['config_dir'], profile_name + '.ini')
        os.makedirs(variables.variables['config_dir'], exist_ok = True)
        
        profile = Profile(
                name = profile_name, 
                wads = self.wads_listbox.get(0, tk.END),
                iwad = selected_iwad,
                config_file = config_file,
                dmflags = self.dmflags1_entry.get(),
                dmflags2 = self.dmflags2_entry.get()
                )

        profile_filename = os.path.join(variables.variables['profile_dir'], profile_name + '.gzd')
        os.makedirs(variables.variables['profile_dir'], exist_ok = True)

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
                    title    = 'Profile saved', 
                    message  = 'Profile {} saved successfully'.format(profile_name)
                    )
            # Update the parent's listbox with the new profile
            parent.profile_listbox.update()

    def set_flags(self, kind):
        if kind == 'dmflags':
            result = get_flags(
                    self, 
                    initial_flag_value = int(self.dmflags1_entry.get()),
                    kind = 'dmflags' 
                    )

            self.dmflags1_entry.delete(0, tk.END)
            self.dmflags1_entry.insert(0, str(result))

        elif kind == 'dmflags2':
            result = get_flags(
                    self, 
                    initial_flag_value = int(self.dmflags2_entry.get()),
                    kind = 'dmflags2' 
                    )

            self.dmflags2_entry.delete(0, tk.END)
            self.dmflags2_entry.insert(0, str(result))

    def add_files(self):
        files = filedialog.askopenfilenames(
                initialdir = variables.variables['wad_dirs']
                )

        already_there = self.wads_listbox.get(0, tk.END)
        for fname in files:
            if not fname in already_there:
                self.wads_listbox.insert(tk.END, fname)

    def remove_file(self):
        ind = self.wads_listbox.curselection()
        self.wads_listbox.delete(ind)

    def move(self, where):
        if where == 'down': 
            delta = 1
        elif where == 'up':
            delta = -1

        ind = self.wads_listbox.curselection()
        name = self.wads_listbox.get(ind)
        self.wads_listbox.delete(ind)
        new_ind = ind[0] + delta
        new_ind = max(new_ind, 0)
        new_ind = min(new_ind, self.wads_listbox.size())
        self.wads_listbox.insert(new_ind, name)
        self.wads_listbox.select_clear(0, tk.END)
        self.wads_listbox.select_set(new_ind)

    def __init__(self, parent, profile_name = None):
        super().__init__(
                master = parent
                )

        self.title('Create/Edit profile')
        if not os.name == 'nt':
            self.attributes('-type', 'dialog')
        self.grab_set()

        if profile_name:
            self.profile = Profile.from_file(
                    os.path.join(variables.variables['profile_dir'], profile_name + '.gzd')
                    )
        else:
            self.profile = Profile.default()

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

        self.frame_profile.pack(fill = tk.X, padx = 5, pady = 5)

        #####################################################################
        # The following frame will contain two horizontally located frames. #
        # One for IWADs and another one the gameplay options                #
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

        ##########################################################
        # This frame has the options to set dmflags and dmflags2 #
        ##########################################################
        self.frame_dmflags = tk.Frame(
                master = self.frame_wads,
                )

        self.frame_dmflags1 = tk.Frame(
                master = self.frame_dmflags,
                )

        self.dmflags1_label = ttk.Label(
                master = self.frame_dmflags1,
                text   = 'dmflags', 
                anchor = 'c'
                )
    
        self.dmflags1_entry = ttk.Entry(
                master = self.frame_dmflags1,
                width  = 14
                )

        self.dmflags1_button = ttk.Button(
                master = self.frame_dmflags1,
                text   = 'Generate',
                command = lambda : self.set_flags('dmflags')
                )

        self.dmflags1_label.pack(fill = tk.X)
        self.dmflags1_entry.pack(side = tk.LEFT, fill = tk.X, padx = 5)
        self.dmflags1_button.pack(side = tk.RIGHT, fill = tk.X, padx = 5)
        self.frame_dmflags1.pack(fill = tk.X, expand = True, padx = 5)
    
        self.frame_dmflags2 = tk.Frame(
                master = self.frame_dmflags,
                )

        self.dmflags2_label = ttk.Label(
                master = self.frame_dmflags2,
                text   = 'dmflags2',
                anchor = 'c'
                )
    
        self.dmflags2_entry = ttk.Entry(
                master = self.frame_dmflags2,
                width  = 14
                )

        self.dmflags2_button = ttk.Button(
                master  = self.frame_dmflags2,
                text    = 'Generate',
                command = lambda : self.set_flags('dmflags2')
                )

        self.dmflags2_label.pack(fill = tk.X)
        self.dmflags2_entry.pack(side = tk.LEFT, fill = tk.X, padx = 5)
        self.dmflags2_button.pack(side = tk.RIGHT, fill = tk.X, padx = 5)
        self.frame_dmflags2.pack(fill = tk.X, expand = True, padx = 5)

        self.dmflags2_label.pack()
        self.dmflags2_entry.pack()
    
        self.frame_dmflags.pack(fill = tk.X, pady = 5)

        #Here we pack the frame with the IWADs and dmflags
        self.frame_wads.pack(pady = 5, fill = tk.BOTH, expand = True)
    
        #########################################
        # Here is the frame with available WADs #
        #########################################
        self.frame_wads_wads = tk.Frame(
                master = self,
                )

        self.frame_wads_wads.pack(
                fill = tk.BOTH,
                expand = True,
                padx = 5
                )

        self.wads_listbox = tk.Listbox(
                master          = self.frame_wads_wads,
                selectmode      = tk.SINGLE,
                exportselection = False, 
                width           = 40
                )

        #for n, wad in enumerate(wad_list):
        #    self.wads_listbox.insert(tk.END, wad)

        self.label_wad = ttk.Label(
                master = self.frame_wads_wads,
                text   = "Additional files",
                )

        self.frame_wads_buttons = ttk.Frame(
                master = self.frame_wads_wads
                )

        self.button_add_wad = ttk.Button(
                master  = self.frame_wads_buttons,
                text    = 'Add...', 
                command = self.add_files
                )

        self.button_up = ttk.Button(
                master  = self.frame_wads_buttons,
                text    = '⬆️',
                command = lambda: self.move('up'),
                )

        self.button_down = ttk.Button(
                master  = self.frame_wads_buttons,
                text    = '⬇️',
                command = lambda: self.move('down')
                )
                
        self.button_remove_wad = ttk.Button(
                master  = self.frame_wads_buttons,
                text    = 'Remove',
                command = self.remove_file
                )

        self.label_wad.pack()

        self.wads_listbox.pack(
                expand = True, 
                fill = tk.BOTH, 
                side = tk.LEFT,
                padx = 5, 
                pady = (0, 5)
                )
        self.button_add_wad.pack(pady = 5)
        self.button_up.pack(pady = 5)
        self.button_down.pack(pady = 5)
        self.button_remove_wad.pack(pady = 5)
        self.frame_wads_buttons.pack()

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
