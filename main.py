import customtkinter as ctk
from tkinter import filedialog, messagebox
from utils import populate_list, validate_stock_exists, vin_stock_matches, odom_matches
import sys
import os
import subprocess

paths = ['', '', '', '']
lists = []

def make_file_selector(label, i):
    def select_file():
        file_path = filedialog.askopenfilename(title="Select a file")
        if file_path:
            label.config(text=file_path)
            paths[i] = file_path
    return select_file

def print_to_file(f, a, b):
    f.write("------------------------------\n")
    f.write(f"{"NEW VEHICLE VALIDATION REPORT" if a==1 else "USED VEHICLE VALIDATION REPORT"}\n")
    f.write("------------------------------\n")
    stock_missing_count, missing_stocks = validate_stock_exists(lists[a], lists[b])
    f.write(f"Number of stocks missing from ignite: {stock_missing_count}\n")
    if len(missing_stocks) > 0:
        for i in missing_stocks:
            f.write(f"{i}\n")
    vin_errors_found, vin_error_cars = vin_stock_matches(missing_stocks, lists[a], lists[b])
    f.write(f"Number of stock/vin mismatches: {vin_errors_found}\n")
    if vin_errors_found > 0:
        f.write("(original system stock/vin)\n")
        for car in vin_error_cars:
            f.write(f"{str(car)}\n")
    odom_errors_found, odom_error_cars = odom_matches(missing_stocks, lists[a], lists[b])
    f.write(f"Number of stocks with odom discrepancy: {odom_errors_found}\n")
    if odom_errors_found > 0 :
        f.write("(from original system)\n")
        for i in odom_error_cars:
            f.write(f"{str(i)}\n")

def run():
    user_text = entry.get()
    
    for i in range(len(paths)):
        if not paths[i]:
            messagebox.showinfo("info","Please attach files to all locations")
            return
        lists.append(populate_list(paths[i]))
    file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{user_text}{' ' if user_text else ''}Validation Report.txt")
    with open(file_name, "w") as f:
        print_to_file(f, 1, 0)
        print_to_file(f, 3, 2)
        if sys.platform == "win32":
            os.startfile(file_name)
        elif sys.platform == "darwin":  # macOS
            subprocess.run(["open", file_name])
        else:  # Linux and others
            subprocess.run(["xdg-open", file_name])



ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")
# Set up the main window
root = ctk.CTk()
root.title("Auto Validate Inventory")
root.geometry("500x500")

# Create labels and buttons in a loop
labels = []
titles = ['New Inventory IGNITE', 'New Inventory Old', 'Used Inventory IGNITE', 'Used Inventory Old']
# entry_label = ctk.Label(root, text="CIF Number (Optional)", wraplength=550)
# entry_label.pack()
entry_label = ctk.CTkLabel(root, text="CIF Number (Optional)", wraplength=550)
entry_label.pack()
entry = ctk.CTkEntry(root, width=150)
entry.pack()
entry_spacer = ctk.CTkFrame(root, height=20, fg_color="transparent")
entry_spacer.pack()
for i in range(4):
    label = ctk.CTkLabel(root, text=f"No file selected for File {i+1}", wraplength=550)
    label.pack()

    top_spacer = ctk.CTkFrame(root, height=5, fg_color="transparent")
    top_spacer.pack()
    
    button = ctk.CTkButton(root, height=25, width=150, text=titles[i], command=make_file_selector(label, i))
    button.pack()

    bottom_spacer = ctk.CTkFrame(root, height=20, fg_color="transparent")
    bottom_spacer.pack()
    
    labels.append(label)


top_spacer = ctk.CTkFrame(root, height=5, fg_color="transparent")
top_spacer.pack()
    
button = ctk.CTkButton(root, height=25, width=60, text="Run", command=run)
button.pack()



    

# Start the GUI event loop
root.mainloop()
