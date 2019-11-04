#from abc import ABC, abstractmethod

class interaction():
    #Vererbung - hier abstrakt lassen und in Unterklassen dann spezifisch definieren

    def __init__(self):

        #@abstractmethod
        def aufheizen(self):
            #print('Ich heize auf, gaaanz heiß!')
            pass
        def schneiden(self):
            print('Ich schneeeide')

        def reinigen(self):
            print('ich reinige')

        def wiegen(self):
            print('Das wird jetzt abgewogen')

        def mischen(self):
            print('Ich mische mische mische')

        def ruehren(self):
            print('Rüüüühren')

        def kneten(self):
            print('Das wird jetzt geknetet')

        def zerkleinern(self):
            print('Das wird jetzt klein')

        def kochen(self):
            print('Ich habe Hunger. Koch!')

        def duensten(self):
            print('Das wird ganz schön warm hier, dünste lieber!')
