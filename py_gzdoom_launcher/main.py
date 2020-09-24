#!/bin/python

import os
import tkinter as tk
import sys
from tkinter import ttk, filedialog, messagebox
import glob
from py_gzdoom_launcher.create_profile import CreateProfileWindow
from py_gzdoom_launcher.select_profile import SelectProfileWindow
from py_gzdoom_launcher.configure_window import ConfigureWindow
from py_gzdoom_launcher.run_command import launch_gzdoom, detect_profiles
from py_gzdoom_launcher import variables
from py_gzdoom_launcher.profile import Profile

configuration_file = variables.variables['configuration_file']

def init():
    found = os.path.exists(configuration_file)

    if not found:
        print('Configuration file {} not found. Creating one with default values...'.format(configuration_file))
        variables.set_defaults()
        variables.write_config()
    else:
        variables.read_config(configuration_file)

def main(args):
    init()

    main_window = SelectProfileWindow(found)
    tk.mainloop()

def help_run_profile():
    options = {
            '<profile_name>' : 'to run the selected profile',
            '--list'         : 'to list available profiles',
            '--help'         : 'to prompt this message'
            }

    field_length = max([len(x) for x in options])
    fmt_str = '{:' + str(field_length) + '} :    {}'

    print('Usage: pygzld-run [option]')
    print('The available options are:')
    for key, val in options.items():
        print(fmt_str.format(key, val))

    quit()

def run_profile():
    init()
    args = sys.argv

    if len(args) < 2:
        help_run_profile()
    else:
        profile_names = detect_profiles()
        if args[1] == '--list':
            print('Available profiles: ')
            print('--------------------')
            for name in profile_names:
                print('  ' + name)

            quit()
        elif args[1] == '--help':
            help_run_profile()
        else:
            profile_name = args[1]

        if not profile_name in profile_names: 
            msg = ", ".join(profile_names)
            print('Profile {} not detected.'.format(profile_name))
            print('Available profiles are: ' + msg)
            quit()
        else:
            profile_filename = os.path.join(variables.variables['profile_dir'], profile_name + '.gzd')
            profile = Profile.from_file(profile_filename)
            launch_gzdoom(profile)

if __name__ == '__main__':
    main()
