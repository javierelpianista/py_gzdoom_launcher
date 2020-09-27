import tkinter as tk
from tkinter import ttk
import os
import sys

class Option:
    def __init__(self, string, mult, options):
        self.string  = string
        self.mult    = mult
        self.options = options
        self.val     = 0

dmflags = [
    Option('Falling damage', 8, ['Off', 'Old', 'Hexen', 'Strife']),
    Option('Infinite ammo', 2048, ['No', 'Yes']),
    Option('No monsters', 4096, ['No', 'Yes']),
    Option('Monsters respawn', 8192, ['No', 'Yes']),
    Option('Items respawn', 16384, ['No', 'Yes']),
    Option('Fast monsters', 32768, ['No', 'Yes']),
    Option('Allow jump', 65536, ['Default', 'Off', 'On']),
    Option('Allow freelook', 262144, ['Default', 'Off', 'On']),
    Option('Allow FOV', 1048576, ['Off', 'On']),
    Option('Allow crouch', 4194304, ['Default', 'Off', 'On']),
]

dmflags2 = [
    Option('Drop weapon', 2, ['No', 'Yes']),
    Option('Double ammo', 64, ['No', 'Yes']),
    Option('Degeneration', 128, ['No', 'Yes']),
    Option('Allow BFG aiming', 256, ['Yes', 'No']),
    Option('No respawn', 16384, ['No', 'Yes']),
    Option('Infinite inventory', 65536, ['No', 'Yes']),
    Option('No monsters to exit', 131072, ['No', 'Yes']),
    Option('Allow automap', 262144, ['Yes', 'No']),
    Option('Automap allies', 524288, ['Yes', 'No']),
    Option('Allow spying', 1048576, ['Yes', 'No']),
    Option('Chasecam cheat', 2097152, ['No', 'Yes']),
    Option('Allow Suicide', 4194304, ['Yes', 'No']),
    Option('Allow Autoaim', 8388608, ['Yes', 'No']),
    Option('Check ammo for weapon switch', 16777216, ['Yes', 'No']),
    Option('Icon\'s death kills its spawns', 33554432, ['No', 'Yes']),
    Option('End sector counts for kill %', 67108864, ['Yes', 'No']),
    Option('Big powerups respawn', 134217728, ['No', 'Yes']),
    ]

class ButtonList(ttk.Frame):
    def print_value(self):
        val = self.intvar.get()
        for n, option in enumerate(self.option.options):
            if n == val:
                print(option)

    def update(self):
        self.option.val = self.intvar.get()
        self.master.update_flag_value()

    def set(self, value):
        self.intvar.set(value)
        self.option.val = value

    def __init__(self, master, option):
        super().__init__(master = master)

        self.checkbuttons = []
        self.value  = 0
        self.master = master
        self.intvar = tk.IntVar()
        self.option = option

        for n, option in enumerate(self.option.options):
            self.checkbuttons.append(
                    ttk.Checkbutton(
                        master   = self,
                        text     = option,
                        variable = self.intvar,
                        onvalue  = n,
                        command  = self.update
                        )
                    )

            self.checkbuttons[-1].pack(side = tk.LEFT, fill = tk.X)

class DmFlagsWindow(tk.Toplevel):
    def update_flag_value(self):
        dmflag = 0
        for button in self.buttons:
            dmflag += button.option.mult*button.option.val

        self.flag_value = dmflag
        self.label_flag.config(text = '{}: {}'.format(self.title(), dmflag))

    def return_flag(self):
        return self.flag_value

    def set_flags(self):
        sorted_buttons = sorted(self.buttons, key = lambda x: x.option.mult, reverse = True)

        curr_flag_value = self.flag_value

        for button in sorted_buttons:
            mult = button.option.mult
            val  = int(curr_flag_value / mult)
            button.set(val)

            curr_flag_value -= val*mult

    def OK(self):
        self.destroy()

    def back(self):
        self.flag_value = self.initial_flag_value
        self.destroy()

    def __init__(self, master, options, flag_value = 0, title = ''):
        super().__init__(master)

        if not os.name == 'nt':
            self.attributes('-type', 'dialog')
    
        self.labels  = []
        self.buttons = []
        self.initial_flag_value = flag_value
        self.flag_value = flag_value
        self.title(title)

        self.label_flag = ttk.Label(
                master = self,
                text   = '{}: {}'.format(self.title(), self.flag_value)
                )

        self.label_flag.grid(row = 0, columnspan = 2, pady = (5, 10))

        for n, option in enumerate(options):
            self.labels.append(
                    ttk.Label(
                        master = self,
                        text   = option.string,
                        anchor = 'w'
                        )
                    )

            self.labels[-1].grid(
                    row    = n + 1,
                    column = 0,
                    sticky = tk.W
                    )

            self.buttons.append(
                    ButtonList(
                        self,
                        option
                        )
                    )

            self.buttons[-1].grid(
                    row = n + 1,
                    column = 1,
                    sticky = tk.W
                    )

        self.frame_bottom = ttk.Frame(
                master = self
                )

        self.button_ok = ttk.Button(
                master  = self.frame_bottom,
                text    = 'OK',
                command = self.OK
                )

        self.button_back = ttk.Button(
                master  = self.frame_bottom,
                text    = 'Back',
                command = self.back
                )

        self.button_ok.pack(side = tk.LEFT, padx = 5)
        self.button_back.pack(side = tk.LEFT, padx = 5)

        self.frame_bottom.grid(row = n + 2, columnspan = 2, pady = (10, 5))

        self.set_flags()

def get_flags(parent, initial_flag_value = 0, kind = 'dmflags'):
    if kind == 'dmflags':
        window2 = DmFlagsWindow(parent, dmflags, flag_value = initial_flag_value, title = kind)
    elif kind == 'dmflags2':
        window2 = DmFlagsWindow(parent, dmflags2, flag_value = initial_flag_value, title = kind)
    else:
        raise Exception('kind {} not recognized'.format(kind))

    parent.wait_window(window2)
    return window2.return_flag()

if __name__ == '__main__':
    pass
