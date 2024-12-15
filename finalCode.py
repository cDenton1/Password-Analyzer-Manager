import string
import tkinter as tk
import finalGUIcode
import os
import mmap
import pickle
from servClass import services
from tkinter import filedialog
from tkinter import messagebox
import sys
# test password = T3zt!ngP@zzw0rd
# test password #2 = Chr!s0lsenP@ssw0rd1997

# function to get users input * NO LONGER IN USE *
def get_input():
    password = finalGUIcode.input_box.get()         # store user input
    print(f"The password entered: {password}")      # print entered password out

# function to print output and call functions used for analyzing    * DEBUGGED WITH AI *
def analyze(password, output_widget):
    clear_output(output_widget)  # Clear previous output in the widget

    # password = finalGUIcode.input_box.get()         # store user input
    if len(password) == 0:                          # check if something was actually input
        output_widget.insert("end", f"Nothing entered try again\n")        # tell user to re-enter if length equals 0
        return
    
    password = password.replace(' ', '_')           # replace all spaces with underscores

    # Define a tag for bold text
    output_widget.tag_configure("bold", font=("Helvetica", 10, "bold"))
    output_widget.insert("end", f"The password entered: {password}\n\n", "bold")

    # Analyze length
    lenStrength = int(check_length(password, output_widget))
    output_widget.insert("end", f"Password length score: {lenStrength}\n\n", "bold")

    # Analyze variation
    varStrength = check_variation(password, output_widget)
    output_widget.insert("end", f"Password variation score: {varStrength}\n\n", "bold")

    # Analyze substitutions
    mPassword = make_subs(password, output_widget)

    # Analyze dictionary
    subStength, wordStrength = check_dictionary(password, mPassword, output_widget)
    # scores for 3 and 4 are printed in the function

    # Analyze names
    nameStrength = int(check_names(password, mPassword, output_widget))
    output_widget.insert("end", f"Names used score: {nameStrength}\n\n", "bold")

    # Analyze places
    placeStrength = int(check_places(password, mPassword, output_widget))
    output_widget.insert("end", f"Places used score: {placeStrength}\n\n", "bold")

    # Analyze dates
    dateStrength = int(check_dates(password, mPassword, output_widget))
    output_widget.insert("end", f"Dates used score: {dateStrength}\n\n", "bold")

    # Analyze numerical/alphabetical strings
    stringStrength = int(check_strings(password, mPassword, output_widget))
    output_widget.insert("end", f"Numerical/alphabetical strings used score: {stringStrength}\n\n", "bold")

    # Compare with rockyou.txt file
    rockyouStrength = int(check_rockyou(password, mPassword, output_widget))
    output_widget.insert("end", f"Rockyou comparison score: {rockyouStrength}\n\n", "bold")

    # Compare with previous input passwords
    prevpassStrength = int(check_prev(password, mPassword, output_widget))
    output_widget.insert("end", f"Previous password comparison score: {prevpassStrength}\n\n", "bold")

    # print out total score
    output_widget.insert("end", "Your overall score is calculated as the sum of the above criteria scores: the higher the score, the stronger your password.\n")
    overallScore = (lenStrength + varStrength + subStength + wordStrength + nameStrength + 
                    placeStrength + dateStrength + stringStrength + rockyouStrength + prevpassStrength)
    output_widget.insert("end", f"The overall score of your password: {overallScore}\n\n", "bold")

# function called to clear the text box used for output
def clear_output(output_widget):
    output_widget.delete("1.0", "end")


# 1. The length of the password is a minimum of twelve characters
def check_length(password, output_widget):
    pwd_len = len(password)     # store password length
    lenStrength = 0             # set strength score of the length to 0

    # check the length, print to the user how it stands, and update the strength score
    if pwd_len >= 12:
        output_widget.insert("end", "The length of your password is equal to or above the recommended length of 12\n")
        lenStrength = 10

    elif pwd_len >= 8:
        output_widget.insert("end", "The length of your password is below the recommended length of 12 BUT it is equal to or above what most websites and services require\n")
        lenStrength = 5

    else:
        output_widget.insert("end", "The length of your password doesn't meet the recommended length of 12 OR the minimum requirement of most websites\n")
        lenStrength = 0

    return(lenStrength)         # return the strength score

