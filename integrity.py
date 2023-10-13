import hashlib
import smtplib
import os
import time
from email.message import EmailMessage
import re

BUF_SIZE = 65536 # 64 KB chunks

directory = "/home/kali/Documents/test_files" # Set a directory for file hash scanning. Can be determined by user in main() function

def new_baseline():
    # Calculate hash from the target files and store in baseline.txt

    if os.path.exists("baseline.txt"):
        os.remove("baseline.txt")
    for filename in os.listdir(directory):
        filehash = hashlib.sha256()
        fn = os.path.join(directory, filename)
        with open(fn, 'rb') as f:
            while True:
                data = f.read()
                #print(data)
                if not data:
                    break
                if data:
                    #data = data.encode(encoding = 'UTF-8', errors = 'strict')
                    filehash.update(data)
                    #filehash(data.encode('utf-8')).update(data)
            f.close()
        f = open('baseline.txt', 'a')
        print(f"{fn} | {filehash.hexdigest()}", file=f) # Sends the print output to the baseline file
        print(f"{fn} | {filehash.hexdigest()}")

        f.close()

def comp_baseline():
    # Begin (continuously) monitoring files with saved baseline
    base_dict = {}
    if os.path.exists("baseline.txt"): # Load file|hash from baseline.txt and store them in a dictionary
        with open("baseline.txt", 'r') as f:
            for line in f.readlines():
                fp, filehash = line.split(" | ")
                re.sub('\n', '', filehash)
                print(filehash)
                # fp is a file path name
                # with fp, read each line of baseline.txt
                for filename in os.listdir(directory):
                    fpath = os.path.join(directory, filename)
                    # check if the current fp matches any of the files in the directory
                    # if it DOES: start an if statement
                    if fp == str(fpath):
                        with open(fpath, 'rb') as tf:
                            test_hash = hashlib.sha256(tf.read())
                            print(test_hash.hexdigest())
                            if test_hash.hexdigest() == filehash:
                                print(f"{fp!r} has a matching hash.")
                            else:
                                print(f"{fp!r} has a non-matching hash")

        # Compare current file: hash to dictionary to check if it's in there
        # if not, it means the file does not exist
        # if the file exists but the hash is different, the file has been compromised     
                    
    else:
        print("Baseline file does not exist in local directory.")



if __name__ == "__main__":
    print("What would you like to do?\nA) Collect new Baseline?\nB) Begin monitoring files with saved Baseline?\n\n")
    choice = input("Please enter 'A' or 'B': ").upper()
    if choice != 'A' and choice != 'B':
        print("Not a valid option!")
        quit()

    if choice == 'A':
        new_baseline()
    elif choice == 'B':
        comp_baseline()

    print(f"User has entered: {choice}")
