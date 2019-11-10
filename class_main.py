import class_appliance
import class_furniture


if __name__ == '__main__':

    a = class_appliance.kaffemaschine() #Neue Kaffemaschine erstellt (neues Objekt)
    a.kaffeKochen() #Methode Kaffekochen aufgerufen
    a.aufheizen()
    b = class_appliance.wasserkocher()
    b.aufheizen()
    c = class_furniture.unterschrank()
    c.statusWiedergeben()
    b.eigenschaften()
    b.x = True
    b.eigenschaften()
