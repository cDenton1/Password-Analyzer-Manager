import tkinter as tk
from tkinter import messagebox
import analyzeCode
import manageCode
import pickle
from servClass import services

mastPassCheck = False
section = 1

# function to check the master password that was input
def returnMasterPass(masterPass_input):
    global mastPassCheck, section
    mastPassCheck = False
    mastPassCheck = manageCode.check_input(masterPass_input)

    manager.destroy()
    print(mastPassCheck)
    return(mastPassCheck)

def masterPass():
    global manager
    
    # create page to input master password
    manager = tk.Toplevel()
    manager.wm_title("Enter Master Password")
    manager.geometry("300x150")
    manager.configure(bg="gray")

    # input box for password
    masterPass_input = tk.Entry(manager, width=35)
    masterPass_input.place(x=15, y=50)

    # submit button to analyze users input
    masterPass_submit = tk.Button(manager, text="Enter", command=lambda: returnMasterPass(masterPass_input))
    # masterPass_submit = tk.Button(manager, text="Enter", command=manageCode.check_input)
    masterPass_submit.place(x=250, y=48)

    # label to request user to enter their master password
    enter_label = tk.Label(manager, text="Enter your Master Password:", background="gray")
    enter_label.place(x=15, y=25)

    # label to request user to enter their master password
    note_label = tk.Label(manager, text="*WARNING: First time entering your master password\n will set the password, keep track of it!*", background="gray")
    note_label.place(x=5, y=90)

    manager.wait_window()  # Wait for the password window to close
    return mastPassCheck


# functions to deal with what is showing on the GUI
def a_sect():
    global section 
    section = 1
    change_sect()

def m_sect():
    global section
    section = 2
    change_sect()

def change_sect():
    global section
    # section 1 = analyzer
    if section == 1:
        submit_button.place(x=250, y=48)        # show submit button
        input_box.place(x=75, y=50)             # show input box

        analyze_button.place_forget()           # hide analyze button
        manage_button.place(x=200, y=0)         # show manage button

        analyze_label.place(x=75, y=2.5)        # show analyze label
        manage_label.place_forget()             # hide manage label

        canvasAnalyze.place(x=15, y=100)        # show the analyzing canvas
        canvasManager.place_forget()            # hide the managing canvas

        save_button.place(x=95, y=465)          # show the save button
        export_button.place(x=195, y=465)       # show the export button

        scrollbarA.place(x=370, y=100, height=350)  # show analyzer scrollbar
        scrollbarM.place_forget()                   # hide manager scrollbar

        output_textM.delete("1.0", "end")

    # section 2 = manager
    elif section == 2:
        submit_button.place_forget()            # hide submit button
        input_box.place_forget()                # hide input box

        analyze_button.place(x=0, y=0)          # show analyze button
        manage_button.place_forget()            # hide manage button

        analyze_label.place_forget()            # hide analyze label
        manage_label.place(x=275, y=2.5)        # show manage label

        canvasAnalyze.place_forget()            # hide the analyzing canvas
        canvasManager.place(x=15, y=45)         # show the managing canvas

        save_button.place_forget()              # hide the save button
        export_button.place_forget()            # hide the export button
        scrollbarA.place_forget()               # hide analyzer scrollbar

        checkMP = masterPass()                  # check master password

        if checkMP is False:
            a_sect()                            # go back to the analyzer section
        else:
            scrollbarM.place(x=370, y=50, height=434) # show manage scrollbar

            # open and store passwords
            with open("passwords.pickle", 'rb') as file:
                pass_list = pickle.load(file)

            # cycle through passwords in the pickle file to output
            for entry in pass_list:
                if isinstance(entry, services):
                    if entry.service == "Master" or entry.service == None:
                        continue
                    else: 
                        output_textM.insert("end", f"{entry.service}: {entry.password}\n\n", "bold")
        

# create the main window
window = tk.Tk()
window.title("Password Analyzer & Manager")
window.geometry("400x500")
window.configure(bg="gray")

# initialize password input
password = ""


# make canvas, where text output for analyzing will be
canvasAnalyze = tk.Canvas(window, width=370, height=350, bg="white")
canvasAnalyze.place(x=15, y=100)

# add a text widget for displaying analysis results
output_textA = tk.Text(canvasAnalyze, width=44, height=22, wrap="word", bg="white")
output_textA.place(x=0, y=0)

# add a scrollbar for the text widget
scrollbarA = tk.Scrollbar(window, orient="vertical", bg="gray", command=output_textA.yview)
scrollbarA.place(x=370, y=100, height=349)

# link the scrollbar to the text widget
output_textA.config(yscrollcommand=scrollbarA.set)


# make canvas, where text output for managing will be
canvasManager = tk.Canvas(window, width=370, height=435, bg="white")
canvasManager.place(x=15, y=15)

# add a text widget for displaying passwords in the manager will be
output_textM = tk.Text(canvasManager, width=44, height=28, wrap="word", bg="white")
output_textM.place(x=0, y=0)

# add a scrollbar for the text widget
scrollbarM = tk.Scrollbar(window, orient="vertical", bg="gray", command=output_textM.yview)
scrollbarM.place(x=370, y=50, height=434)

# link the scrollbar to the text widget
output_textM.config(yscrollcommand=scrollbarM.set)


# analyze button to switch sections of the GUI
analyze_button = tk.Button(window, text="Analyzer", width=28, command=a_sect)

# label to replace the button when in the analyze section
analyze_label = tk.Label(window, text="Analyzer", background="gray")
analyze_label.place(x=75, y=0)

# manage button to switch sections of the GUI
manage_button = tk.Button(window, text="Manager", width=28, command=m_sect)
manage_button.place(x=200, y=0)

# label to replace the button when in the manager section
manage_label = tk.Label(window, text="Manager", background="gray")

# input box for password
input_box = tk.Entry(window, width=25)
input_box.place(x=75, y=50)

# submit button to analyze users input
# submit_button = tk.Button(window, text="Analyze", command=finalCode.get_input)
submit_button = tk.Button(window, text="Analyze", command=lambda: finalCode.analyze(input_box.get(), output_textA))
submit_button.place(x=250, y=48)

# button to save password to the password manager
save_button = tk.Button(window, text="Save Password", command=lambda: manageCode.save_password(input_box.get(), output_textA))
save_button.place(x=85, y=465)

# button to export password info
export_button = tk.Button(window, text="Export Password Info", command=lambda: finalCode.export_password(output_textA))
export_button.place(x=185, y=465)

change_sect()

window.mainloop()
