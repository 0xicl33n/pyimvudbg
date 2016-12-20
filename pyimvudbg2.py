#!/usr/bin/env python
#!/c/Python27/python.exe
import platform
import os
from os import system
if "32bit" not in platform.architecture():
    print "You are using a 64bit python installation. This will not work with the debugger\nPlease install 32bit 2.7.x"
    os._exit(-1)
else:
    pass
try:
    from pydbg import *
except ImportError:
    print "\n[!] ERORR - PAIMEI NOT FOUND\n\nPlease get it here:\nhttps://github.com/0xicl33n/paimei"
    os._exit(-1)
try:
    import win32gui,win32con
except ImportError:
    print "\n[!] ERROR - WIN32API NOT FOUND\n\nPlease get it here:\nhttp://sourceforge.net/projects/pywin32/"
    os._exit(-1)
from pydbg.defines import *
import logging
import utils
import sys
import datetime
import threading
from os import system
import time
import getpass
#testing new method of calling the client
import windowsinfo
path = windowsinfo.client()
#import snapshot
#snapit = snapshot.snapshotter()
hwnd = win32gui.GetForegroundWindow()
win32gui.ShowWindow(hwnd, win32con.SW_MAXIMIZE)
user = str(getpass.getuser())
cwd = os.getcwd()
os.system('title IMVU Debugger by Exploit')
snapshot = '%s\\snapshot.exe'%(cwd)
buffer = ""
dbg = pydbg
#cant make this work for some reason
def handler_breakpoint(dbg):
    print '--------------------------------Dumping context'
    print dbg.dump_context()
# register a breakpoint handler function.
def check_accessv(dbg):
    # skip first-chance exceptions
    if dbg.dbg.u.Exception.dwFirstChance:
        pass
    crash_bin = utils.crash_binning.crash_binning()
    crash_bin.record_crash(dbg)
    print crash_bin.crash_synopsis()
    dbg.terminate_process()
#this doesnt work
#dbg.set_callback(EXCEPTION_ACCESS_VIOLATION,check_accessv)
#dbg.set_callback(EXCEPTION_BREAKPOINT, handler_breakpoint)
def logo():print '''
  G#: #  ####tK#    
  #    j#       #   `
 ,# D# #; #####.    
  #W # # #W;# W# #  
  #E # # ## # .# #  
  ## # # W# #  : #  
  ## # GE     D ##  
  ##   ########:GG         IMVU nspr4.dll hook
   #####i;##     :            By Exploit
   ##       ;# ## E              2.2-dev
   #, # ## . # ## # 
   ## ### ;# #### # 
   ##  ## ##  ## K# 
    ## GW ###   E#  
    W##  ########.  
     #####   ###    
      E##\npress p to pause execution\t(experimental)\npress r to search for a new string(experimental)\npress s to open the snapshotter\t(experimental)\npress d to dump registars\t(experimental)\npress q to quit\n'''
def clear_screen():
    platClear = platform.system().lower()
    if platClear == "linux" or platClear == "unix": 
        os.system('clear')
    elif platClear == "windows":
        os.system('cls')
exe = "imvuclient.exe"
for (pid, name) in dbg.enumerate_processes():
    x = name.lower()
    if x == exe:
        break
    elif x != exe:
        clear_screen()
        print '[*] Making sure imvu isnt running, so we get a clean startup\n'
        dbg.detach()
        system('taskkill /F /IM imvuclient.exe')
        print '\n[*] Wait about 5 seconds while we start IMVU, alright?'
        system('start %s'%(path))
        time.sleep(2)
        print '3....'
        time.sleep(1)
        print '2...'
        time.sleep(1)
        print '1...'
        break
now = datetime.datetime.now()
#getch allows commands to be sent to the program as its running (supposedly)
class _Getch:    
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()
    def __call__(self): return self.impl()
class _GetchUnix:
    def __init__(self):
        import tty
    def __call__(self):
        import termios
        fd = sys.stdin.fileno()
        old_settings = termios.tcgetattr(fd)
        try:
            tty.setraw(sys.stdin.fileno())
            ch = sys.stdin.read(1)
        finally:
            termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
        return ch