# 2. The variation in lowercase letters, uppercase letters, special characters, and numbers 
def check_variation(password, output_widget):
    length = len(password)
    varStrength = 10
    checkL = 2                  # set the check number

    lowercase = 0               # set the lowercase counter to 0
    uppercase = 0               # set the uppercase counter to 0
    digit = 0                   # set the number counter to 0
    specialchar = 0             # set the special character counter to 0

    for char in password:       # loop through characters in the password
        if char.islower():      # check if lowercase, uppercase, etc.
            lowercase += 1      # increase counter 

        elif char.isupper():
            uppercase += 1
        
        elif char.isdigit():
            digit += 1
        
        elif char in string.punctuation:
            specialchar += 1

    # initialize an empty list to store password tips
    tips = []

    # check and append necessary tips
    if lowercase < checkL:                              # check counter is lower than the predetermined check number
        tips.append("Adding more lowercase letters")    # append tip if below the predetermined check number
        varStrength -= 2.5                              # subtract from variation strength score
    if uppercase < checkL:
        tips.append("Adding more uppercase letters")
        varStrength -= 2.5
    if digit < checkL:
        tips.append("Adding more digits")
        varStrength -= 2.5
    if specialchar < checkL:
        tips.append("Adding more special characters")
        varStrength -= 2.5

    # decide what to print based on strength score
    if varStrength < 10:
        output_widget.insert("end", "You should consider:\n")                   # print tips on what to improve
        for tip in tips:
            output_widget.insert("end", f"{tip}\n")
    else:
        varStrength = int(varStrength)
        output_widget.insert("end", "Password includes a strong amount of variation\n")

    return(varStrength)                         # return the strength score

# make the subs that will be checked in the next step (ex. 3 instead of e) 
def make_subs(password, output_widget):
    mPassword = []                      # create array for modified password
    for char in password:               # check each char for commonly used subsitutions
        if char == "@":
            mPassword.append("a")       # append mPasswod with updated sub and loop through the rest
        elif char == "0":
            mPassword.append("o")
        elif char == "3":
            mPassword.append("e")
        elif char == "!":
            mPassword.append("i")
        elif char == "z":
            mPassword.append("s")
        else:
            mPassword.append(char)      # even if not a sub, still append mPassword

    mPassword = ''.join(mPassword)      # join array into a string
    print(f"The password after replacing common substitutions: {mPassword}\n")
    return(mPassword)                   # return mPassword

# class for reading and comparing with the files needed to check for some of the criteria 
class FileComparing:
    def __init__(self, file_path, password, mPassword):
        self.file_path = file_path
        self.password = password
        self.mPassword = mPassword

    def file_check(self):                       # check if the file exists
        if os.path.exists(self.file_path):      # mainly used for debugging
            print(f"{self.file_path} exists")
        else:
            print("File does not exist.")
            return False

    def compare(self):
        file = self.file_path
        matching_words = []
        matching_words_modified = []

        total_words = sum(1 for _ in open(file, encoding="utf-8", errors="ignore"))         # estimate progress for debugging
        processed = 0                                    # counter to track words that have been checked
        wordStrength = 10
        wordStrengthM = 10

        # print(f"Modified password for dictionary check: {mPassword.lower()}")     # print mPassword for debugging

        with open(file, 'r', encoding="utf-8", errors="ignore") as file:                                    # open the file storing dictionary words
            dictionary_words = {word.strip().lower() for word in file.readlines()}  # store words in a set for faster lookups

        for word in dictionary_words:
            word = word.strip().lower()                         # remove any whitespace or newline characters

            if "dates" not in self.file_path and (len(word) > len(self.password) or len(word) < 4):      # check the length before checking if it's in the password
                continue
            elif "places" in self.file_path and len(word) < 5:
                continue
            elif "lang" in self.file_path and len(word) <= len(self.password):
                if word in self.password.lower():               # check if the word is in the password
                    matching_words.append(word)                 # store the matching word
                    wordStrength -= 1                           # remove a point from the strength score

                if word in self.mPassword.lower():              # check if the word is in the password
                    matching_words_modified.append(word)        # store the matching word
                    wordStrengthM -= 1                          # remove a point from the strength score
            else:
                if word in self.password.lower():               # check if the word is in the password
                    matching_words.append(word)                 # store the matching word
                    wordStrength -= 0.5                           # remove a point from the strength score

                if word in self.mPassword.lower():              # check if the word is in the password
                    matching_words_modified.append(word)        # store the matching word
                    wordStrengthM -= 0.5                        # remove a point from the strength score

