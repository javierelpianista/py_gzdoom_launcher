#!/bin/python

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import glob
from py_gzdoom_launcher.create_profile import CreateProfileWindow
from py_gzdoom_launcher.select_profile import SelectProfileWindow
from py_gzdoom_launcher.configure_window import ConfigureWindow
from py_gzdoom_launcher import variables

configuration_file = variables.variables['configuration_file']

def main():
    found = os.path.exists(configuration_file)

    if not found:
        print('Configuration file {} not found. Creating one with default values...'.format(configuration_file))
        variables.set_defaults()
        variables.write_config()
    else:
        variables.read_config(configuration_file)

    main_window = SelectProfileWindow(found)
    tk.mainloop()

if __name__ == '__main__':
    main()
