import tkinter as tk
import os
import shutil
from tkinter import filedialog

# end of imports!
#--------------------------------------------------------------------------------------------------------- end of imports!
# start of vacriable definitions

Loop_started = (False)
Unrealengineoutput = ("")
Mods_folderloc = ("")
Modname = ("Test_P")


# end of variable definitions!
#--------------------------------------------------------------------------------------------------------- end of variable definitions!
# start of functions

def scan_for_unreal_builds(directory): # scand for unreal engine builds
    target_names = {"Windows", "WindowsNoEditor"}
    matches = []

    for root, dirs, files in os.walk(directory):
        for name in dirs:
            if name in target_names:
                full_path = os.path.join(root, name)
                matches.append(full_path)
        return matches
    
#--------------------------------------------------------

def collect_filtered_contents(target_path): # collects all files inside the unreal engine build and filters out unwanted files and folders.
    all_items = []

    for root, dirs, files in os.walk(target_path):
        # Filter out 'Engine' folders
        dirs[:] = [d for d in dirs if d.lower() != "engine"]

        # Add remaining folders
        for d in dirs:
            all_items.append(os.path.join(root, d))

        # Filter out .exe and .txt files
        for f in files:
            if not (f.lower().endswith(".exe") or f.lower().endswith(".txt")):
                all_items.append(os.path.join(root, f))

    return all_items

#--------------------------------------------------------

def further_filter_dirs_with_paks(paths): # further filters the collected folders down to only the paks folder
    filtered = []

    for path in paths:
        # Check if "Paks" exists inside this directory
        paks_path = os.path.join(path, "Paks")
        if os.path.isdir(paks_path):
            filtered.append(path)

    return filtered

#--------------------------------------------------------

def find_pak_files(base_directory): #finds all of the mod files we wish to be packaged and saves their directories to a list.
    target_extensions = {".pak", ".utoc", ".ucas"}
    matched_files = []

    for root, dirs, files in os.walk(base_directory):
        for file in files:
            name_lower = file.lower()
            if "50" in name_lower:
                ext = os.path.splitext(file)[1].lower()
                if ext in target_extensions:
                    full_path = os.path.join(root, file)
                    matched_files.append(full_path)

    return matched_files

#--------------------------------------------------------

def restartloop(): # restarts the loop if the loop is still supposed to be on.
    global Loop_started
    if Loop_started == True:
        loopingfunction()

#--------------------------------------------------------

def rename_and_move_to_test_p(pakfilelist, destination_folder): # renames and moves the mod files to the target mods folder.
    global Modname
    if not os.path.isdir(destination_folder):
        print(f"Destination folder does not exist: {destination_folder}")
        return

    for original_path in pakfilelist:
        _, ext = os.path.splitext(original_path)
        new_path = os.path.join(destination_folder, f"{Modname}{ext}")

        # If file already exists, overwrite it
        try:
            shutil.copy2(original_path, new_path)
            print(f"Moved and renamed: {original_path} → {new_path}")
        except Exception as e:
            print(f"Failed to move {original_path}: {e}")

#--------------------------------------------------------

def loopingfunction(): # the main looping function that runs once a second to check if there are any new mod files that need to be renamed and moved.
    global Loop_started
    print("looping function exicuted!")
    print("---------------------------------------------------------------------------------------------------------------------")
    foundwindowsfolder = scan_for_unreal_builds(Unrealengineoutput)
    if not foundwindowsfolder:
        root.after(1000, restartloop)
        return
    print(foundwindowsfolder)
    print("space")
    unrealprojectnamedir = collect_filtered_contents(foundwindowsfolder[0])
    if not unrealprojectnamedir:
        root.after(1000, restartloop)
        return
    print(unrealprojectnamedir)
    print("space")
    furtherfiltered = further_filter_dirs_with_paks(unrealprojectnamedir)
    if not furtherfiltered:
        root.after(1000, restartloop)
        return
    print(furtherfiltered)
    print("space")
    fullpaksdir = (furtherfiltered[0] + "\\Paks")
    print(fullpaksdir)
    print("space")
    pakfilelist = find_pak_files(fullpaksdir)
    if not pakfilelist:
        root.after(1000, restartloop)
        return
    print(pakfilelist)
    print("space")
    rename_and_move_to_test_p(pakfilelist, Mods_folderloc)
    for file_path in pakfilelist:
        try:
            os.remove(file_path)
            print(f"Deleted: {file_path}")
        except Exception as e:
            print(f"Failed to delete {file_path}: {e}")
    root.after(1000, restartloop)
    
