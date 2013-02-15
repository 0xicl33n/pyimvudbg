from pydbg import *
from pydbg.defines import *
import logging
import struct
import utils
import sys

#this code left intentionally undocumented
dbg           = pydbg()
found_imvu = False
print "\n\nIMVU HOOK by Exploit\n\n\n\n"
pattern       = raw_input("\n[?] What string to search for? >   \n")
logme = raw_input("\n[?] Would you like to log my output to a text file?  ( y/n )")
#readinput() 
print '\n[!] Searching for pattern:%s'%(pattern)
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
        logging.basicConfig(filename='hook.log',level=logging.DEBUG)
        logging.debug("Pre-Encrypted: %s" % buffer)
        print "Pre-Encrypted: %s" % buffer

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
    print "[*] Hook set, continuing process."
    dbg.run()
else:    
    print "[!] Error: Couldn't find the  process. Please fire up IMVU first."
    sys.exit(-1)
