import class_gerate
import class_moebel


if __name__ == '__main__':

    a = class_gerate.kaffemaschine() #Neue Kaffemaschine erstellt (neues Objekt)
    a.kaffeKochen() #Methode Kaffekochen aufgerufen
    a.aufheizen()
    b = class_gerate.wasserkocher()
    b.aufheizen()
    c = class_moebel.unterschrank()
    c.statusWiedergeben()
    b.eigenschaften()
    b.x = True
    b.eigenschaften()