# DEBUGGING
            #if processed >= 345000:                                 # if processing halts at 345,000, stop there for debugging
            #    print(f"Stopping at {processed} for debugging")
            #    break                                               # temporary break for debugging

            #processed += 1                                                  # progress indicator for debugging
            #if processed % 2500 == 0:                                      # print progress every 2500 words processed
            #        print(f"Processed {processed}/{total_words} words...")
            #        time.sleep(0.01)

        # print(f"Found matching dictionary words: ")                               # begin printing found words for debugging
        # for word in matching_words:                                               # loop through words
        #     match_percentage = int((len(word) / len(self.password)) * 100)        # check matching percentage
        #     print(f"{word}: {match_percentage}")

        # print(f"\nFound matching dictionary words for the modified password: ")   # begin printing found words for debugging
        # for word in matching_words_modified:                                      # loop through words
        #     match_percentage = int((len(word) / len(self.mPassword)) * 100)       # check matching percentage
        #     print(f"{word}: {match_percentage}")
# DEBUGGING

        if self.password == self.mPassword and "lang-english.txt" in self.file_path:
            wordStrengthM = 10

        return(matching_words, matching_words_modified, wordStrength, wordStrengthM)

# 3. The use of common substitutions of letters (ex. 3 instead of e)    
# 4. The use of dictionary words * DEBUGGED WITH AI *
def check_dictionary(password, mPassword, output_widget):
    file_path = "lang-english.txt"
    matching_words, matching_words_modified, wordStrength, subStrength = FileComparing(file_path, password, mPassword).compare()

    common_words = list(set(matching_words) | set(matching_words_modified))

    if subStrength == 10 and password != mPassword:     # check the strength score and print a message related to the score
        output_widget.insert("end", "There were no dictionary words found\n")
    elif subStrength == 10 and password == mPassword:
        output_widget.insert("end", "No common substitutions were used\n")
    else:     # if it wasn't a perfect score, print the score and password advice
        output_widget.insert("end", "There were dictionary words found after replacing common substitutions\n")
    output_widget.insert("end", "With your passwords try to avoid the following: 3 = e/E, 0 = o, @ = a, and ! = i\n")
    
    output_widget.insert("end", f"Common substitution score: {subStrength}\n\n", "bold")

    # check the use of dictionary words
    if wordStrength == 10:      # check the strength score and print a message related to the score
        output_widget.insert("end", "There were no dictionary words found in your password\n")
    elif wordStrength > 6:
        output_widget.insert("end", "There were a couple of dictionary words found in your password\n")
    elif wordStrength > 3:
        output_widget.insert("end", "There were a handful of dictionary words found in your password\n")
    else:
        output_widget.insert("end", "There were a lot dictionary words found in your password\n")

    output_widget.insert("end", f"Words used score: {wordStrength}\n\n", "bold")

    # password advice no matter the score
    # print("Keep in mind, there might not be any dictionary words in the original but when modified with common substitutions, there might be.")

    return(subStrength, wordStrength)

# 5. The use of names
def check_names(password, mPassword, output_widget):
    file_path = "names.txt"
    matching_words, matching_words_modified, nameStrength, nameStrengthM = FileComparing(file_path, password, mPassword).compare()

    common_names = list(set(matching_words) & set(matching_words_modified))

    if nameStrength == 10 and nameStrengthM == 10:     # check the strength score and print a message related to the score
        output_widget.insert("end", "There were no names found in your password\n")
    elif nameStrengthM < 10 and nameStrength == 10:
        output_widget.insert("end", f"After replacing common substitutions, the listed names were found: {matching_words_modified}\n")
    elif nameStrength < 10 and nameStrengthM == 10:
        nameStrength = 0
        output_widget.insert("end", f"The listed names were found in your password: {matching_words}\n")
    else:
        nameStrength = 0
        output_widget.insert("end", f"The listed names were found in the original and modified password: {common_names}\n")

    overNameStrength = int((nameStrength + nameStrengthM) / 2)

    # password advice no matter the score
    # print("Keep in mind, there might not be any names in the original but when modified with common substitutions, there might be. And you shouldn't be putting any names in your password.")

    return(overNameStrength)

