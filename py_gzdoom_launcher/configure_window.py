import os
import tkinter as tk
from tkinter import messagebox
from tkinter import ttk, filedialog
from py_gzdoom_launcher import variables

class BrowseButton(ttk.Button):
    def __init__(self, master, **kwargs):

        super().__init__(
                master  = master,
                text    = 'Browse...',
                **kwargs
                )

class FrameEntryBrowse(ttk.Frame):
    def get_value(self):

        return self.entry.get()

    def browse_filename(self, initial_dir, dialog_title, filetype):
        if filetype == 'dir':
            filename = filedialog.askdirectory(
                    initialdir = os.path.dirname(initial_dir),
                    title      = dialog_title
                    )

        elif filetype == 'file':
            filename = filedialog.askopenfilename(
                    initialdir = os.path.dirname(initial_dir),
                    title      = dialog_title
                    )
        else:
            raise Exception('Wrong filetype. Choose either file or dir.')

        if filename:
            self.entry.delete(0, tk.END)
            self.entry.insert(0, filename)

    def __init__(self, **kwargs):
        super().__init__(kwargs['master'])

        self.label = ttk.Label(
                master = self,
                text   = kwargs['text']
                )

        self.label.pack(
                fill   = tk.X
                )

        self.entry = ttk.Entry(
                master = self,
                )

        self.entry.insert(0, kwargs['initial_value'])

        self.entry.pack(
                fill   = tk.X,
                expand = True, 
                side   = tk.LEFT
                )

        self.button = BrowseButton(
                master = self,
                command = lambda: self.browse_filename(
                    kwargs['initial_value'],
                    kwargs['text'],
                    kwargs['filetype']
                    )
                )

        self.button.pack(
                side = tk.RIGHT,
                padx = 5
                )

class ConfigureWindow(tk.Toplevel):
    def accept(self):
        variables.variables['executable']   = self.frame_executable.get_value()
        variables.variables['wad_dirs']     = self.frame_wads.get_value()
        # For now we set the iwad dir to be in the same place as the wad one. May change in the future.
        variables.variables['iwad_dir']     = self.frame_wads.get_value()
        variables.variables['default_iwad'] = os.path.basename(self.frame_iwad.get_value())

        variables.write_config()

        messagebox.showinfo(
                master  = self,
                message = 'Configuration saved.'
                )

    def back(self, master):
        self.destroy()

    def __init__(self, master):
        super().__init__(master)

        self.title('Configuration')
        if not os.name == 'nt':
            self.attributes('-type', 'dialog')
        self.grab_set()
        self.minsize(400, 0)

        # Choose the executable
        self.frame_executable = FrameEntryBrowse(
                master        = self,
                text          = 'gzdoom executable location',
                initial_value = variables.variables['executable'],
                filetype      = 'file'
                )

        self.frame_executable.pack( fill = tk.X, padx = 5, pady = 5 )

        ## Choose the directory where all the files will be included
        #self.frame_directory = FrameEntryBrowse(
        #        master        = self,
        #        text          = 'py_gzdoom_launcher main directory',
        #        initial_value = variables.variables['main_dir'],
        #        filetype      = 'dir'
        #        )

        #self.frame_directory.pack( fill = tk.X, padx = 5, pady = 5 )

        ## Directory for the profile files
        #self.frame_profile = FrameEntryBrowse(
        #        master        = self,
        #        text          = 'Profile directory',
        #        initial_value = variables.variables['profile_dir'],
        #        filetype      = 'dir'
        #        )

        #self.frame_profile.pack( fill = tk.X, padx = 5, pady = 5 )

        ## Directory for the config files
        #self.frame_config = FrameEntryBrowse(
        #        master = self,
        #        text   = 'Configuration files directory',
        #        initial_value = variables.variables['config_dir'],
        #        filetype      = 'dir'
        #        )

        #self.frame_config.pack( fill = tk.X, padx = 5, pady = 5 )

        # IWAD directory
        #self.frame_iwads = FrameEntryBrowse(
        #        master = self,
        #        text   = 'IWADs directory',
        #        initial_value = variables.variables['iwad_dir'],
        #        filetype      = 'dir'
        #        )

        #self.frame_iwads.pack( fill = tk.X, padx = 5, pady = 5 )

        # WADs directory
        self.frame_wads = FrameEntryBrowse(
                master = self,
                text   = 'WADs directory',
                initial_value = variables.variables['wad_dirs'],
                filetype      = 'dir'
                )

        self.frame_wads.pack( fill = tk.X, padx = 5, pady = 5 )

        # Default IWAD
        self.frame_iwad = FrameEntryBrowse(
                master = self,
                text   = 'Default IWAD',
                initial_value = os.path.join(
                    variables.variables['wad_dirs'],
                    variables.variables['default_iwad']
                    ),
                filetype      = 'file'
                )

        self.frame_iwad.pack( fill = tk.X, padx = 5, pady = 5 )

        # Buttons to accept configuration changes or back them
        self.frame_buttons = ttk.Frame(master = self)

        self.button_accept = ttk.Button(
                master  = self.frame_buttons,
                text    = 'Save',
                command = self.accept
                )

        self.button_back = ttk.Button(
                master  = self.frame_buttons,
                text    = 'Back',
                command = lambda: self.back(master)
                )

        self.button_accept.pack(
                side = tk.RIGHT,
                fill = tk.X,
                )

        self.button_back.pack(
                side = tk.RIGHT,
                fill = tk.X,
                padx = (0, 10)
                )

        self.frame_buttons.pack(
                fill = tk.X,
                padx = 5, 
                pady = (5, 10)
                )

if __name__ == '__main__':
    root = tk.Tk()
    window = ConfigureWindow(root)

    tk.mainloop()
