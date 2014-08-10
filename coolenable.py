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
    
    
class CoolEnable(PowerFeed):
    """ Class to calculate primary/secondary cooling enable signals.
    Main and secondary coolers may share the same power feeder,
    total consumption may not exceed the feederlimit then.
    The aim is to generate enable signals for all coolers taking into
    account the current headroom, feeder availability and zone temperatures.

    1. iga tsooni varujahutust voib koivitada soltumata soojuspumpade
    tervisest siis, kui tsooni temperatuur seda nouab, eeldusel, et
    abitoiteks kasutavas fiidris on kaivitusloa andmise hetkel x A reservi
    ning pohijahutus ja varujahutus ei saa toidet sama fiidri pealt. kui
    varujahutuse sisselylituseks vajalikku reservi on voimalik tekitada vent
    seadme voi mitsu tarbimise piiramise teel, tuleb seda teha.

    2. kui tekib vajaduse kaivitada varujahutus mitmes tsoonis korraga,
    tehakse seda koigepealt etteantud temperatuuri koige enam yletavas
    tsoonis. jargmise tsooni lubamiseks vajaliku reservi kontroll tehakse
    peale seda ning ajal, kui eelmisena lubatud tsoonis toimub tarbimine
    (avastatakse voolu juurdekasv)

    3. kui avastatakse soojuspumba viga (jahutusagendi temperatuuri tous yle
    etteantud piiri), blokeeritakse see pump ja antakse haire. sp
    taaskaivitamine toimub manuaalse protsessina vaba tarbimismahu
    olemasolul, soovitavalt molema sisendfiidri korrasoleku ajal ja peab
    sisaldama sp diagnostikat.

    4. kui soojuspumbad ja varujahutus satuvad (naiteks pohifiidri rikke
    puhul) samale toitefiidrile ja soojuspumbad on teadaolevalt korras,
    keelatakse varujahutuse kaivitumine ja rakendatakse piiranguid
    ventilatsioonile ja mitsu jahutusele.
    """
    def __init__(self, zonecount=4, \
                       cooler1count=2, \
                       cooler2count=4, \
                     cooler1current=[50000, 50000], \
                     cooler2current=[25000, 24000, 25000, 24000], \
                    zoneservicemap1=[1,2,1,3], \
                    zoneservicemap2=[1,6,6,8], \
                        zonetempset=[250, 260 , 270, 260], \
                       currentdelay=10, \
                        enabledelay=30):

        self.zonecount = zonecount # zone has temperature and relates to coolers
        self.cooler1count = cooler1count
        self.cooler2count = cooler2count
        self.cooler1current = cooler1current # max consumption mA
        self.cooler2current = cooler2current
        self.zoneservicemap1 = zoneservicemap1 # primary to zones
        self.zoneservicemap2 = zoneservicemap2 # secondary to zones
        self.zonetempset = zonetempset # temperature setpoints for zones
        self.currentdelay = currentdelay # min time for current to stay below
        self.enabledelay = enabledelay # min delay s before next enable
        self.cooler1enable = [1, 1] # output tuple for primary coolers enable
        self.cooler2enable = [0, 0, 0, 0] # output tuple for secondary coolers enable

        self.set_cooler1feeder([0, 0])
        self.set_cooler2feeder([1, 1, 1, 1])
        self.set_zonetemp = [200, 200, 200, 200]  # ddegC

        log.info('CoolEnable init done')


    def get_cooler1enable(self):
        return self.cooler1enable


    def get_cooler2enable(self):
        return self.cooler2enable


    def set_cooler1feeder(self, input):
        if len(input) != self.cooler1count:
            log.warning('attempt to set invalid cooler1 to feeder map')
        else:
            cooler1feeder = input  # initially primary cooling is enabled


    def set_cooler2feeder(self, input):
        if len(input) != self.cooler2count:
            log.warning('attempt to set invalid cooler2 to feeder map')
        else:
            self.cooler2feeder = input  # secondary (backup) cooling disabled


    def set_zonetemp(self, input):
        if len(input) != self.zonecount:
            log.warning('attempt to set invalid zonetemp values')
        else:
            self.zonetemp = input  # actual temperatures in zones as a tuple


    def get_zonetemp(self):
        return self.zonetemp # actual temperatures in zones as a tuple


    def output(self):
        """Returns enable tuples for both primary and secondary coolers
        based on currents in feeders and coolers to feeders usage mapping """
        # correct coolerXfeeder and zonetemp variables must be set
        tsnow = time.time()

        # add here a lot...

        return self.cooler1enable, self.cooler2enable # tuple of 2 tuples


        