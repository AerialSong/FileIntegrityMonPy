import json
import hashlib
import smtplib
import json
import os
import datetime
import time
from email.message import EmailMessage
import re

BUF_SIZE = 65536 # 64 KB chunks

def new_baseline():
    # Calculate hash from the target files and store in baseline.txt

    if os.path.exists(jsfile):
        os.remove(jsfile)
    # For each directory within the chosen directory
    # scan each file
    # then move onto the next directory and scan each file there until there are no more deeper directories
    jslist = {}
    for subdir, dirs, files in os.walk(directory):
        for filename in files:
            filehash = hashlib.sha256()
            fn = os.path.join(subdir, filename)
            with open(fn, 'rb') as f:
                while True:
                    data = f.read()
                    if not data:
                        break
                    if data:
                        filehash.update(data)
                f.close()
                hexdigest = filehash.hexdigest()
                jslist.update({fn:hexdigest})
                #print(f"{fn} | {filehash.hexdigest()}", file=f) # Sends the print output to the baseline file
    with open(jsfile, 'w+') as jf:
        json.dump(jslist, jf, indent=4)
    with open(jsfile, 'r') as jf:
        data = json.load(jf)
        for i in data:
            print(i, ':', data[i])

def comp_baseline():
    # Begin (continuously) monitoring files with saved baseline
    if os.path.exists(jsfile): # Load file|hash from baseline.txt and store them in a dictionary
        # Exclude the baseline that is currently being read from
        # Next Step:
        # Don't include Changelog in the scanning. Because it's constantly changing it'll be infinite
        while True:
            for subdir, dirs, files in os.walk(directory):
                for filename in files:
                    fpath = os.path.join(subdir, filename)
                    if 'File_Integrity\changelog.txt' not in fpath:
                        jf = open(jsfile, 'r')
                        # Declares the json data as a value
                        data = json.load(jf)
                        jf.close()
                        for i in data:
                            # Checks if the current file matches the filename in the json data
                            if i == str(fpath):
                                with open(fpath, 'rb') as tf:
                                    test_hash = hashlib.sha256(tf.read())
                                    # The file hash in the json file is compared to the current hash of the file being scanned
                                    # If the hashes do not match, a log will be updated with the changed log
                                    # and the json file will be updated.
                                    if test_hash.hexdigest() == data[i]:
                                        pass
                                    # This elif is because this particular hash always appears in the log and baseline before the actual specified file's hash
                                    # Temporary, dirty solution
                                    elif test_hash.hexdigest() != "e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855" and test_hash.hexdigest() != data[i]:
                                        print("Old hash:\n",data[i], '\n')
                                        print("New Hash:\n",test_hash.hexdigest())
                                        print(f"{i!r} has a non-matching hash.\n")
                                        with open("changelog.txt", 'a') as lf:
                                            lf.write(f'{i} : {test_hash.hexdigest()}\nFile was changed at {datetime.datetime.now()}\n\n')
                                        with open(jsfile, 'r+') as jf:
                                            data[i] = test_hash.hexdigest()
                                            jf.seek(0)
                                            jf.write(json.dumps(data))
                                            jf.truncate()
                                    tf.close()
                    # Consider scanning on an hourly or daily schedule
                    # instead of a continuous real time scan
                    
    else:
        print("Baseline file does not exist in local directory.")


try:
    if __name__ == "__main__":
        print("What would you like to do?\nA) Collect new Baseline?\nB) Begin monitoring files with saved Baseline?\n\n")
        choice = input("Please enter 'A' or 'B': ").upper()
        if choice != 'A' and choice != 'B':
            print("Not a valid option!")
            quit()
        print(f"User has entered: {choice}")
        directory = input("Please enter the filepath of the directory you would like to monitor: ") # Set a directory for file hash scanning
        jsfile = f'{directory}.json'.replace('\\', '_').replace('/', '_').replace(':', '_').replace(' ', '_')
        #baseline = f'baseline_{directory}.txt'.replace('\\', '_').replace('/', '_').replace(':', '_').replace(' ', '_')

        if choice == 'A':
            new_baseline()
        elif choice == 'B':
            comp_baseline()
except KeyboardInterrupt:
    print("\nExiting program...")