# 6. The use of places
def check_places(password, mPassword, output_widget):
    file_path = "places_sanitized.txt"
    matching_words, matching_words_modified, placeStrength, placeStrengthM = FileComparing(file_path, password, mPassword).compare()

    common_places = list(set(matching_words) & set(matching_words_modified))

    if placeStrength == 10 and placeStrengthM == 10:     # check the strength score and print a message related to the score
        output_widget.insert("end", "There were no places found in your password\n")
    elif placeStrengthM < 10 and placeStrength == 10:
        output_widget.insert("end", f"The listed places were found in the modified password: {matching_words_modified}\n")
    elif placeStrength < 10 and placeStrengthM == 10:
        placeStrength = 0
        output_widget.insert("end", f"The listed places were found in your password: {matching_words}\n")
    else:
        placeStrength = 0
        output_widget.insert("end", f"The listed places were found in the original and modified password: {common_places}\n")

    overPlaceStrength = (placeStrength + placeStrengthM) / 2

    # password advice no matter the score
    # print("Keep in mind, there might not be any names of places in the original but when modified with common substitutions, there might be. And you shouldn't be putting any names in your password.")

    return(overPlaceStrength)

# 7. The use of dates
def check_dates(password, mPassword, output_widget):
    file_path = "dates.txt"
    matching_dates, matching_dates_modified, dateStrength, dateStrengthM = FileComparing(file_path, password, mPassword).compare()

    common_dates = list(set(matching_dates) & set(matching_dates_modified))

    # USED FOR DEBUGGING 
    # print(dateStrength)
    # print(dateStrengthM)

    if dateStrength == 10 and dateStrengthM == 10:     # check the strength score and print a message related to the score
        output_widget.insert("end", "There were no dates found in your password\n")
    elif dateStrengthM < 0 and dateStrength == 10:
        output_widget.insert("end", f"The listed dates were found in the modified password: {matching_dates_modified}\n")
    elif dateStrength < 0 and dateStrengthM == 10:
        dateStrength = 0
        output_widget.insert("end", f"The listed dates were found in your password: {matching_dates}\n")
    else:
        dateStrength = 0
        output_widget.insert("end", f"the listed dates were found in the original and modified password: {common_dates}\n")

    # calculate average
    overDateStrength = int((dateStrength + dateStrengthM) / 2)

    # return calculated score
    return(overDateStrength)

# 8. The use of numerical or alphabetical strings (ex. 12345, abcde, etc.)
def check_strings(password, mPassword, output_widget):
    file_path = "strings.txt"
    matching_words, matching_words_modified, stringStrength, stringStrengthM = FileComparing(file_path, password, mPassword).compare()

    common_strings = list(set(matching_words) & set(matching_words_modified))

    if stringStrength == 10 and stringStrengthM == 10:     # check the strength score and print a message related to the score
        output_widget.insert("end", "There were no numerical/alphabetical strings found in your password\n")
    elif stringStrengthM < 10 and stringStrength == 10:
        output_widget.insert("end", f"The listed numerical/alphabetical strings were found in the modified password: {matching_words_modified}\n")
    elif stringStrength < 10 and stringStrengthM == 10:
        stringStrength = 0
        output_widget.insert("end", f"The listed numerical/alphabetical strings were found in your password: {matching_words}\n")
    else:
        stringStrength = 0
        output_widget.insert("end", f"The listed numerical/alphabetical strings were found in the original and modified password: {common_strings}\n")

    # calculate average
    overStringStrength = (stringStrength + stringStrengthM) / 2

    # return calculated score
    return(overStringStrength)

