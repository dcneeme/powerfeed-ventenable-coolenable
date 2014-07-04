#!/usr/bin/python

APVER='energy_starman' # for olinuxino

#####################################################

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

from droidcontroller.udp_commands import * # sellega alusta, kakaivitab ka SQlgeneral
p=Commands(OSTYPE) # setup and commands from server
r=RegularComm(interval=120) # variables like uptime and traffic, not io channels

if os.environ['HOSTNAME'] == 'server': # test linux  
    mac_ip=p.subexec('./getnetwork.sh',1).decode("utf-8").split(' ')
    mac='000101100002' # replace! CHANGE THIS!
    print('replaced mac to',mac_ip)
elif os.environ['HOSTNAME'] == 'olinuxino':
    mac_ip=p.subexec('/root/d4c/getnetwork.sh',1).decode("utf-8").split(' ')
elif os.environ['HOSTNAME'] == 'techbase':
    mac_ip=p.subexec('/mnt/nand-user/d4c/getnetwork.sh',1).decode("utf-8").split(' ')
else:
    print('unknown hostname! cannot start!')
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
    global ts,A1W,A2W,A2limited,R2value
    try:
        # get_value() returns raw,value,lo,hi,status values based on service name and member number
        A2W=ac.make_svc('A2W','A2S') # returns [sta_reg,status,val_reg,values], values are space separated
        if A2W[1] == 0: # svc status normal
            if A2limited >0:
                A2limited -= 1
        else: # svc status not normal
            if A2limited <3:
                A2limited += 1
        #R2value=str(int(A2limited>0))+' '+str(int(A2limited>1))+' '+str(int(A2limited>2))
        d.set_divalue('R2W',1,int(A2limited>0))
        d.set_divalue('R2W',2,int(A2limited>1))
        d.set_divalue('R2W',3,int(A2limited>2))
        # 0=nolimits, 1=mitsuoff, 2=cooloff, 3=ventoff
    except:
        msg='main: app logic error!'
        print(msg)
        udp.syslog(msg)
        traceback.print_exc()
        time.sleep(5)
        

def crosscheck(): # FIXME: should be autoadjustable to the number of counter state channels RxyV
    ''' Report failure states (via dichannels) depending on other states (from counters for example) '''
    global ts, LRW_ts
    LRW=s.get_value('LRW','dichannels') # LRW REREAD
    
    services=s.get_column('counters','val_reg','R__V') # table,column,like = ''
    for svc in services:
        feeder=svc[1]
        phase=svc[2]
        try:
            phasestate=s.get_value('R'+feeder+phase+'V','counters')[0]  # must not be empty!! should be ok in the end when values appear
            if ts > LRW_ts + 20: # time to check if state based on power is the same as LRW[0]. off_tout = 10
                s.set_membervalue('F'+feeder+'W', eval(phase),(LRW[0]^phasestate),'dichannels') # for 3in1 service, members are phases
                #s.set_membervalue('F'+feeder+phase'S', 1,(LRW[0]^phasestate),'dichannels') # for 1by1 service, always member 1
 
        except:
            print('feeder,phase',feeder+1,phase+1) # debug
            traceback.print_exc()
            time.sleep(5)
    
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