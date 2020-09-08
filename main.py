import tkinter as tk
import os
import run_command
from variables import wad_dirs

# Get the list of available wad files
wad_list = run_command.get_list_of_wad_files(wad_dirs)

def run(window):
    window.destroy()
    #os.system('gzdoom')
    command = 'gzdoom' 
    for wad in wad_list:
        if intvars[wad].get():
            command += ' -file {}'.format(wad)

    os.system(command)

def handle_exit(event):
    exit()

def exit():
    quit()

window = tk.Tk()
window.bind("<Control-q>", handle_exit)

frame1 = tk.Frame()
frame2 = tk.Frame()

intvars = {}
for n, wad in enumerate(wad_list):
    intvars[wad] = tk.IntVar()
    tk.Checkbutton(frame1, text = wad, variable = intvars[wad]).grid(row=n, sticky=tk.W)

run_gzdoom_button = tk.Button(
        master  = frame2,
        text    = "Run gzdoom", 
        command = lambda: run(window)
        )
run_gzdoom_button.pack()

exit_button = tk.Button(
        master  = frame2,
        text    = "Exit",
        command = exit
        )
exit_button.pack()

frame1.pack()
frame2.pack()

tk.mainloop()
