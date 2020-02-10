# Beschreibung des vorhandenen Koch- und Essgeschirrs und  ob es in Benutzung ist
# Beschreibung der Behälter für Lebensmittel, Gewürze etc.


class Tool:
    def __init__(self, tool_id, tool_type, usage_tags, location, is_in_location):
        self.tool_id = tool_id
        self.tool_type = tool_type
        self.usage_tags = usage_tags
        self.location = location
        self.is_in_location = is_in_location
