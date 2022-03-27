#!/usr/bin/python3

"""Variables

    Settings:
        host: The host we want to ping
        delay: The delay between the pings. Be careful. Dont set the delay to less. 
    """
host = "pi.gringer" #the host to ping
delay = 1 # delay between the pings
lang = "de" # "DE" os "EN"
port = 8000 # The http serverport to open the download from the logs 

import os
import time
import sys
from threading import Thread
from http.server import HTTPServer, CGIHTTPRequestHandler

"""Some variables that not have to be changed

        start_time: Point the start of the session
        count: startpoint for the ping counter
    """
start_time = time.strftime("%Y_%m_%d  %H:%M")
count = 0
i = False
lang_index = "Will override with the language settings" 

class log:
    def __init__(self, logfile):
        self.logfile = logfile
        self.f = None
    def eintrag(self, logtext):
        self.f.write("{}\n".format(logtext))
    def __enter__(self):
        self.f = open(self.logfile, "a")
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.f.close()

def eintrag(foo, boo):
    with log(start_time + " " + boo + ".txt") as bar:
        bar.eintrag(foo)

def listen():
    global i
    input()
    i = True
listener = Thread(target=listen)
listener.start()

def timestamp():
    foo = time.localtime()
    return time.asctime(foo)

def mkdir(path):
    os.mkdir(path)
    
def chdir(path):
    os.chdir(path)

def ping(host):
    foo = "ping -c 1 " + host #+ " | grep = | grep -v rtt"
    time.sleep(delay)
    return os.popen(foo).read()

def output(foo):
    bar = ping(host)
    bar = bar.strip()
    if lang_index in bar:
        bar = bar.splitlines()
        for line in bar:
            if lang_index in line:
                print(f"{timestamp()} {line}")
                eintrag(timestamp()+ "     " + line, "OK")
    elif 'erreichbar' in bar:
        print(f"\n\nLeider ging das in die Hose {timestamp()} {bar}\n\n")
        eintrag("\n\n\n" + timestamp()+ "     " + bar, "Time_error")
    else:
        print(f"\n\nUnbekannter Fehler um {timestamp()} Payload.: \n{bar} \n\n")
        eintrag("\n\n\n" + timestamp() + "     " + bar, "Error")

def workingdir(path):
    try:
        mkdir(path)
        chdir(path)
    except (FileExistsError):
        chdir(path)

def webserv():
    server_object = HTTPServer(server_address=('', port), RequestHandlerClass=CGIHTTPRequestHandler)
    # Start the web server
    server_object.serve_forever()
server = Thread(target=webserv)
server.start()

def set_lang():
    global lang_index
    if lang.upper() == "DE":
        lang_index = "Zeit="
    elif lang.upper() == "EN":
        lang_index = "time="
    else:
        print(f"This language is not supported.")

def main():
    set_lang()
    os.system("clear")
    print("Starting pogram…")
    print(f"")
    print(f"Hit return to exit the program!")
    print(f"")
    try:
        count = 0
        workingdir(host)
        while i is False:
            count += 1
            output(count)
    except ():
        return 0
    os._exit(0)

main()
