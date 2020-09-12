#!/bin/python

import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import glob
from create_profile import CreateProfileWindow
from select_profile import SelectProfileWindow
from configure_window import ConfigureWindow
import variables

# These two will be set up by the installer
configuration_file = variables.variables['configuration_file']

main_window = tk.Tk()
main_window.withdraw()

if not os.path.exists(configuration_file):
    variables.set_defaults(main_dir, configuration_file)
    messagebox.showinfo(
            parent  = main_window, 
            message = 'It looks like it your first time running py_gzdoom_launcher.\nShowing the configuration window.'
            )

    ConfigureWindow(main_window)
    SelectProfileWindow(main_window)
else:
    variables.read_config(configuration_file)
    SelectProfileWindow(main_window)

tk.mainloop()
