# Beschreibung des vorhandenen Koch- und Essgeschirrs und  ob es in Benutzung ist
# Beschreibung der Behälter für Lebensmittel, Gewürze etc.


class Tools:
    def __init__(self, tool_id, tool_type, usage_tags):
        self.tool_id = tool_id
        self.tool_type = tool_type
        self.usage_tags = usage_tags


class Container(Tools):
    def __init__(self, tool_id, tool_type, usage_tags, capacity):
        Tools.__init__(self, tool_id, tool_type, usage_tags)
        self.capacity = capacity
