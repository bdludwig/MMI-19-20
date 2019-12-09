# Beschreibung der Möbel. Stauraum besitzt Inhalt.
class Furniture:
    def __init__(self, name, location):
        self.name = name
        self.location = location


class Storage(Furniture):
    def __init__(self, name, location):
        Furniture.__init__(self, name, location)
        self.content = []

    def putItem(self, item):
        self.content.append(item)

    def removeItem(self, item_id):
        print("ToDo: Remove Item")

    def getContent(self):
        return self.content
