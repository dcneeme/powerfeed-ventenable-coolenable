-- DC58888-2 starman energiamotmine keldris + ouman-gw

-- CONF BITS
-- # 1 - value 1 = warningu (values can be 0 or 1 only)
-- # 2 - value 1 = critical, 
-- # 4 - value inversion 
-- # 8 - value to status inversion
-- # 16 - immediate notification on value change (whole multivcalue service will be (re)reported)
-- # 32 - this channel is actually a writable coil output, not a bit from the register (takes value 0000 or FF00 as value to be written, function code 05 instead of 06!)
--     when reading coil, the output will be in the lowest bit, so 0 is correct as bit value
-- # 512 do not send

-- if 2 lowest bits are 0 then status is not following value and must be set programmatically

-- # block sending. 1 = read, but no notifications to server. 2=do not even read, temporarely register down or something...

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

CREATE TABLE dichannels(mba,regadd,bit,val_reg,member,cfg,block,value,status,ts_chg,chg,desc,regtype,ts_msg,type integer,mbi integer); -- ts_chg is update toime (happens on change only), ts_msg =notif
-- mis on dsp_id?? type?? kuidagi kaudselt naitab h voi i starmanis. mbi on index. mb[mbi] jaoks
-- value is bit value 0 or 1, to become a member value with or without inversion
-- status values can be 0..3, depending on cfg. member values to service value via OR (bigger value wins)
-- if newvalue is different from value, write will happen. do not enter newvalues for read only register related rows.
-- type is for category flagging, 0=do, 1 = di, 2=ai, 3=ti. use only 0 and 1 in this table

INSERT INTO "dichannels" VALUES('1','1','8','D1W','1','17','0','0','1','0','','di1 ajutine jalgimine','h','',0,0); -- debug
INSERT INTO "dichannels" VALUES('1','1','9','D1W','2','17','0','0','1','0','','di2 ajutine jalgimine','h','',0,0); -- debug
INSERT INTO "dichannels" VALUES('1','1','10','D1W','3','17','0','0','1','0','','di3 ajutine jalgimine','h','',0,0); -- debug
INSERT INTO "dichannels" VALUES('1','1','11','D1W','4','17','0','0','1','0','','di4 ajutine jalgimine','h','',0,0); -- debug
INSERT INTO "dichannels" VALUES('1','1','12','D1W','5','17','0','0','1','0','','di5 ajutine jalgimine','h','',0,0); -- debug
INSERT INTO "dichannels" VALUES('1','1','13','D1W','6','17','0','0','1','0','','di6 ajutine jalgimine','h','',0,0); -- debug
INSERT INTO "dichannels" VALUES('1','1','14','D1W','7','17','0','0','1','0','','di7 ajutine jalgimine','h','',0,0); -- debug
INSERT INTO "dichannels" VALUES('1','1','15','D1W','8','17','0','0','1','0','','di8 ajutine jalgimine','h','',0,0); -- debug


-- INSERT INTO "dichannels" VALUES('1','1','0','F1W','1','18','0','0','1','0','','pohifiider korras','h','',0,0); -- korrasolek
-- INSERT INTO "dichannels" VALUES('1','1','2','F1W','2','17','0','0','1','0','','pohifiider kasutuses','h','',0,0); -- kasutus

-- INSERT INTO "dichannels" VALUES('1','1','1','F2W','1','18','0','0','1','0','','varufiider korras','h','',0,0); -- korrasolek
-- INSERT INTO "dichannels" VALUES('1','1','3','F2W','2','17','0','0','1','0','','varufiider kasutuses','h','',0,0); -- kasutus

INSERT INTO "dichannels" VALUES('1','1','0','F3W','1','18','0','0','1','0','','pohifiidri f1 rike, 0=ok','h','',0,0); -- f1 FiidriteRikked
INSERT INTO "dichannels" VALUES('1','1','1','F3W','2','18','0','0','1','0','','varufiidri f2 rike','h','',0,0); -- f2 PARANDA BITID

INSERT INTO "dichannels" VALUES('1','1','2','S2W','1','18','0','0','1','0','','varutoide pohifiidril','h','',0,0); -- AbitarbeAllikas
INSERT INTO "dichannels" VALUES('1','1','3','S2W','2','16','0','0','1','0','','varutoide varufiidril','h','',0,0); -- 

INSERT INTO "dichannels" VALUES('1','1','1','S1W','1','16','0','0','1','0','','pohitoide f1 peal ','h','',0,0); -- PohitarbeAllikas
INSERT INTO "dichannels" VALUES('1','1','4','S1W','2','17','0','0','1','0','','pohitoide f2 peal ','h','',0,0); -- tapsusta
INSERT INTO "dichannels" VALUES('1','1','5','S1W','3','18','0','0','1','0','','pohitoide gene peal','h','',0,0); -- tapsusta!

INSERT INTO "dichannels" VALUES('1','0','8','R1S','1','17','0','0','1','0','','mitsu blokeeritud','h','',0,0); -- relee jalgimine. ei pruugi mon naidata

-- virtuaalsed muutujad  varufiidri max faasivoolu ehk oleku alusel
INSERT INTO "dichannels" VALUES('','','0','R2W','1','17','0','0','1','0','','mitsu cooling off','h','',0,0); -- mitsu kinni.
INSERT INTO "dichannels" VALUES('','','0','R2W','2','17','0','0','1','0','','vent-cooling-vent off','h','',0,0); -- vent jahutus kinni
INSERT INTO "dichannels" VALUES('','','0','R2W','3','18','0','0','1','0','','vent almost totally off','h','',0,0); -- 20 % alles jatta?


CREATE UNIQUE INDEX di_regmember on 'dichannels'(val_reg,member); -- mbi, mba jne voivad korduda! teenuste liikmed!
-- NB bits and registers are not necessarily unique!

COMMIT;
