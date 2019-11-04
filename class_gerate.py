import class_interaction

class elektrogeraete():
    def __init__(self):
        pass

class kaffemaschine(elektrogeraete):

    def reinigen(self):
        print('Jetzt reinige ich mich mal')
        # todo

    def kaffeKochen(self):
        print('Kaffe, wer will Kaffe?')
        # todo

    def temperaturEinstellen(self, warm, heiss, sehrHeiss):
        print('Heiß, heißer, Kaffe')
        if warm == True:
            print('Warmduscher')
        elif heiss == True:
            print('Wird schon besser.')
        elif sehrHeiss == True:
            print('Läuft bei dir.')
        # todo


    def kaffestaerkeEinstellen(self):
        print('How stark darf es sein?')

    def bohnenMahlen(self):
        print('Jemand Lust auf Bohnen? Nein? Dann mahle ich')

    def kaffeartEinstellen(self, button1, button2, button3, menge):
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

    def aufheizen(self):
        print('Kaffe ist heeiß')

class wasserkocher(elektrogeraete):
    x = False

    def aufheizen(self):
        print('Nicht der Kaffe, sondern das Wasser blubbert')

    def eigenschaften(self):
        if self.x == False:
            print('Wasserkocher ist leer')
        else:
            print('Ist voll')

    def wasserAuffuellen(self): #für Mensch
        self.x = True

    def wasserEntnehmen(self): #für Maschine
        self.x = False


class ofen(elektrogeraete):

    def aufheizen(self):
        print('Heiß, heißer, Backofen')