#--------------------------------------------------------

def OnProgramstart(): # toggels whether the main loop function above is running or not.
    global Loop_started
    if Loop_started == False:
        Loop_started = True
        isrunning.set("program is running!")
    else:
        Loop_started = False
        isrunning.set("program is not running.")
    print("loop toggeled to " + str(Loop_started))
    if Loop_started == True:
        loopingfunction()

#--------------------------------------------------------
    
def Opencookdirectory():
    global Unrealengineoutput
    print("cook directory opened.")
    folder_path = filedialog.askdirectory(
        title="Select a folder"
    )
    if folder_path:
        Unrealengineoutput = (folder_path)
        print(f"Selected file: {Unrealengineoutput}")
        Unreal_directory_var.set(Unrealengineoutput)

#--------------------------------------------------------
def OpenModsdir():
    global Mods_folderloc
    print("cook directory opened.")
    folder_path = filedialog.askdirectory(
        title="Select a folder"
    )
    if folder_path:
        Mods_folderloc = (folder_path)
        print(f"Selected file: {Mods_folderloc}")
        Mods_folderdir.set(Mods_folderloc)

#--------------------------------------------------------


# end of function definitions!
#---------------------------------------------------------------------------------------------------------end of function definitions!
# Random hello world I guess XD.

print("Hello World")

#Random hello world I guess XD.
#------------------------------------------------------------------------------Random hello world I guess XD.
#start of the user interfact code.

root = tk.Tk()
root.title("ModAutoDeploy")

label = tk.Label(root, text="ModAutoDeploy V1.0", font=("Arial", 16))
label.pack()

label = tk.Label(root, text="----------------------------------------------------------------------------------------------------------------------------------------")
label.pack()

button = tk.Button(root, text="       Toggle Program       ",font=("Arial", 14), command=OnProgramstart)
button.pack(expand=True)

isrunning = tk.StringVar()
isrunning.set("program is not running")

directory_label = tk.Label(root, textvariable=isrunning)
directory_label.pack()

label = tk.Label(root, text="----------------------------------------------------------------------------------------------------------------------------------------")
label.pack()

#------------------------------------------------------------------------------cooked file directory button

button = tk.Button(root, text="       Open packaging directory       ",font=("Arial", 14), command=Opencookdirectory)
button.pack(expand=True)

#defines a modifiable variable for the unreal directory.
Unreal_directory_var = tk.StringVar()
Unreal_directory_var.set("unreal directory will be shown here")

directory_label = tk.Label(root, textvariable=Unreal_directory_var)
directory_label.pack()
#END defines a modifiable variable for the unreal directory.


label = tk.Label(root, text="----------------------------------------------------------------------------------------------------------------------------------------")
label.pack()

#------------------------------------------------------------------------------FSB2target file directory button

button = tk.Button(root, text="       Open target Mods folder       ",font=("Arial", 14), command=OpenModsdir)
button.pack(expand=True)

#defines a modifiable variable for the unreal directory.
Mods_folderdir = tk.StringVar()
Mods_folderdir.set("mods folder directory will be shown here")

directory_label = tk.Label(root, textvariable=Mods_folderdir)
directory_label.pack()
#END defines a modifiable variable for the unreal directory.

label = tk.Label(root, text="----------------------------------------------------------------------------------------------------------------------------------------")
label.pack()

#------------------------------------------------------------------------------

# Create a Text widget
textbox = tk.Text(root, height=2, width=30, font=("Arial", 14))
textbox.pack(padx=10, pady=10)


# Optional: Insert default text
textbox.insert(tk.END, "Test_P")

def read_text():
    global Modname
    content = textbox.get("1.0", tk.END).strip()
    Modname = (content)
    currentmodname.set(content)

tk.Button(root, text="Apply Modname",font=("Arial", 14), command=read_text).pack()

label = tk.Label(root, text="")
label.pack()

label = tk.Label(root, text="Current mod name:",font=("Arial", 14))
label.pack()

currentmodname = tk.StringVar()
currentmodname.set("Test_P")

directory_label = tk.Label(root, textvariable=currentmodname, font=("Arial", 14))
directory_label.pack()

label = tk.Label(root, text="")
label.pack()

label = tk.Label(root, text="----------------------------------------------------------------------------------------------------------------------------------------")
label.pack()

label = tk.Label(root, text="Made by The Human Cookieman",font=("Arial", 14))
label.pack()

#------------------------------------------------------------------------------

root.geometry("700x550") # sets the window size

root.mainloop() # runs the program window