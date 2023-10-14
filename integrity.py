import hashlib
import smtplib
import os
import time
from email.message import EmailMessage
import re

BUF_SIZE = 65536 # 64 KB chunks

def new_baseline():
    # Calculate hash from the target files and store in baseline.txt

    if os.path.exists(baseline):
        os.remove(baseline)
    for filename in os.listdir(directory):
        filehash = hashlib.sha256()
        fn = os.path.join(directory, filename)
        with open(fn, 'rb') as f:
            while True:
                data = f.read()
                if not data:
                    break
                if data:
                    filehash.update(data)
            f.close()
        f = open(baseline, 'a')
        print(f"{fn} | {filehash.hexdigest()}", file=f) # Sends the print output to the baseline file
        print(f"{fn} | {filehash.hexdigest()}")

        f.close()

def comp_baseline():
    # Begin (continuously) monitoring files with saved baseline
    base_dict = {}
    if os.path.exists(baseline): # Load file|hash from baseline.txt and store them in a dictionary
        with open(baseline, 'r') as f:
            for line in f.readlines():
                fp, filehash = line.split(" | ")
                filehash = filehash.rstrip()
                print(filehash, '\n')
                # fp is a file path name
                # with fp, read each line of the relevant baseline
                for filename in os.listdir(directory):
                    fpath = os.path.join(directory, filename)
                    # check if the current fp matches any of the files in the directory
                    # if it DOES: start an if statement
                    if fp == str(fpath):
                        with open(fpath, 'rb') as tf:
                            test_hash = hashlib.sha256(tf.read())
                            print(test_hash.hexdigest())
                            if test_hash.hexdigest() == filehash:
                                print(f"{fp!r} has a matching hash.\n")
                            else:
                                print(f"{fp!r} has a non-matching hash.\n")

        # Compare current file: hash to dictionary to check if it's in there
        # if not, it means the file does not exist
        # if the file exists but the hash is different, the file has been compromised     
                    
    else:
        print("Baseline file does not exist in local directory.")



if __name__ == "__main__":
    print("What would you like to do?\nA) Collect new Baseline?\nB) Begin monitoring files with saved Baseline?\n\n")
    choice = input("Please enter 'A' or 'B': ").upper()
    directory = input("Please enter the filepath of the directory you would like to monitor: ") # Set a directory for file hash scanning
    baseline = f'baseline{directory}.txt'.replace('/', '_')
    if choice != 'A' and choice != 'B':
        print("Not a valid option!")
        quit()

    if choice == 'A':
        new_baseline()
    elif choice == 'B':
        comp_baseline()

    print(f"User has entered: {choice}")
