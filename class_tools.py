# Beschreibung des vorhandenen Koch- und Essgeschirrs und  ob es in Benutzung ist
# Beschreibung der Behälter für Lebensmittel, Gewürze etc.


class tools:
    def __init__(self, name, usage):
        self.name = name
        self.usage = usage


class container(tools):
    def __init__(self, name, usage, capacity):
        tools.__init__(self, name, usage)
        self.capacity = capacity
