# Beschreibung der Möbel. Stauraum besitzt Inhalt.
class furniture():
    def __init__(self, name, location):
        self.name = name
        self.location = location


class storage(furniture):
    def __init__(self, name, location, content):
        furniture.__init__(self, name, location)
        self.content = content


# Oberschrank
class wallUnit(furniture):

     def statusWiedergeben(self):
         print('Ich bin voll.')

# Unterschrank
class baseUnit(furniture):

    def statusWiedergeben(self):
        print('Der Mülleimer ist so voll wie der Oberschrank')
