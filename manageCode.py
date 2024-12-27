import tkinter as tk
from tkinter import messagebox
from servClass import services
import guiCode
import os
import pickle

test = services(None, None, None)

pass_list = [test]

def check_input(input_field):
    global pass_list                    # global variable list to store contents of pickle file every time i read or write to it
    password = " "                      # initialize password

    password = input_field.get()        # store password from the input field
    file_path = "passwords.pickle"      # initialize file path the to the passwords file
    is_master = False                   # set if master password exists to false

    if password == "" :                 # check for no input
        messagebox.showinfo("Error", "No password entered, try again!")
        return(False)
    
    if os.path.exists(file_path):       # check if file exists
        print("File exists") 
        with open(file_path, 'rb') as file:
            pass_list = pickle.load(file)   # store list of passwords
    else:
        with open(file_path, 'wb') as file:
            pickle.dump(pass_list, file)    # create list and store placeholder

    for service in pass_list:               # check if master password exists
        if service.service == 'Master':
            is_master = True
        
    if is_master == False:                                                          # check if false
        Master = services("Master", None, password)                                 # set master password
        pass_list.append(Master)                                                    # append list for writing to the pickle file with 
        with open(file_path, 'wb') as file:
            pickle.dump(pass_list, file)
        messagebox.showinfo("Success", "New Master Password set!")
    else:
        for service in pass_list:                                                   # check if true
            if service.service == 'Master' and service.password == password:        # check if input equals the master password
                messagebox.showinfo("Success", "Correct password, welcome back!")   # print success/welcome back message
                return(True)
            elif service.service == 'Master' and service.password != password:      # check if input doesnt the master password
                messagebox.showerror("Error", "Incorrect password")                 # print error/incorrect message
                return(False)

def save_password(password, output_widget):
    print(password)
    if len(password) == 0:                                              # check if something was actually input
        output_widget.insert("end", f"Nothing entered try again\n")     # tell user to re-enter if length equals 0
        return    
    password = password.replace(' ', '_')                               # replace all spaces with underscores
    save_info(password)

def save_info(password):
    password = password
    global serviceP
    
    # create window for password info input
    serviceP = tk.Toplevel()
    serviceP.wm_title("Enter Password Info")
    serviceP.geometry("300x100")
    serviceP.configure(bg="gray")

    # input box for password
    service_input = tk.Entry(serviceP, width=35)
    service_input.place(x=15, y=50)

    # submit button to analyze users input
    service_submit = tk.Button(serviceP, text="Enter", command=lambda: write_save(service_input, password))
    # masterPass_submit = tk.Button(manager, text="Enter", command=manageCode.check_input)
    service_submit.place(x=250, y=48)

    # label to request user to enter their master password
    enter_label = tk.Label(serviceP, text="Enter the service used for this password:", background="gray")
    enter_label.place(x=15, y=25)

# function for saving new entries to the password file
def write_save(service_input, password):
    global pass_list
    global serviceP
    file_path = "passwords.pickle"      # initialize file path

    if os.path.exists(file_path):       # check if file exists
        print("File exists") 
        with open(file_path, 'rb') as file:
            pass_list = pickle.load(file)   # store list of passwords
    else:
        with open(file_path, 'wb') as file:
            pickle.dump(pass_list, file)    # create list and store placeholder

    password = password                     # store password
    service = service_input.get()           # store service

    with open(file_path, 'rb') as file:
        pass_list = pickle.load(file)       # store contents of pickle

    entry = services(service, None, password)   # create service entry
    pass_list.append(entry)                     # append list of contents

    with open(file_path, 'wb') as file:
        pickle.dump(pass_list, file)            # write to the pickle file
    messagebox.showinfo("Success", "New password added!") # output to user the successful password
    serviceP.destroy()
    
    print("done")                           # debug message to terminal to make sure it wasn't getting stuck anywhere
