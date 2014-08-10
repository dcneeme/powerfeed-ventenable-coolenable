#!/usr/bin/python

APVER='energy_starman 09.08.2014' # for olinuxino

#####################################################

import logging
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG) # change as needed ##################

import os

# env variable HOSTNAME should be set before starting python
try:
    print('HOSTNAME is',os.environ['HOSTNAME'])
    # FIXME set OSTYPE
except:
    os.environ['HOSTNAME']='olinuxino' # to make sure it exists on background of npe too
    print('set HOSTNAME to '+os.environ['HOSTNAME'])
    
OSTYPE='archlinux'
print('OSTYPE',OSTYPE)   

from droidcontroller.udp_commands import * # sellega alusta, kaivitab ka SQlgeneral
from droidcontroller.loadlimit import * # load limitation level 0..3 to be calculation

p=Commands(OSTYPE) # setup and commands from server
r=RegularComm(interval=120) # variables like uptime and traffic, not io channels
l=LoadLimit(currentlevel=3, maxlevel=3, \
            leveldelay=30, \
          currentdelay=10, \
              lo_limit=180000, \
              hi_limit=200000, phasecount=3)
# use l.set_lo_limit(value_mA) to set another limit

if os.environ['HOSTNAME'] == 'server': # test linux  
    mac_ip=p.subexec('./getnetwork.sh',1).decode("utf-8").split(' ')
    mac='000101100002' # replace! CHANGE THIS!
    log.warning('replaced mac to',mac_ip)
elif os.environ['HOSTNAME'] == 'olinuxino':
    mac_ip=p.subexec('/root/d4c/getnetwork.sh',1).decode("utf-8").split(' ')
elif os.environ['HOSTNAME'] == 'techbase':
    mac_ip=p.subexec('/mnt/nand-user/d4c/getnetwork.sh',1).decode("utf-8").split(' ')
else:
    log.critical('unknown hostname! cannot start!')
    time.sleep(60)
    sys.exit()
    
print('mac ip',mac_ip)
mac=mac_ip[0]
ip=mac_ip[1]
r.set_host_ip(ip)

udp.setID(mac) # env muutuja kaudu ehk parem?
tcp.setID(mac) # 
udp.setIP('195.222.15.51') # ('46.183.73.35') # mon server ip. only 195.222.15.51 has access to starman
udp.setPort(44445)

from droidcontroller.acchannels import *
from droidcontroller.dchannels import *

# the following instances are subclasses of SQLgeneral.
d=Dchannels(readperiod = 0, sendperiod = 180) # di and do. immediate notification, read as often as possible.
ac=ACchannels(in_sql = 'aicochannels.sql', readperiod = 5, sendperiod = 30) # counters, power. also 32 bit ai! trigger in aichannels

s.check_setup('aicochannels')
#s.check_setup('dichannels')
#s.check_setup('counters')

s.set_apver(APVER) # set version


# functions

def comm_doall():
    ''' Handle the communication with io channels via modbus and the monitoring server  '''
    udp.unsent() # vana jama maha puhvrist
    d.doall()  #  di koik mis vaja, loeb tihti, raporteerib muutuste korral ja aeg-ajalt asynkroonselt
    ac.doall() # ai koik mis vaja, loeb ja vahel raporteerib
    for mbi in range(len(mb)): # check modbus connectivity
        mberr=mb[mbi].get_errorcount()
        if mberr > 0: # errors
            print('### mb['+str(mbi)+'] problem, errorcount '+str(mberr)+' ####')
            time.sleep(2) # not to reach the errorcount 30 too fast!
                        
    r.regular_svc(svclist = ['ULW','UTW','ip']) # UTW,ULW are default. also forks alive processes!
    got = udp.comm() # loeb ja saadab udp, siin 0.1 s viide sees. tagastab {} saadud key:value vaartustega
    if got != {} and got != None: # got something from monitoring server
        ac.parse_udp(got) # chk if setup or counters need to be changed
        d.parse_udp(got) # chk if setup ot toggle for di
        todo=p.parse_udp(got) # any commands or setup variables from server?
        
        
        
        
        # a few command to make sure they are executed even in case of udp_commands failure
        if todo == 'REBOOT':
            stop = 1 # kui sys.exit p sees ei moju millegiparast
            print('emergency stopping by main loop, stop=',stop)
        if todo == 'FULLREBOOT':
            print('emergency rebooting by main loop')
            p.subexec('reboot',0) # no []
        # end making sure 
        
        #print('main: todo',todo) # debug
        p.todo_proc(todo) # execute other possible commands
        
        
def app_doall():
    ''' Application rules and logic for energy metering and consumption limiting, via services if possible  '''
    A2W = s.get_value('A2W','aicochannels')
    current = A2W[0:3] # phase currents mA
    lo_limit = A2W[3]
    hi_limit = A2W[4]
    # if l.get_lo_limit() != lo_limit:
    #    l.set_lo_limit()
    # if l.get_hi_limit() != hi_limit:
    #    l.set_hi_limit(hi_limit)
    
    print('current',current) 
    log.info('current')
    limitlevel = l.output(current) # 0..3 (from no limits to max)
    # set limitlevel service values
    s.set_membervalue('LLW', member=1, value=limitlevel, table='aicochannels') # KoormusPiirang
    #set outputs to disconnect loads if needed
    mitsustate = s.getbit_do(mbi=0, mba=1, regadd=0, bit=9) # mitsu deactivation state
    if mitsustate == None:
        log.warning('invalid dochannels, missing record for bit 9?')
    if limitlevel > 0:
        mitsuoff = 1
    else:
        mitsuoff = 0
    if mitsustate != mitsuoff:
        s.setbit_do(bit=9, value=mitsuoff, mba=1, regadd=0, mbi=0) # deactivate mitsu cooler
        print('limitlevel ' + str(limitlevel) + ', mitsu cooler state change from ' + str(mitsustate) + ' to ' + str(mitsuoff))
    
    

def crosscheck(): # FIXME: should be autoadjustable to the number of counter state channels RxyV
    ''' Report failure states (via dichannels) depending on other states (from counters for example) '''
    pass
    
    
 ################  MAIN #################
ts=time.time() # needed for manual function testing
LRW_ts=ts
A1W=[]
A2W=[]
A2limited=0
R2value=[0,0,0]

if __name__ == '__main__':
    #kontrollime energiamootjate seisusid. koik loendid automaatselt?
    msg=''
    stop=0
    
    # saada apver jaj taasta valgustuse olek reboodi korral
    sendstring="AVV:"+APVER+"\nAVS:0\nLRW:?\nLSW:?"  # taastame moned seisud serverist
    udp.udpsend(sendstring)
    

    while stop == 0: # endless loop 
        ts=time.time() # global for functions
        comm_doall()  # communication with io and server
        app_doall() # application rules and logic, via services if possible 
        #crosscheck() # check for phase consumption failures 
        # #########################################
        
        if len(msg)>0:
            print(msg)
            udp.syslog(msg)
            msg=''
        #time.sleep(1)  # main loop takt 0.1, debug jaoks suurem / jookseb kinni kui viidet pole? subprocess?
        sys.stdout.write('.') # dot without newline for main loop
        sys.stdout.flush()        
    # main loop end, exit from application