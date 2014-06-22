#!/usr/bin/python
# compatible with both python 2 and 3, tested on olinuxino

APVER='main_starman 14mai2014' # tested on olinuxino and python3

import os
# env variable HOSTNAME should be set before starting python
try:
    print('HOSTNAME is '+os.environ['HOSTNAME'])
except:
    os.environ['HOSTNAME']='olinuxino' # techbase # to make sure it exists on background of npe too
    print('no HOSTNAME, set to '+os.environ['HOSTNAME'])
    
from droidcontroller.udp_commands import * # start with this, also invokes SQlgeneral
p=Commands() # setup and commands from server
r=RegularComm() # variables like uptime and traffic, not io channels



if os.environ['HOSTNAME'] == 'server': # test linux  
    #mac_ip=p.subexec('./getnetwork.sh',1).decode("utf-8").split(' ')
    mac_ip=['000101100002','10.0.0.253'] 
    
elif os.environ['HOSTNAME'] == 'olinuxino':
    mac_ip=p.subexec('/root/d4c/getnetwork.sh',1).decode("utf-8").split(' ')
elif os.environ['HOSTNAME'] == 'techbase':
    mac_ip=p.subexec('/mnt/nand-user/d4c/getnetwork.sh',1).decode("utf-8").split(' ')
else:
    print('no mac_ip variable! exiting')
    sys.exit()
    
print('mac ip',mac_ip)
mac=mac_ip[0]
ip=mac_ip[1]
r.set_host_ip(ip)

udp.setID(mac) # env muutuja kaudu ehk parem?
tcp.setID(mac) # calendar is here too
udp.setIP('46.183.73.35')
udp.setPort(44445)

from droidcontroller.achannels import *
from droidcontroller.cchannels import *
from droidcontroller.dchannels import *

# the following instances are subclasses of SQLgeneral. why?
a=Achannels() # both ai and ao
print(a) # debug, kas v avab sama instance?
d=Dchannels() # di and do 
c=Cchannels() # counters, power

s.check_setup('aichannels')
s.check_setup('dichannels')
s.check_setup('counters')

s.set_apver(APVER) # set version

from vent_starman import *  # the application-specific part. setup is here too.
v=VentStarman()


#functions for main

def comm_doall():
    ''' Handle the communication with io channels via modbus and the monitoring server  '''
    udp.unsent() # vana jama maha puhvrist
    d.doall()  #  di koik mis vaja, loeb tihti, raporteerib muutuste korral ja aeg-ajalt asynkroonselt
    c.doall() # loeb ja vahel ka raporteerib
    a.doall() # ai koik mis vaja, loeb ja vahel raporteerib
    r.regular_svc(svclist = ['ULW','UTW','ip']) # UTW,ULW are default
    got = udp.comm() # loeb ja saadab udp, siin 0.1 s viide sees. tagastab {} saadud key:value vaartustega
    if got != None:
        print(got) # debug
        todo=p.parse_udp(got) # any commands or setup varioables from server?
        
        # a few command to make sure they are executed even in case of udp_commands failure
        if todo == 'REBOOT':
            stop = 1 # kui sys.exit p sees ei moju millegiparast
            print('emergency stopping by main loop, stop=',stop)
        if todo == 'FULLREBOOT':
            print('emergency rebooting by main loop')
            p.subexec(['reboot'],0)
        # end making sure 
        
        #print('main: todo',todo) # debug
        p.todo_proc(todo) # execute other possible commands


    
 ################  MAIN #################
ts=time.time() # needed for manual function testing
LRW_ts=ts


if __name__ == '__main__':
    msg=''
    stop=0
    
    # send APVER and restores some values based on data sent to server before the restart
    sendstring="AVV:"+APVER+"\nAVS:0\nLRW:?\nLSW:?"  # taastame moned seisud serverist
    udp.udpsend(sendstring)


    while stop == 0: # endless loop begin
        ts=time.time() # global for functions
        comm_doall()  # communication with io and server
        v.doall() # application specific rules and logic
        # #########################################
        
        if len(msg)>0:
            print(msg)
            udp.syslog(msg)
            msg=''
        
        if ts > tcp.get_ts_cal() + 3600:
            print('going to check calendar')
            tcp.get_calendar(mac) # stores into local table 'calendar'
        
        #time.sleep(1)  # main loop takt 0.1, debug jaoks suurem / jookseb kinni kui viidet pole?
        sys.stdout.write('.') # dot without newline for main loop
        sys.stdout.flush()        
    # main loop end, exit from application