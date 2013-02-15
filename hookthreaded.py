from pydbg import *
from pydbg.defines import *
import logging
import struct
import utils
import sys
import datetime
import threading
import os
from os import system
import platform
import time
import subprocess
snapshot = 'snapshot.py'
path = "C:\Users\\\"7 User\"\\AppData\\\Roaming\\\IMVUClient\\imvuclient.exe"
buffer = ""
def logo():
    print '''
  G#: #  ####tK#    
  #    j#       #   
 ,# D# #; #####.    
  #W # # #W;# W# #  
  #E # # ## # .# #  
  ## # # W# #  : #  
  ## # GE     D ##  
  ##   ########:GG         IMVU Debug Hook
   #####i;##     :            By Exploit
   ##       ;# ## E 
   #, # ## . # ## # 
   ## ### ;# #### # 
   ##  ## ##  ## K# 
    ## GW ###   E#  
    W##  ########.  
     #####   ###    
      E##\npress p to pause execution\npress r to search for a new string\npress q to quit\n'''
def clear_screen():
    platClear = platform.system().lower()
    if platClear == "linux" or platClear == "unix": 
        os.system('clear')
    elif platClear == "windows":
        os.system('cls')
dbg = pydbg()
def printreg():
    print 'EAX is',pydbg.context.Eax
    print pydbg.context.Edp
    print pydbg.context.Esp
    print pydbg.context.Eip
#this code left intentionally undocumented
exe = "imvuclient.exe"
for (pid, name) in dbg.enumerate_processes():
    x = name.lower()
    if x == exe:
        break
    elif x != exe:
        clear_screen()
        print '[*] Making sure imvu isnt running, so we get a clean startup\n'
        system('taskkill/IM imvuclient.exe')
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
class _Getch:    
    def __init__(self):
        try:
            self.impl = _GetchWindows()
        except ImportError:
            self.impl = _GetchUnix()

    def __call__(self): return self.impl()
class _GetchUnix:
    def __init__(self):
        import tty, sys
    def __call__(self):
        import sys, tty, termios
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
class readinput(threading.Thread):
    def run(self):
        for i in xrange(sys.maxint):
            k=inkey()
            if k >='':break
        if k == "q":print '''[!]QUITTING, IMVU WILL CRASH WITH THIS (EXPECTED) ERROR:\n\n\nStructuredException: EXCEPTION_BREAKPOINT(80000003)\nParameters: [Something, Something, Something]\n\n''',os._exit(1)
        if k == "s":
            system('start c:\0xic-zex\Python\imvustuff\snapshot.py',shell = True)
    #if k == "":
def imdbg():
    clear_screen()
    dbg = pydbg()
    found_imvu = False
    logging.basicConfig(filename='hook.log',level=logging.DEBUG)
    logo()
    pattern = raw_input("\n[?] What string to search for? >\n")
    logme = raw_input("\n[?] Would you like to log my output to a text file?  ( y/n )")
    v = raw_input('\n[?] Use verbose mode?(no output at all)(y/n)')
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

        return DBG_CONTINUE
    for (pid, name) in dbg.enumerate_processes():
        if name.lower() == "imvuclient.exe":
            found_imvu = True
            hooks = utils.hook_container()
            dbg.attach(pid)
            print "[!] Attaching to IMVU with PID: %d..." % pid
            hook_address  = dbg.func_resolve_debuggee("nspr4.dll","PR_Write")

            if hook_address:
                hooks.add( dbg, hook_address, 2, ssl_sniff, None)
                print "[*] nspr4.PR_Write hooked at: 0x%08x" % hook_address
                break
            else:
                print "[!] Error: Couldn't resolve hook address."
                sys.exit(-1)


    if found_imvu:   
        print "[*] Hook set, continuing process.\n\n"
        if v == "y":
            print '[*] Verbose mode '
        readinput().start()
        dbg.run()
    else:    
        print "[!] Error: Couldn't find the  process. Please wait while I up IMVU and try again"
        system('start %s'%(path))
        os._exit(-1)
if __name__ == '__main__':
    imdbg()