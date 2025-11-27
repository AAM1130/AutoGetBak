#
# Created by SituationUnknown(AAM1130) on 11/21/25
#
# Simplified Python GUI application for removing copied .bak files from directory sync backups.
#

import os
import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.constants import RIGHT, MULTIPLE


# function call to choose directory to scan
def choose_dir():
    folder = filedialog.askdirectory()
    if folder:
        dir_var.set(folder)

# function to walk the selected directory and find valid .bak files with a matching .dwg
def search_bak_files():
    folder = dir_var.get()
    bak_files.clear()
    listbox.delete(0, tk.END)

    for root, _, files in os.walk(folder):
        for file in files:
            # print(file.lower()) # debug statement
            if file.lower().endswith((".bak")):
                # print(file.lower()) # debug statement
                dwg_file = os.path.splitext(file)[0] + ".dwg"
                # print(dwg_file) # debug statement
                if dwg_file in files: # confirm the .dwg file exists
                    full_path = os.path.join(root, file)
                    bak_files.append(full_path)
                    listbox.insert(tk.END, full_path)

# function to select all listed items in the view
def select_all():
    listbox.select_set(0, tk.END)

# function to clear all selected items in the view
def clear_selected():
    listbox.select_clear(0, tk.END)

# function to remove all selected .bak files
def delete_selected_files():
    selected_indices = listbox.curselection()
    if not selected_indices:
        messagebox.showinfo("Info", "No files selected")
        return

    selected_files = [bak_files[i] for i in selected_indices]
    confirm = messagebox.askyesno("Confirm", f"Delete {len(selected_files)} selected .bak files?")
    if confirm:
        for file in selected_files:
            try:
                os.remove(file)
            except FileNotFoundError as e:
                messagebox.showerror("Error", e)

        # refresh listing after delete
        search_bak_files()
        messagebox.showinfo("Done", "Selected .bak files deleted")


# GUI Variables

root = tk.Tk()
root.title("AutoGetBak")

dir_var = tk.StringVar()
bak_files: list = []

# directory selection frame
dir_frame = tk.Frame(root)
dir_frame.pack(pady=5)
# directory entry elements
tk.Entry(dir_frame, textvariable=dir_var, width=50).pack(side="left", padx=5, pady=5)
tk.Button(dir_frame, text="Choose Directory", command=choose_dir).pack(side="left", padx=5, pady=5)

# buttons frame
button_frame = tk.Frame(root)
button_frame.pack(pady=5)
# button elements for button frame
tk.Button(button_frame, text="Search", command=search_bak_files).pack(side="left", padx=5, pady=5)
tk.Button(button_frame, text="Select All", command=select_all).pack(side="left", padx=5, pady=5)
tk.Button(button_frame, text="Clear Selected", command=clear_selected).pack(side="left", padx=5, pady=5)
tk.Button(button_frame, text="Purge Selected", command=delete_selected_files).pack(side="left", padx=5, pady=5)

# list box frame
listbox_frame = tk.Frame(root)
listbox_frame.pack(fill="both", expand=True, padx=10, pady=10)

# list box
listbox = tk.Listbox(listbox_frame, selectmode=MULTIPLE)
listbox.grid(row=0, column=0, sticky="nsew")
# scroll bars
sb_y = tk.Scrollbar(listbox_frame, orient="vertical", command=listbox.yview)
sb_y.grid(row=0, column=1, sticky="ns")
sb_x = tk.Scrollbar(listbox_frame, orient="horizontal", command=listbox.xview)
sb_x.grid(row=1, column=0, sticky="ew")

# attach scroll bars to the list box
listbox.configure(yscrollcommand=sb_y.set, xscrollcommand=sb_x.set)

# make list box frame expandable
listbox_frame.grid_rowconfigure(0, weight=1)
listbox_frame.grid_columnconfigure(0, weight=1)

root.mainloop()
