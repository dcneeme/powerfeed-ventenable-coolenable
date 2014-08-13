#!/usr/bin/python3

class CoolingZones():
	def __init__(self):
		self.coolingzones = []

	def addZone(self, coolingzone):
		self.coolingzones.append(coolingzone)

	def __str__(self):
		s = "Zone priorities:\n"
		for coolingzone in self.self.coolingzones:
			pass 
            # s += "  " + coolingzone.name + " cooled by: %d, priority of %d (%s)\n" % (coolingzone.getCoolerDevice(), .... ?)
		return s


class CoolingZone():
	def __init__(self, name, maxtemp):
		self.name = name
		self.maxtemp = maxtemp
		self.devices = []

	def addDevice(self, device):
		self.consumers.append(device)

	def removeDevice(self, device):
		if device in self.coolingzone:
			pass #self.consumers.remove(consumer)
		else:
			pass # raise Exception("no such consumer connected with " + name)

	def getPriorities(self):
		cp = 0
		for device in self.coolingzones:
			cp += consumer.getCurrentPower()
		return cp

	    
class PowerFeeds():
	def __init__(self):
		self.powerfeeds = []

	def addFeed(self, powerfeed):
		self.powerfeeds.append(powerfeed)

	def __str__(self):
		s = "Power usage:\n"
		for powerfeed in self.powerfeeds:
			s += "  " + powerfeed.name + " usage: %d of %d (%s)\n" % (powerfeed.getCurrentPower(), powerfeed.maxpower, powerfeed.getConnectedConsumers())
		return s


class PowerFeed():
	def __init__(self, name, maxpower):
		self.name = name
		self.maxpower = maxpower
		self.consumers = []

	def addConsumer(self, consumer):
		self.consumers.append(consumer)

	def removeConsumer(self, consumer):
		if consumer in self.consumers:
			self.consumers.remove(consumer)
		else:
			raise Exception("no such consumer connected with " + name)

	def getCurrentPower(self):
		cp = 0
		for consumer in self.consumers:
			cp += consumer.getCurrentPower()
		return cp

	def getAvailablePower(self):
		return self.maxpower - self.getCurrentPower()

	def getConnectedConsumers(self):
		return ", ".join(map(lambda a: a.name, self.consumers))


class PowerConsumer():
	def __init__(self, name):
		self.name = name
		self.currentpower = 0

	def setCurrentPower(self, currentpower):
		self.currentpower = currentpower

	def getCurrentPower(self):
		return self.currentpower


class Ventilation(PowerConsumer):
	def __init__(self, name, power):
		PowerConsumer.__init__(self, "V:" + name)
		self.power = power
		self.currentpower = 0

	def switchOn(self):
		self.setCurrentPower(self.power)

	def switchOff(self):
		self.setCurrentPower(0)

	def getMaxPower(self):
		return self.power


pf = PowerFeeds()
feed1 = PowerFeed("fiider1", 200)
feed2 = PowerFeed("fiider2", 10)	# pane >=20 ja viimane sisselylitus ei onnestu
pf.addFeed(feed1)
pf.addFeed(feed2)

cool = PowerConsumer("jahutus")
cool.setCurrentPower(60)

vent = Ventilation("ventilatsioon", 20)
vent.switchOn()

print("Molemad seadmed feed1 peal")
feed1.addConsumer(cool)
feed1.addConsumer(vent)
print(str(pf))

print("Lylitame vendi valja")
vent.switchOff()
vent.setCurrentPower(0)
print(str(pf))

print("Liigutame vendi feed2 peale")
feed1.removeConsumer(vent)
feed2.addConsumer(vent)
print(str(pf))

print("kui voolu jatkub, lylitame sisse")
if feed2.getAvailablePower() > vent.getMaxPower():
	vent.switchOn()
	print("-> vent kaivitatud")
else:
	print("-> ei jatku voolu")
print(str(pf))


