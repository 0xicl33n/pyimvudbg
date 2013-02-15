from pydbg import *
from pydbg.defines import *
import logging
import struct
import utils
import sys
import datetime
import threading
found_imvu = False
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
getch = _Getch()
#this code left intentionally undocumented
dbg           = pydbg()
inkey = _Getch()
logging.basicConfig(filename='hook.log',level=logging.DEBUG)
class readinput(threading.Thread):
    def run():
        for i in xrange(sys.maxint):
            k=inkey()
            if k >='':break
        if k == "q":print "QUITTING! IMVU WILL PROBABLY CRASH!",sys.exit(-1)
   # if k == "r":
    #if k == "":
def debug():
    print "\n\nIMVU HOOK by Exploit\n\n\n\n"
    print "press p to pause execution\npress r to search for a new string\npress q to quit\n\n^ none of these work yet..."
    pattern       = raw_input("\n\n[?] What string to search for? >   \n")
    logme = raw_input("\n[?] Would you like to log my output to a text file?  ( y/n )")
#readinput() 
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
        dbg.run()
    else:    
        print "[!] Error: Couldn't find the  process. Please fire up IMVU first."
        sys.exit(-1)
if __name__ == '__main__':
    debug()