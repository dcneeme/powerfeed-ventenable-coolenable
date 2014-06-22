#!/usr/bin/bash
# find out if connectivity is ok. start by crontab
# pings testserver, it no success, restarts gprs
# if ping ok but no udpconn_alive in ps, start vpn

testserver="195.222.15.51"
LOG=/root/d4c/chk_conn.log
#vpnconf=/mnt/mtd/openVPN/config/itvilla.conf

cd /root/d4c/

if [ `ping -c3 $testserver | grep "0 packets received" | wc -l` -gt 0 ]; then # conn lost
    (echo -n "no ping response from ${testserver}, waiting for retry "; date) | tee -a $LOG
    #logger -t d4c no response to ping $testserver
    sleep 10 # wait before retry
    
    if [ `ping -c3 $testserver | grep "0 packets received" | wc -l` -gt 0 ]; then # conn lost
        (echo -n "no ping response again from ${testserver}, trying to run setnetwork,sh"; date) | tee -a $LOG
        #logger -t d4c no response to ping again... going to restart gprs
        ./setnetwork.sh &
    else
        echo connectivity ok on second try
        #logger -t d4c connectivity ok on second try based on ping $testserver
    fi
        
else
    echo connectivity ok
    #logger -t d4c connectivity ok on first try based on ping $testserver
    
    # chk if not alive in ps then vpn should be started
    #count=`./ps1 alive | grep -v chk_conn.sh | wc -l`
    #if [ $count -eq 0 ]; then # need for vpn
    #    /bin/npe -USER_LED # yellow LED off 
    #    echo missing alive processes... starting vpn
    #    logger -t missing alive processes... starting vpn
    #    vpn stop
    #    vpn start $vpnconf
        #./ps1 $proc # debug
    #    exit 0
    #else
    #    /bin/npe +USER_LED # yellow LED on, udp conn ok, vpn no needed. 
    #    #vpn auto off? only if appd in ps...
    #fi

fi
exit 0
