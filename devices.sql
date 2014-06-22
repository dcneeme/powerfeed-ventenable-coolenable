-- devices attached to the modbusRTU or modbusTCP network. starman energy
BEGIN TRANSACTION; 
-- count0..count3 are channel counts for do, do, ai an 1wire.

CREATE TABLE 'devices'(num integer,rtuaddr integer,tcpaddr,mbi integer,status integer,name,location,descr,count0 integer,count1 integer,count2 integer,count3 integer); -- enables using mixed rtu and tcp inputs
-- last 4 columns not used!

-- inputs via rs485, line analyzers
INSERT INTO 'devices' VALUES(1,1,'/dev/ttyAPP0',0,0,'DC6888','kelder','droid4control kontroller',8,8,8,8); -- controller iocard
INSERT INTO 'devices' VALUES(2,43,'/dev/ttyAPP0',0,0,'analy1','kelder','pohifiider',8,8,8,8); -- analyser 1
INSERT INTO 'devices' VALUES(3,44,'/dev/ttyAPP0',0,0,'analy2','kelder','varufiider',8,8,8,8); -- analyzer 2

-- ouman modbustcp
INSERT INTO 'devices' VALUES(4,1,'62.65.245.83:502',1,0,'ouman','kelder','soojuspump 1',8,8,8,8); -- heat pump 1
INSERT INTO 'devices' VALUES(5,1,'62.65.245.84:502',2,0,'ouman2','kelder','soojuspump 2',8,8,8,8); -- heat pump 2
 
CREATE UNIQUE INDEX num_devices on 'devices'(num); -- device ordering numbers must be unique
CREATE UNIQUE INDEX addr_devices on 'devices'(rtuaddr,tcpaddr); -- device addresses must be unique

COMMIT;
    