-- starmani energiamootmise jaoks. siin sees ka wcount! lo hi viide nr alusel, kui lo hi nr vahemikus 1...9. muidu kui vaartus. prefix m? parem mitte. 
-- viidatud liikme vaartus arvesse votta hi lo jaoks.

-- analogue values and temperatures channel definitions for android- or linux-based automation controller 
-- x1 ja x2 for input range, y1 y2 for output range. conversion based on 2 points x1,y1 and y1,y2. x=raw, y=value.
-- avg defines averaging strength, has effect starting from 2

-- # CONFIGURATION BITS
-- # siin ei ole tegemist ind ja grp teenuste eristamisega, ind teenused konfitakse samadel alustel eraldi!
-- # konfime poolbaidi vaartustega, siis hex kujul hea vaadata. vanem hi, noorem lo!
-- # x0 - alla outlo ikka ok, 0x - yle outhi ikka ok 
-- # x1 - alla outlo warning, 1x - yle outhi warning
-- # x2 - alla outlo critical, 2x - yle outhi critical
-- # x3 - alla outlo ei saada, 3x - yle outhi ei saada, status 3? not useed so far...
-- hex 21 = dec 33, hex 12 = dec 18 - aga ei muuda statust???
-- # lisaks bit 2 lisamine asendab vaartuse nulliga / kas on vaja?
-- # lisaks bit 4 teeb veel midagi / reserv


PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;
-- drop table aichannels; -- remove the old one
-- mingi muust teenuse mingist liikmest soltuva korrektsiooni siseviimiseks lisa tulbad addregister,addmember. 
-- see viide mis liidab viidatud value kui paranduse.
CREATE TABLE aichannels(mba,regadd,val_reg,member,cfg,x1,x2,y1,y2,outlo,outhi,avg,block,raw,value,status,ts,desc,comment,type integer,mbi integer,wcount integer,loref,hiref); 
-- type is for category flagging, 0=do, 1 = di, 2=ai, 3=ti. use only 2 and 3 in this table (4=humidity, 5=co2?)

-- hi lo voetakse viidatud lisateenustest, kui viide olemas on. eristamine member nr alusel.    


-- voltage
INSERT INTO "aichannels" VALUES('44','769','V1W','1','18','0','100','0','100','200','250','2','','','110','0','','voltage phase1 mV','',3,0,2,'4','5'); -- actual voltage mV (V initially, must be overwritten in member chg)
INSERT INTO "aichannels" VALUES('44','773','V1W','2','18','0','100','0','100','210','270','2','','','110','0','','voltage phase1 mV','',3,0,2,'4','5'); -- 
INSERT INTO "aichannels" VALUES('44','777','V1W','3','18','0','100','0','100','200','270','2','','','110','0','','voltage phase1 mV','',3,0,2,'4','5'); -- 
INSERT INTO "aichannels" VALUES('','','V1W','4','','','','','','','1','','','','200000','','','hi limit mV','',3,0,2,'',''); -- max voltage mV, value to member 2 hi using trigger
INSERT INTO "aichannels" VALUES('','','V1W','5','','','','','','1','','','','','250000','','','lo limit mV','',3,0,2,'',''); -- min voltage mV, value to member 1 lo

INSERT INTO "aichannels" VALUES('43','769','V2W','1','18','0','100','0','100','200','250','2','','','110','0','','voltage phase1 mV','',3,0,2,'4','5'); -- actual voltage mV (V initially, must be overwritten in member chg)
INSERT INTO "aichannels" VALUES('43','773','V2W','2','18','0','100','0','100','210','270','2','','','110','0','','voltage phase1 mV','',3,0,2,'4','5'); -- 
INSERT INTO "aichannels" VALUES('43','777','V2W','3','18','0','100','0','100','200','270','2','','','110','0','','voltage phase1 mV','',3,0,2,'4','5'); -- 
INSERT INTO "aichannels" VALUES('','','V2W','4','','','','','','','1','','','','200000','','','hi limit mV','',3,0,2,'',''); -- max mV, value to member 2 hi using trigger
INSERT INTO "aichannels" VALUES('','','V2W','5','','','','','','1','','','','','250000','','','lo limit mV','',3,0,2,'',''); -- min mV, value to member 1 lo

-- current
INSERT INTO "aichannels" VALUES('44','781','A1W','1','18','0','100','0','100','200','250','2','','','110','0','','voltage phase1 mV','',3,0,2,'4','5'); -- actual current mA 
INSERT INTO "aichannels" VALUES('44','785','A1W','2','18','0','100','0','100','210','270','2','','','110','0','','voltage phase1 mV','',3,0,2,'4','5'); -- 
INSERT INTO "aichannels" VALUES('44','789','A1W','3','18','0','100','0','100','200','270','2','','','110','0','','voltage phase1 mV','',3,0,2,'4','5'); -- 
INSERT INTO "aichannels" VALUES('','','A1W','4','','','','','','','1','','','','200000','','','hi limit mV','',3,0,2,'',''); -- max current, value to member 2 hi using trigger
INSERT INTO "aichannels" VALUES('','','A1W','5','','','','','','1','','','','','250000','','','lo limit mV','',3,0,2,'',''); -- min current mA, value to member 1 lo

INSERT INTO "aichannels" VALUES('43','781','A2W','1','18','0','100','0','100','200','250','2','','','110','0','','voltage phase1 mA','',3,0,2,'4','5'); -- actual voltage mV (V initially, must be overwritten in member chg)
INSERT INTO "aichannels" VALUES('43','785','A2W','2','18','0','100','0','100','210','270','2','','','110','0','','voltage phase1 mA','',3,0,2,'4','5'); -- 
INSERT INTO "aichannels" VALUES('43','789','A2W','3','18','0','100','0','100','200','270','2','','','110','0','','voltage phase1 mA','',3,0,2,'4','5'); -- 
INSERT INTO "aichannels" VALUES('','','A2W','4','','','','','','','1','','','','200000','','','hi limit mV','',3,0,2,'',''); -- max mA, value to member 2 hi using trigger
INSERT INTO "aichannels" VALUES('','','A2W','5','','','','','','1','','','','','250000','','','lo limit mV','',3,0,2,'',''); -- min mA, value to member 1 lo

INSERT INTO "aichannels" VALUES('1','202','T1V','1','18','0','100','0','100','200','250','2','','','110','0','','voltage phase1 mA','',3,1,2,'4','5'); -- ouman test


CREATE UNIQUE INDEX ai_regmember on 'aichannels'(mbi,val_reg,member); -- every service member only once

CREATE TRIGGER ai_lo after update on aichannels when exists(select val_reg,member from aichannels where val_reg=new.val_reg)
BEGIN
update aichannels set outlo=new.value where val_reg=new.val_reg AND loref=new.member; -- member value to outlo of another member
END;

CREATE TRIGGER ai_hi after update on aichannels when exists(select val_reg,member from aichannels where val_reg=new.val_reg)
BEGIN
update aichannels set outhi=new.value where val_reg=new.val_reg AND hiref=new.member; -- member value to outhi of another member
END;
-- several records can be updated in one go

COMMIT;