# 9. Compare with rockyou.txt * DEBUGGED WITH AI *
def check_rockyou(password, mPassword, output_widget):
    word_strengths = [10, 10]  # [Original password strength, Modified password strength]
    matching_words = []
    matching_words_modified = []

    try:
        with open("rockyou.txt", "r", encoding="utf-8", errors="ignore") as file:
            # Memory-map the file for efficient reading
            with mmap.mmap(file.fileno(), 0, access=mmap.ACCESS_READ) as mmapped_file:
                # begin comparing and adjusting score
                for line in iter(mmapped_file.readline, b""):
                    word = line.decode("utf-8", errors="ignore").strip().lower()

                    if not word or len(word) < 4:
                        continue

                    if word in password.lower() and word not in matching_words:
                        matching_words.append(word)
                        word_strengths[0] = max(0, word_strengths[0] - 1)

                    if word in mPassword.lower() and word not in matching_words_modified:
                        matching_words_modified.append(word)
                        word_strengths[1] = max(0, word_strengths[1] - 1)

    except FileNotFoundError:
        return 0

    # Find common words in both lists
    common_words = list(set(matching_words) & set(matching_words_modified))

    # Output results
    if word_strengths[0] == 10 and word_strengths[1] == 10:
        output_widget.insert("end", "There were no matching passwords in rockyou.txt found in your password.\n")
    elif word_strengths[1] < 10 and word_strengths[0] == 10:
        output_widget.insert("end", "There were matching passwords in rockyou.txt found in your modified password.\n")
    elif word_strengths[0] < 10 and word_strengths[1] == 10:
        output_widget.insert("end", "There were matching passwords in rockyou.txt found in your password.\n")
    else:
        output_widget.insert("end", f"There were matching passwords in rockyou.txt found in both original and modified passwords.\n")

    # Calculate average strength
    over_word_strength = sum(word_strengths) / 2
    return over_word_strength

# 10. Compare with previous inputs
def check_prev(password, mPassword, output_widget):
    word_strengths = [10, 10]  # [Original password strength, Modified password strength]
    matching_words = []
    matching_words_modified = []

    try:
        # open passwords file
        with open("passwords.pickle", "rb") as file:
            entries = pickle.load(file)

        # begin comparing strings
        for entry in entries:
            if entry.password == password:
                # matching_words.append(word)
                word_strengths[0] = max(0, word_strengths[0] - 1)

            if entry.password == mPassword:
                # matching_words_modified.append(word)
                word_strengths[1] = max(0, word_strengths[1] - 1)

    except FileNotFoundError:
        output_widget.insert("end", "No previous passwords saved.\n")
        return 10
    
    # Output results
    if word_strengths[0] == 10 and word_strengths[1] == 10:
        output_widget.insert("end", "There were no matching passwords entered previously.\n")
    elif word_strengths[1] < 10 and word_strengths[0] == 10:
        output_widget.insert("end", "There were matching passwords entered previously found in your modified password.\n")
    elif word_strengths[0] < 10 and word_strengths[1] == 10:
        output_widget.insert("end", "There were matching passwords entered previously found in your password.\n")
    else:
        output_widget.insert("end", f"There were matching passwords entered previously found in both original and modified passwords.\n")
    
    # Calculate average strength
    over_word_strength = sum(word_strengths) / 2
    return over_word_strength


def export_password(output_widget):
    # open dialog for saving file
    file_path = filedialog.asksaveasfilename(
        defaultextension=".txt",
        filetypes=[("Text Files", "*.txt"), ("All files", "*.*")]
    )

    try:
        # save text from file
        if file_path:
            # Retrieve all text from the output widget
            output_text = output_widget.get("1.0", "end-1c")  # Get all text, excluding the trailing newline
            with open(file_path, 'w') as file:
                file.write(output_text)  # Write text to the selected file
            print(f"Output successfully saved to {file_path}")  # Optional: for debugging purposes
    except FileNotFoundError as e:
        messagebox.showerror("Error", f"File not found: {e}")
    except IOError as e:
        messagebox.showerror("Error", f"An I/O error occurred: {e}")
    except Exception as e:
        # Log or display the error message for unexpected exceptions
        error_message = f"An unexpected error occurred: {e}"
        print(error_message)  # Log error to console (optional)
        messagebox.showerror("Error", error_message)
        # Optionally, use sys to print more details about the exception
        sys.print_exception(e)
