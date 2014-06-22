-- DC58888-2 starman energiamotmine keldris + ouman-gw

-- CONF BITS
-- # 1 - value 1 = warningu (values can be 0 or 1 only)
-- # 2 - value 1 = critical, 
-- # 4 - value inversion 
-- # 8 - value to status inversion
-- # 16 - immediate notification on value change (whole multivcalue service will be (re)reported)
-- # 32 - this channel is actually a writable coil output, not a bit from the register (takes value 0000 or FF00 as value to be written, function code 05 instead of 06!)
--     when reading coil, the output will be in the lowest bit, so 0 is correct as bit value

-- if 2 lowest bits are 0 then status is not following value and must be set programmatically

-- # block sending. 1 = read, but no notifications to server. 2=do not even read, temporarely register down or something...

PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

CREATE TABLE dichannels(mba,regadd,bit,val_reg,member,cfg,block,value,status,ts_chg,chg,desc,dsp_id,ts_msg,type integer,mbi integer); -- ts_chg is update toime (happens on change only), ts_msg =notif
-- mis on dsp_id?? type?? kuidagi kaudselt naitab h voi i starmanis. mbi on index. mb[mbi] jaoks
-- value is bit value 0 or 1, to become a member value with or without inversion
-- status values can be 0..3, depending on cfg. member values to service value via OR (bigger value wins)
-- if newvalue is different from value, write will happen. do not enter newvalues for read only register related rows.
-- type is for category flagging, 0=do, 1 = di, 2=ai, 3=ti. use only 0 and 1 in this table

INSERT INTO "dichannels" VALUES('1','1','0','F1W','1','18','0','0','1','0','','pohifiider korras','20','',0,0); -- korrasolek
INSERT INTO "dichannels" VALUES('1','1','2','F1W','2','17','0','0','1','0','','pohifiider kasutuses','20','',0,0); -- kasutus

INSERT INTO "dichannels" VALUES('1','1','1','F2W','1','18','0','0','1','0','','varufiider korras','20','',0,0); -- korrasolek
INSERT INTO "dichannels" VALUES('1','1','3','F2W','2','17','0','0','1','0','','varufiider kasutuses','20','',0,0); -- kasutus

CREATE UNIQUE INDEX di_regmember on 'dichannels'(val_reg,member); -- mbi, mba jne voivad korduda! teenuste liikmed!
-- NB bits and registers are not necessarily unique!

COMMIT;
