import customtkinter as ctk
from tkinter import filedialog, messagebox
from utils import populate_list, validate_stock_exists, vin_stock_matches, odom_matches
import sys
import os
import subprocess

# Define a paths list for the paths of the 4 files we will be reading with inventory info
paths = ['', '', '', '']
# Define lists variable for storing the info from the inventory files
lists = []

# Function for creating a file selector takes in a label and index
def make_file_selector(label, i):
    # function to select file
    def select_file():
        # Gets file path from user with filedialog pop up
        file_path = filedialog.askopenfilename(title="Select a file")
        # checks to make sure there is actually a file path before using it
        if file_path:
            # sets label to the file path so user can visually verify they've selected the correct file
            label.config(text=file_path)
            # sets the path in the paths list at the index to the retrieved file path
            paths[i] = file_path
    # returns the select file function to be used by the file selectors on the GUI
    return select_file

# function to print results to .txt file. F is a reference to the file to use to write
# a is the index within lists for the inventory in the old system
# b is the index for the inventory in the new system
def print_to_file(f, a, b):
    # write to the file either for the new or used vehicle header
    f.write("------------------------------\n")
    f.write(f"{"NEW VEHICLE VALIDATION REPORT" if a==1 else "USED VEHICLE VALIDATION REPORT"}\n")
    f.write("------------------------------\n")
    # call validate_stock_exists function to validate stock with input indexs
    stock_missing_count, missing_stocks = validate_stock_exists(lists[a], lists[b])
    # write any missing stocks to the file
    f.write(f"Number of stocks missing from ignite: {stock_missing_count}\n")
    if len(missing_stocks) > 0:
        for i in missing_stocks:
            f.write(f"{i}\n")
    # call vin_stock_matches function to get any vin errors
    vin_errors_found, vin_error_cars = vin_stock_matches(missing_stocks, lists[a], lists[b])
    # write any errors to txt file
    f.write(f"Number of stock/vin mismatches: {vin_errors_found}\n")
    if vin_errors_found > 0:
        f.write("(original system stock/vin)\n")
        for car in vin_error_cars:
            f.write(f"{str(car)}\n")
    # do the same for odom_matches
    odom_errors_found, odom_error_cars = odom_matches(missing_stocks, lists[a], lists[b])
    f.write(f"Number of stocks with odom discrepancy: {odom_errors_found}\n")
    if odom_errors_found > 0 :
        f.write("(from original system)\n")
        for i in odom_error_cars:
            f.write(f"{str(i)}\n")

# define function to run when the "Run" button is clicked on the UI
def run():
    # get user text input
    user_text = entry.get()
    
    # iterate through the user selected file paths
    for i in range(len(paths)):
        # if a path is missing, give the user a message box asking to select all file
        if not paths[i]:
            messagebox.showinfo("info","Please attach files to all locations")
            # return if not all files are correctly selected
            return
        # call populate_list function to extract data from file and append that result to the list of file info
        lists.append(populate_list(paths[i]))
    # create file name for the txt file to include the CIF if the user entered one
    file_name = os.path.join(os.path.dirname(os.path.abspath(__file__)), f"{user_text}{' ' if user_text else ''}Validation Report.txt")
    # open txt file
    with open(file_name, "w") as f:
        # call print_to_file function passing the file reference with the new inventory indexes
        print_to_file(f, 1, 0)
        # call print_to_file with used inventory indexes
        print_to_file(f, 3, 2)
        # Set what method to use to setup the file depending on operating system
        if sys.platform == "win32":
            os.startfile(file_name)
        elif sys.platform == "darwin":  # macOS
            subprocess.run(["open", file_name])
        else:  # Linux and others
            subprocess.run(["xdg-open", file_name])


# set color UI color scheme and default color
ctk.set_appearance_mode("dark")
ctk.set_default_color_theme("blue")

# Set up the main window with root, title, and dimensions
root = ctk.CTk()
root.title("Auto Validate Inventory")
root.geometry("500x500")

# Create labels and buttons in a loop
labels = []
titles = ['New Inventory IGNITE', 'New Inventory Old', 'Used Inventory IGNITE', 'Used Inventory Old']

# create label and entry for CIF and the space around it
entry_label = ctk.CTkLabel(root, text="CIF Number (Optional)", wraplength=550)
entry_label.pack()
entry = ctk.CTkEntry(root, width=150)
entry.pack()
entry_spacer = ctk.CTkFrame(root, height=20, fg_color="transparent")
entry_spacer.pack()

# Iterate 4 times for the 4 different files
for i in range(4):
    # create label for file selectors
    label = ctk.CTkLabel(root, text=f"No file selected for File {i+1}", wraplength=550)
    label.pack()
    # space between label and button
    top_spacer = ctk.CTkFrame(root, height=5, fg_color="transparent")
    top_spacer.pack()
    # button for a user to select file with the command make_file_selector run automatically called with the label and index
    # so that when it's clicked it will run the function returned by make_file_selector
    button = ctk.CTkButton(root, height=25, width=150, text=titles[i], command=make_file_selector(label, i))
    button.pack()
    # bottom spacer
    bottom_spacer = ctk.CTkFrame(root, height=20, fg_color="transparent")
    bottom_spacer.pack()
    # append the label to the labels list
    labels.append(label)

# create a spacer between the file selectors and the run button
top_spacer = ctk.CTkFrame(root, height=5, fg_color="transparent")
top_spacer.pack()

# create the run button that runs the run function when clicked
button = ctk.CTkButton(root, height=25, width=60, text="Run", command=run)
button.pack()



    

# Start the GUI event loop
root.mainloop()
