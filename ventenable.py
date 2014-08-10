import time
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

from powerfeed import *
try:
    if pwr:
        log.info('powerfeed instance already exists')
except:
    pwr = PowerFeed()
    log.info('created PowerFeed instance')
    
    
class VentEnable(PowerFeed):
    """ Class to calculate limit level for ventilation
    and related cooling by enabling or disabling them
    or adjusting the load if possible. Compares current
    in selected for ventilation feeder with it's capacity.
    Returns level of limitation being within the range of 0 to 3.
    """
    def __init__(self, feeder=0, limitlevel=3, maxlevel=3, \
           leveldelta = [10000, 15000, 20000], leveldelay=30, \
                  currentdelay=10):
        # current in mA
        self.ventfeeder = feeder
        self.limitlevel = limitlevel # initial limitation level on output
        self.maxlevel = maxlevel # initial limitation level on output
        self.leveldelta = leveldelta # estimated load increase due to falling to the level
        self.leveldelay = leveldelay # no level changes more often than that
        self.currentdelay = currentdelay # filter to check current against lo_limit
        self.ts_notlocurrent = time.time() # must have age above currentdelay to enable limitlevel change
        self.set_limitlevel(limitlevel)
        log.info('LimitLevel init done')


    def set_ventfeeder(self, input):
        if input >= 0 and input < self.feedercount:
            # indexing feeders from 0
            self.ventfeeder = input
        else:
            log.warning('attempt to set an invalid ventfeeder', input)


    def get_limitlevel(self):
        return self.limitlevel


    def set_limitlevel(self, input):
        if input >= 0 and input <= self.maxlevel:
            self.limitlevel = input
            self.ts_level = time.time()
        else:
            log.warning('attempt to set an invalid limitlevel ') # +str(input))


    def output(self):
        """Returns limitation level in range from 0 (no limitations) to
        3 (maximum limitation), avoiding changes faster than self.leveldelay.
        Limitation level increase is immediate, but decrease is allowed in
        increments of 1 after leveldelay s from previous change.
        """
        tsnow = time.time()
        updn = 0 # self.limitlevel change
        if len(pwr.feedercurrent[self.ventfeeder]) != pwr.phasecount:
            log.warning('invalid number of phase feedercurrents ') # +str(feedercurrent))
            log.info('all controlled loads to be disconnected')
            return self.maxlevel

        if pwr.ts_feedercurrent[self.ventfeeder] + 10 < tsnow:
            log.warning('stalled current for ventfeeder, age ' + str(tsnow - pwr.ts_feedercurrent[self.ventfeeder])) 
            log.info('all controlled loads to be disconnected')
            return self.maxlevel
            
        for i in range(pwr.phasecount):
            # the values for i are 0 1 2 for 3 phases
            if pwr.feedercurrent[self.ventfeeder][i]  == None:
                #no valid value yet, do nothing
                log.warning('no change to self.limitlevel due to invalid feedercurrent')
                return self.limitlevel # stop

            if (pwr.feedercurrent[self.ventfeeder][i] > pwr.feederlimit[self.ventfeeder] \
                    and self.limitlevel < self.maxlevel):
                updn += pwr.phasecount # to ensure detection
                self.ts_notlocurrent = tsnow # pwr.ts_current[self.ventfeeder]  # updating with above lo_limit only
            elif self.limitlevel > 0 and updn <= 0:
                if (pwr.feedercurrent[self.ventfeeder][i] + self.leveldelta[self.limitlevel - 1] < pwr.feederlimit[self.ventfeeder]):
                    updn += -1 # decrease limitations
                else:
                    self.ts_notlocurrent = tsnow # pwr.ts_current[self.ventfeeder]
            else:
                self.ts_notlocurrent = tsnow # pwr.ts_current[self.ventfeeder]  # updating with above lo_limit only

        if (updn > 0 and self.limitlevel < self.maxlevel):
            self.limitlevel = self.maxlevel
            self.ts_level = tsnow
            log.info('limitations to be set') #  due to feedercurrent '+str(feedercurrent))
            print('limitations to be set, level',self.limitlevel) # temporary
        elif (updn == -pwr.phasecount and tsnow > self.leveldelay + self.ts_level \
                and pwr.ts_feedercurrent[self.ventfeeder] < tsnow - self.currentdelay and self.limitlevel > 0):
            self.limitlevel += -1
            self.ts_level = tsnow
            log.info('limitations decrease ') # to '+str(self.limitlevel))
            print('limitations decrease, level',self.limitlevel) # temporary

        return self.limitlevel