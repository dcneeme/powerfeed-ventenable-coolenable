-- starmani energiamootmise jaoks. siin sees ka wcount! lo hi viide nr alusel, kui lo hi nr vahemikus 1...9. muidu kui vaartus. prefix m? parem mitte. 
-- viidatud liikme vaartus arvesse votta hi lo jaoks.

-- analogue values and temperatures channel definitions for android- or linux-based automation controller 
-- x1 ja x2 for input range, y1 y2 for output range. conversion based on 2 points x1,y1 and y1,y2. x=raw, y=value.
-- avg defines averaging strength, has effect starting from 2

-- # CONFIGURATION BITS
-- CONFIG BIT MEANINGS
-- # 1 - below outlo warning, 4 
-- # 2 - below outlo critical, 8 - above outhi critical
-- # 4 - above outhi warning
-- # 8   above outhi critical

-- 16 - immediate notification on status change (USED FOR STATE FROM POWER)
-- 32 - value "limits to status" inversion  - to defined forbidden area instead of allowed area  
-- 64 - power flag, based on value increments
-- 128 - state from power flag
-- 256 - notify on 10% value change (not only limit crossing that becomes activated by first 4 cfg bits)
-- 512 - do not report at all, for internal usage
-- 1024 - counter, unsigned, to be queried/restored from server on restart
    -- counters are normally located in 2 registers, but also ai values can be 32 bits. 
    -- negative wcount means swapped words (barionet, npe imod)
 


PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
-- drop table aicochannels; -- remove the old one
-- mingi muust teenuse mingist liikmest soltuva korrektsiooni siseviimiseks lisa tulbad addregister,addmember. 
-- see viide mis liidab viidatud value kui paranduse.
CREATE TABLE aicochannels(mba,regadd,val_reg,member,cfg,x1,x2,y1,y2,outlo,outhi,avg,block,raw,value,status,ts,desc, regtype, grp integer,mbi integer,wcount integer,loref,hiref); 
-- type is for category flagging, 0=do, 1 = di, 2=ai, 3=ti. use only 2 and 3 in this table (4=humidity, 5=co2?)

-- hi lo voetakse viidatud lisateenustest, kui viide olemas on. eristamine member nr alusel.    loref, hiref only for triggers!

-- dio bitmap testiks
INSERT INTO "aicochannels" VALUES('1','1','D1V','1','17','0','100','0','100','200','250','2','','','110','0','','di bitmap','h',3,0,2,'',''); 

-- voltage
INSERT INTO "aicochannels" VALUES('44','769','V1W','1','18','0','100','0','100','200','250','2','','','110','0','','voltage phase1 mV','h',3,0,2,'4','5'); -- actual voltage mV (V initially, must be overwritten in member chg)
INSERT INTO "aicochannels" VALUES('44','773','V1W','2','18','0','100','0','100','210','270','2','','','110','0','','voltage phase1 mV','h',3,0,2,'4','5'); -- 
INSERT INTO "aicochannels" VALUES('44','777','V1W','3','18','0','100','0','100','200','270','2','','','110','0','','voltage phase1 mV','h',3,0,2,'4','5'); -- 
INSERT INTO "aicochannels" VALUES('','','V1W','4','','','','','','','1','','','','200000','','','hi limit mV','s!',3,0,2,'',''); -- max voltage mV, value to member 2 hi using trigger
INSERT INTO "aicochannels" VALUES('','','V1W','5','','','','','','1','','','','','250000','','','lo limit mV','s!',3,0,2,'',''); -- min voltage mV, value to member 1 lo

INSERT INTO "aicochannels" VALUES('43','769','V2W','1','18','0','100','0','100','200','250','2','','','110','0','','voltage phase1 mV','h',3,0,2,'4','5'); -- actual voltage mV (V initially, must be overwritten in member chg)
INSERT INTO "aicochannels" VALUES('43','773','V2W','2','18','0','100','0','100','210','270','2','','','110','0','','voltage phase1 mV','h',3,0,2,'4','5'); -- 
INSERT INTO "aicochannels" VALUES('43','777','V2W','3','18','0','100','0','100','200','270','2','','','110','0','','voltage phase1 mV','h',3,0,2,'4','5'); -- 
INSERT INTO "aicochannels" VALUES('','','V2W','4','','','','','','','1','','','','200000','','','hi limit mV','s!',3,0,2,'',''); -- max mV, value to member 2 hi using trigger
INSERT INTO "aicochannels" VALUES('','','V2W','5','','','','','','1','','','','','250000','','','lo limit mV','s!',3,0,2,'',''); -- min mV, value to member 1 lo

-- current
INSERT INTO "aicochannels" VALUES('44','781','A1W','1','18','0','100','0','100','200','250','2','','','110','0','','voltage phase1 mV','h',3,0,2,'4','5'); -- actual current mA 
INSERT INTO "aicochannels" VALUES('44','785','A1W','2','18','0','100','0','100','210','270','2','','','110','0','','voltage phase1 mV','h',3,0,2,'4','5'); -- 
INSERT INTO "aicochannels" VALUES('44','789','A1W','3','18','0','100','0','100','200','270','2','','','110','0','','voltage phase1 mV','h',3,0,2,'4','5'); -- 
INSERT INTO "aicochannels" VALUES('','','A1W','4','','','','','','','1','','','','100000','','','hi limit mA','s!',3,0,2,'',''); -- max current, value to member 2 hi using trigger
INSERT INTO "aicochannels" VALUES('','','A1W','5','','','','','','1','','','','','250000','','','lo limit mA','s!',3,0,2,'',''); -- min current mA, value to member 1 lo