class _GetchWindows:
    def __init__(self):
        import msvcrt

    def __call__(self):
        import msvcrt
        return msvcrt.getch()
inkey = _Getch()
#getch results
class readinput(threading.Thread):
    def run(self):
        for i in xrange(sys.maxint):
            k=inkey()
            if k >='':break
        if k == "q":
            print '''[!]QUITTING, IMVU WILL CRASH WITH THIS (EXPECTED) ERROR:\n\n\nStructuredException: EXCEPTION_BREAKPOINT(80000003)\nParameters: [Something, Something, Something]\n\n''',system('pause'),os._exit(1)
        if k == "s":
            print '[*] To do snapshots we have to reopen and reattach'
            system('taskkill /IM imvuclient.exe')
            system('start %s'%(snapshot))
            imdbg()
        if k == "r":
            dbg.detach()
            dbg.attach(int(pid))
            pattern = None
            imdbg()
        #having trouble with this
        if k == "d":
            handler_breakpoint(pid)
#this is main
def imdbg():
    clear_screen()
    found_imvu = False
    logging.basicConfig(filename='hook.log',level=logging.DEBUG)
    logo()
    #this isnt needed 
    #print 'Python',(sys.version),'\n'
    pattern = raw_input("\n[?] What string to search for? >\n")
    #20151001 - added error checking, previously entering nothing would cause the program to not work
    if pattern =="":
        print "[!] Please enter a string"
        imdbg() #iterate back to main
        #run_nopattern() will come at a later date
    logme = raw_input("\n[?] Would you like to log my output to a text file?  ( y/n )")
    if logme =="":
        print "[!] Please enter a string"
        imdbg()
    v = raw_input('\n[?] Use verbose mode?(no output at all)(y/n)')
    if v =="":
        print "[!] Please enter a string"
        imdbg()
    if logme == "y":
        print "[@] OUTPUT LOGGING ENABLED!"
        print "[@] Placing search string in log..."
        logging.debug("Searched on %s for the string: %s" % (now,pattern))
    print '\n[!] Searching for pattern: %s'% (pattern)
    def ssl_sniff( dbg, args ):
        buffer  = ""
        offset  = 0

        while 1:
            byte = dbg.read_process_memory( args[1] + offset, 1 )
            if byte != "\x00":
                buffer  += byte
                offset  += 1
                continue
            else:
                break           
        if v == "y":
            logging.debug("[>] Pre-Encrypted:  %s %s" %(now,buffer) )
        else:
            if pattern in buffer:
                if logme == "y":
                    logging.debug("[>] Pre-Encrypted:  %s %s" %(now,buffer) )
                    print "[>] Pre-Encrypted: %s" % buffer
                else:
                    print "[>] Pre-Encrypted: %s" % buffer
    for (pid, name) in dbg.enumerate_processes():
        if name.lower() == "imvuclient.exe":
            found_imvu = True
            hooks = utils.hook_container()
            dbg.set_callback(check_accessv)
            dbg.attach(int(pid))
            print "[!] Attaching to IMVU with PID: %d..." % pid
            hook_address  = dbg.func_resolve_debuggee("nspr4.dll","PR_Write")

            if hook_address:
                hooks.add( dbg, hook_address, 2, ssl_sniff, None)
                print "[*] nspr4.PR_Write hooked at: 0x%08x" % hook_address
                break
            else:
                print "[!] Error: Couldn't resolve hook address."
                dbg.detach()
                print "[!] Error: Couldn't find the  process. Please wait while I fire up IMVU and try again"
                system('start %s'%(path))
                imdbg()
    if found_imvu:   
        print "[*] Hook set, continuing process.\n\n"
        if v == "y":
            print '[*] Verbose mode '
            readinput().start()
            dbg.run()
        else:
            readinput().start()
            dbg.run()
    else:    
        print "[!] Error: Couldn't find the  process. Please wait while I fire up IMVU and try again"
        system('start %s'%(path))
        system('pause')
        imdbg()
if __name__ == '__main__':
    while 1:
        imdbg()
