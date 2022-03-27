#!/usr/bin/python3

"""Variables

    Settings:
        host: The host we want to ping
        delay: The delay between the pings. Be careful. Dont set the delay to less. 
    """
host = "192.168.151.11" #the host to ping
delay = 1 # delay between the pings in seconds
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
ips = "Will save the hosts from hosts.txt"
current_directory = os.getcwd()
dir = current_directory

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

class hosts:
    def __init__(self, file):
        self.file = file
        self.f = None
    def __enter__(self):
        self.f = open(self.file, "r")
        return self
    def __exit__(self, exc_type, exc_value, traceback):
        self.f.close()

def eintrag(foo, boo, path):
    os.chdir(path)
    with log(start_time + " " + boo + ".txt") as bar:
        bar.eintrag(foo)

def ip():
    global ips
    foo = open('hosts.txt', 'r')
    ips = ""
    for line in foo:
        ips = ips + line
    ips = ips.split('\n')
    res = [bar for bar in ips if bar.strip()]
    ips = res
    foo.close()

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
    try:
        os.chdir(current_directory + "/result")
    except :
        os.mkdir(current_directory + "/result")
    os.chdir(current_directory + "/result")
    try:
        os.chdir(path)
    except :
        os.mkdir(path)


def ping(host):
    foo = "ping -c 1 " + host #+ " | grep = | grep -v rtt"
    return os.popen(foo).read()

def output(foo, host):
    global dir
    try:
        os.chdir('/opt/ping')
    except FileNotFoundError:
        os.chdir(current_directory)
    bar = ping(host)
    bar = bar.strip()
    mkdir(host)
    os.chdir(current_directory + "/result/" + host)
    if lang_index in bar:
        bar = bar.splitlines()
        for line in bar:
            if lang_index in line:
                print(f"{timestamp()} {line}")
                eintrag(timestamp()+ "     " + line, "OK", os.getcwd())
    elif 'erreichbar' in bar:
        print(f"\n\nLeider ging das in die Hose {timestamp()} {bar}\n\n")
        eintrag("\n\n\n" + timestamp()+ "     " + bar, "Time_error", os.getcwd())
    else:
        print(f"\n\nUnbekannter Fehler um {timestamp()} Payload.: \n{bar} \n\n")
        eintrag("\n\n\n" + timestamp() + "     " + bar, "Error", os.getcwd())
    os.chdir(current_directory)

def workingdir(path):
    try:
        mkdir(path)
        os.chdir(path)
    except (FileExistsError):
        os.chdir(path)

def webserv():
    server_object = HTTPServer(server_address=('', port), RequestHandlerClass=CGIHTTPRequestHandler)
    # Start the web server
    server_object.serve_forever()

def set_lang():
    global lang_index
    if lang.upper() == "DE":
        lang_index = "Zeit="
    elif lang.upper() == "EN":
        lang_index = "time="
    else:
        print(f"This language is not supported.")

def run(host):
    try:
        output(count, host)
    except ():
        return 0
    ip()

def main():
    set_lang()
    os.system("clear")
    print("Starting pogram…")
    print(f"")
    print(f"Hit return to exit the program!")
    print(f"")
    ip()
    os.chdir(current_directory)
    server = Thread(target=webserv)
    server.start()
    count = 0
    while i is False:
        time.sleep(delay)
        count += 1
        for foo in ips:
            run(foo)
            os.chdir(current_directory)
        print(f"\n")
    os._exit(0)

main()