INSERT INTO "aicochannels" VALUES('43','781','A2W','1','18','0','100','0','100','200','250','2','','','110','0','','voltage phase1 mA','h',3,0,2,'4','5'); -- actual voltage mV (V initially, must be overwritten in member chg)
INSERT INTO "aicochannels" VALUES('43','785','A2W','2','18','0','100','0','100','210','270','2','','','110','0','','voltage phase1 mA','h',3,0,2,'4','5'); -- 
INSERT INTO "aicochannels" VALUES('43','789','A2W','3','18','0','100','0','100','200','270','2','','','110','0','','voltage phase1 mA','h',3,0,2,'4','5'); -- 
INSERT INTO "aicochannels" VALUES('','','A2W','4','','','','','','','1','','','','100000','','','hi limit mA','s!',3,0,2,'',''); -- max mA, value to member 2 hi using trigger
INSERT INTO "aicochannels" VALUES('','','A2W','5','','','','','','1','','','','','250000','','','lo limit mA','s!',3,0,2,'',''); -- min mA, value to member 1 lo

-- heat pump 1
INSERT INTO "aicochannels" VALUES('1','202','1H1W','1','17','0','100','0','100','0','500','','','','110','','','h1 supply temp','h',3,1,2,'',''); -- h1 supply temp 1/10 deg
INSERT INTO "aicochannels" VALUES('1','204','1H1W','2','17','0','100','0','100','0','500','','','','110','','','h2 supply temp','h',3,1,2,'',''); -- h1 return temp

INSERT INTO "aicochannels" VALUES('1','274','1H2W','1','17','0','100','0','100','0','500','','','','110','','','h1 supply temp','h',3,1,2,'',''); -- h1 supply temp 1/10 deg
INSERT INTO "aicochannels" VALUES('1','223','1H2W','2','17','0','100','0','100','0','500','','','','110','','','h2 supply temp','h',3,1,2,'',''); -- h1 return temp

-- INSERT INTO "aicochannels" VALUES('1','621','1CSV','2','17','0','100','0','100','0','500','','','','110','','','cooling set','h',3,1,1,'',''); -- cooling setpoint_


-- heat pump 2
INSERT INTO "aicochannels" VALUES('1','202','2H1W','1','17','0','100','0','100','0','500','','','','110','','','h1 supply temp','h',3,2,2,'',''); -- h1 supply temp 1/10 deg
INSERT INTO "aicochannels" VALUES('1','204','2H1W','2','17','0','100','0','100','0','500','','','','110','','','h2 supply temp','h',3,2,2,'',''); -- h1 return temp

INSERT INTO "aicochannels" VALUES('1','274','2H2W','1','17','0','100','0','100','0','500','','','','110','','','h1 supply temp','h',3,2,2,'',''); -- h1 supply temp 1/10 deg
INSERT INTO "aicochannels" VALUES('1','223','2H2W','2','17','0','100','0','100','0','500','','','','110','','','h2 supply temp','h',3,2,2,'',''); -- h1 return temp

-- INSERT INTO "aicochannels" VALUES('1','621','2CSV','1','17','0','100','0','100','0','500','','','','110','','','cooling set','h',3,2,1,'',''); -- cooling setpoint_

-- heat pumps common

INSERT INTO "aicochannels" VALUES('1','220','CTW','1','17','0','100','0','100','0','500','','','','110','','','cooling temp','h',3,1,2,'','3'); -- must be less than 15 deg
INSERT INTO "aicochannels" VALUES('1','220','CTW','2','17','0','100','0','100','0','500','','','','110','','','cooling temp','h',3,2,2,'','3'); -- must be less than 15 deg
INSERT INTO "aicochannels" VALUES('','','CTW','3','','','','','','','1','','','','0','','','lo limit ddegC','s!',3,0,2,'',''); -- 
INSERT INTO "aicochannels" VALUES('','','CTW','4','','','','','','1','','','','','150','','','hi limit ddegC','s!',3,0,2,'',''); -- if higher after initial delay then HP has a problem

CREATE UNIQUE INDEX aico_regmember on 'aicochannels'(mbi,val_reg,member); -- every service member only once

CREATE TRIGGER aico_lo after update on aicochannels when exists(select val_reg,member from aicochannels where val_reg=new.val_reg)
BEGIN
update aicochannels set outlo=new.value where val_reg=new.val_reg AND loref=new.member; -- member value to outlo of another member
END;

CREATE TRIGGER aico_hi after update on aicochannels when exists(select val_reg,member from aicochannels where val_reg=new.val_reg)
BEGIN
update aicochannels set outhi=new.value where val_reg=new.val_reg AND hiref=new.member; -- member value to outhi of another member
END;
-- several records can be updated in one go

COMMIT;
