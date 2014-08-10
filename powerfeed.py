#
# Copyright 2014 droid4control
#

"""Classes and methods to calculate limit level
to control load based on currents in phases of the power
feeders and their capacity

mittekriitilised tarbijad on soltuvad F2 koormusest.
mitsu ja ventilatsiooni taastamisel
(ja ka tarbe suurenemisel) juhib teatud
vahekriitiliste tarbijate tood ouman-gw
piirangutaset ylal pidades. piirangutase
leitakse kasutamata reservi alusel ja on
jargmised:

piirangutase max_vent%  vent_jahut_keeld  mitsu_keeld
3               20            1              1
2               100           1              1
1               100           0              1
0               100           0              0

varujahutuse ja pohijahutuse suhe/lubatus soltub F1 koormusest,
kontrollida, kus fiidril varujahutus asub!
"""

import time
import logging
logging.basicConfig()
log = logging.getLogger(__name__)
log.setLevel(logging.DEBUG)

class PowerFeed:
    """ Class to deal with supply feed issues like
    their count and capacity. Contains subclasses LoadLimit
    and CoolEnable. Needs input on feed switching to activate
    maximum limitations initially and generate ack pulse.
    """
    def __init__(self, feedercount=3, phasecount = 3, \
            feederlimit=[200000, 250000, 150000]):
        # limits for feeder, being equal per phase
        self.feedercount = feedercount # pohi, varu, gene
        self.phasecount = phasecount # normally 3
        self.set_feederlimit(feederlimit) # one value per feeder

        self.feedercurrent = [] # tuple of tuples
        self.ts_feedercurrent=[]
        for i in range(feedercount):
            # one value per feeder phase
            self.feedercurrent.append([None, None, None]) # phase currents shown for each feeder
            self.ts_feedercurrent.append(time.time())
        log.info('PowerFeed init done')


    def get_feederlimit(self):
        return self.feederlimit


    def set_feederlimit(self, input):
        if len(input) != self.feedercount:
            log.warning('attempt to set invalid feederlimits:' + str(input))
        else:
            self.feederlimit = input


    def set_feedercurrent(self, feeder, current=[None, None, None]):
        if len(current) != self.phasecount:
            log.warning('attempt to set invalid feedercurrents to feeder:' + str(feeder) + str(current))
        else:
            self.feedercurrent[feeder] = current
            self.ts_feedercurrent[feeder] = time.time() # timestamp


    def get_feedercurrent(self, feeder):
        return self.feedercurrent[feeder]
        
        
    def get_ts_feedercurrent(self, feeder):
        return self.ts_feedercurrent[feeder]
