import os
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from variables import profile_dir
import glob
from create_profile import CreateProfileWindow
from select_profile import SelectProfileWindow

main_window = SelectProfileWindow()
tk.mainloop()
