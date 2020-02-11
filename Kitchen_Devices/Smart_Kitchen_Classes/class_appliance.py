import Kitchen_Devices.Smart_Kitchen_Classes.class_interaction as class_interaction
# status = on/off; Operable = error message?


class interactiveAppliance():
    def __init__(self, status, operable):
        self.status = status
        self.operable = operable


class coffeeMachine(interactiveAppliance):

    def cleaning(self):
        print('Jetzt reinige ich mich mal')
        # todo

    def brewing(self):
        print('Kaffe, wer will Kaffe?')
        # todo

    def temperatureSettings(self, warm, hot, veryHot):
        print('Heiß, heißer, Kaffe')
        if warm == True:
            print('Warmduscher')
        elif hot == True:
            print('Wird schon besser.')
        elif veryHot == True:
            print('Läuft bei dir.')
        # todo


    def strengthSettings(self):
        print('How stark darf es sein?')

    def grindingBeans(self):
        print('Jemand Lust auf Bohnen? Nein? Dann mahle ich')

    def typeOfCoffee(self, button1, button2, button3, menge):
        if button1 == True:
            print('Dat is Kaffe')
            if menge <= 0 or menge > 200:
                print('Jet net')
            elif menge > 0 and menge < 200:
                print('Passt. Mache ich')
        elif button2 == True:
            print('Dat is Espresso')
            if menge <= 0 or menge > 60:
                print('Jet net')
            elif menge > 0 and menge < 60:
                print('Here you go')
        elif button3 == True:
            print('Dat is Cappucchino')
            if menge <= 0 or menge > 200:
                print('Jet net')
            elif menge > 0 and menge < 200:
                print('Here you go')
        else:
            print('dat war nichts. Drück nur eine Taste')

    def heating(self):
        print('Kaffe ist heeiß')


class waterHeater(interactiveAppliance):
    x = False

    def heating(self):
        print('Nicht der Kaffe, sondern das Wasser blubbert')

    def operational(self):
        if self.x == False:
            print('Wasserkocher ist leer')
        else:
            print('Ist voll')

    def fillWater(self): #für Mensch
        self.x = True

    def extractWater(self): #für Maschine
        self.x = False


class oven(interactiveAppliance):

    def heating(self, function, degrees, timer, childProtechtion):
        if (function == "grillfunction"):
            print("grill on")
        if (function == "upper/lower_heat"):
            print ("upper/lower heat on")
        if (function == "circulating_air"):
            print("circulating air on")
        if (function == "circulating_grill"):
            print("circulating air and grill on")
        if (function == "light"):
            print("light is on")
        if (function == "lower_heat"):
            print("lower heat on")

        if (degrees>=250):
            print("That hot is not possible")

        if (timer>0):
            print("timer is set")

        if (childProtechtion == True):
            print("Child protection is activated")
        if (childProtechtion == False):
            print("Child protection is deactivated")


class dishwasher(interactiveAppliance):
    def isCleaning(self):
        print('Cleaning dishes')


# values for watt: 90, 180, 360, 600, 900
class microwave(interactiveAppliance):
    def __init__(self, status, operable, watt):
        interactiveAppliance.__init__(self, status, operable)
        self.watt = watt


# 4 hotplates, 2 are expandable
class stove(interactiveAppliance):
    def __init__(self, status, operable, hotplate1, hotplate2, hotplate3, hotplate4):
        interactiveAppliance.__init__(self, status, operable)
        self.hotplate1 = hotplate1
        self.hotplate2 = hotplate2
        self.hotplate3 = hotplate3
        self.hotplate4 = hotplate4
