import tkinter as tk
from tkinter import ttk 
from tkinter import filedialog
import os
import run_command
from variables import wad_dirs, default_config_filename

# Get the list of available wad files
wad_list, iwad_list = run_command.get_list_of_wad_files(wad_dirs)

# These lists will contain the selected IWAD and WADs
selected_wads_list  = []
selected_iwads_list = []

def run(window):
    # If the user let the default, we have to generate a ListboxSelect event to use the default
    # value.
    if not selected_iwads_list:
        iwads_listbox.event_generate('<<ListboxSelect>>')

    command = 'gzdoom' 
    for wad in selected_wads_list:
        command += ' -file {}'.format(wad)

    iwad_name = selected_iwads_list[0]
    command += ' -iwad {}'.format(iwad_name)

    config_filename = config_file_entry.get()
    command += ' -config {}'.format(config_filename)

    window.destroy()

    print('Running gzdoom with the following command...')
    print(command)
    os.system(command)

def handle_exit(event):
    exit()

def exit():
    quit()

# Given a listbox, put all the selected items into the values list
def get_listbox_selection(val, values):
    sender = val.widget
    inds   = sender.curselection()

    values.clear()
    for idx in inds:
        values.append(sender.get(idx))

window = tk.Tk()
window.title('GZDoom launcher')
window.bind('<Control-q>', handle_exit)

window.style = ttk.Style()
window.style.theme_use('default')

# This frame contains the options for WADs and IWADs.
frame_wads = ttk.Frame(
        master = window, 
        )

# This frame occupies the left portion of the top frame
# and contains a listbox with the available IWADs
frame_wads_iwads = tk.Frame(
        master = frame_wads,
        )

frame_wads_iwads.pack(
        fill = tk.BOTH,
        expand = True,
        side = tk.LEFT,
        padx = 5
        #expand = True,
        )

# Label for the IWAD radiobuttons
label_iwad = ttk.Label(
        master = frame_wads_iwads,
        text   = "Choose the IWAD",
        )

label_iwad.pack()

# Listbox containing the IWADS
iwads_listbox = tk.Listbox(
        master          = frame_wads_iwads, 
        selectmode      = tk.BROWSE, 
        exportselection = False
        )

for n, iwad in enumerate(iwad_list):
    iwads_listbox.insert(tk.END, iwad) 

iwads_listbox.bind('<<ListboxSelect>>', lambda x: get_listbox_selection(x, selected_iwads_list))
iwads_listbox.select_set(0)
iwads_listbox.pack(expand = True, fill = tk.BOTH, padx = 5, pady = (0, 5))

# This frame occupies the left portion of the top frame
# and contains a listbox with the available WADs
frame_wads_wads = tk.Frame(
        master = frame_wads,
        )

frame_wads_wads.pack(
        fill = tk.BOTH,
        expand = True,
        side = tk.RIGHT,
        padx = 5
        )

wads_listbox = tk.Listbox(
        master          = frame_wads_wads,
        selectmode      = tk.MULTIPLE,
        exportselection = False
        )

for n, wad in enumerate(wad_list):
    wads_listbox.insert(tk.END, wad)

label_wad = ttk.Label(
        master = frame_wads_wads,
        text   = "Available WADs",
        )

label_wad.pack()
wads_listbox.bind('<<ListboxSelect>>', lambda x: get_listbox_selection(x, selected_wads_list))
wads_listbox.pack(expand = True, fill = tk.BOTH, padx = 5, pady = (0, 5))

##############################################
# Options related to the configuration files #
##############################################

frame_config = tk.Frame(
        master = window,
        )
config_label = ttk.Label(
        master = frame_config,
        text   = 'Configuration file'
        )

def config_file_browser():
    global config_file_entry

    config_filename   = filedialog.asksaveasfilename()
    config_file_entry.delete(0, tk.END)
    config_file_entry.insert(0, config_filename)

config_file_entry = ttk.Entry(
        master = frame_config,
        )

config_file_entry.insert(0, default_config_filename)

browse_button = ttk.Button(
        master  = frame_config,
        text    = 'Browse...',
        command = config_file_browser
        )

config_label.pack()
config_file_entry.pack(side = tk.LEFT, fill = tk.X, expand = True, padx = 5)
browse_button.pack(side = tk.RIGHT, padx = 5)

##################################################
# These frames contain the buttons at the bottom #
##################################################

frame_buttons = ttk.Frame(
        master = window,
        )

run_gzdoom_button = ttk.Button(
        master  = frame_buttons,
        text    = "Run gzdoom", 
        command = lambda: run(window)
        )

run_gzdoom_button.pack(side = tk.LEFT, expand = True, fill = tk.X, padx = 5)

exit_button = ttk.Button(
        master  = frame_buttons,
        text    = "Exit",
        command = exit
        )

exit_button.pack(side = tk.RIGHT, expand = True, fill = tk.X, padx = 5)

frame_wads.pack(pady = 2, fill = tk.BOTH, expand = True
    )
frame_config.pack(fill = tk.X)
frame_buttons.pack(fill = tk.X, pady = 2)

tk.mainloop()
