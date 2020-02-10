import json
import class_furniture
import class_appliance
import Kitchen_Devices.Smart_Kitchen_Classes.class_tools as tools


class Kitchen:

    def __init__(self, name, event_queue):
        self.name = name
        self.furnitureList = []
        self.applianceList = []
        self.toolList = []
        self.eventQueue = event_queue

    @staticmethod
    def initialize_furniture(self, data):
        for key, value in data.items():
            if key == "storage":
                for x in data["storage"]:
                    buffer = class_furniture.Storage(x["name"], x["location"])
                    self.furnitureList.append(buffer)

    @staticmethod
    def initialize_interactive_appliances(self, data):
        for key, value in data.items():
            if key == "coffeeMachine":
                for x in data["coffeeMachine"]:
                    buffer = class_appliance.coffeeMachine(x["status"], x["operable"])
                    self.applianceList.append(buffer)
            if key == "waterHeater":
                for x in data["waterHeater"]:
                    buffer = class_appliance.waterHeater(x["status"], x["operable"])
                    self.applianceList.append(buffer)
            if key == "oven":
                for x in data["oven"]:
                    buffer = class_appliance.oven(x["status"], x["operable"])
                    self.applianceList.append(buffer)
            if key == "dishwasher":
                for x in data["dishwasher"]:
                    buffer = class_appliance.dishwasher(x["status"], x["operable"])
                    self.applianceList.append(buffer)
            if key == "microwave":
                for x in data["microwave"]:
                    buffer = class_appliance.microwave(x["status"], x["operable"], x["watt"])
                    self.applianceList.append(buffer)
            if key == "stove":
                for x in data["stove"]:
                    buffer = class_appliance.stove(x["status"], x["operable"], x["hotplate1"], x["hotplate2"],
                                                   x["hotplate3"], x["hotplate4"])
                    self.applianceList.append(buffer)

    @staticmethod
    def initialize_tools(self, data):
        for tool in data:
            if tool['is_in_location'] == "true":
                is_in_location = True
            else:
                is_in_location = False
            item = tools.Tool(tool['tool_id'], tool['tool_type'], tool['usage_tags'], tool['location'], is_in_location)
            self.toolList.append(item)

            for storage in self.furnitureList:
                if storage.name == item.location:
                    storage.putItem(item)

    @staticmethod
    def initialize_kitchen_from_config(self):
        with open("../Kitchen_Config/config.json") as config:
            kitchen_config = json.load(config)

        self.initialize_interactive_appliances(self, kitchen_config["interactiveAppliance"])
        self.initialize_furniture(self, kitchen_config["furniture"])
        self.initialize_tools(self, kitchen_config["tools"])

    def getInteractiveAppliances(self, appliance):
        # Returns a List of the Appliances, depending on the name of the appliances
        appliances = []
        for x in self.applianceList:
            if type(x).__name__ == appliance:
                appliances.append(x)
        return appliances

    def getTools(self):
        return self.toolList

    def getLocationWithId(self, item_id):
        for storage in self.furnitureList:
            items = storage.getContent()
            for item in items:
                if item.tool_id == item_id:
                    return storage.name

    def getToolById(self, tool_id):
        for tool in self.toolList:
            if tool.tool_id == tool_id:
                return tool

    def updateTool(self, data):
        for tool in self.toolList:
            if data[0] == tool.tool_id:
                if tool.is_in_location:
                    tool.is_in_location = False
                    self.eventQueue.put([data[0], tool.tool_type, tool.location, "Take out"])
                else:
                    tool.is_in_location = True
                    self.eventQueue.put([data[0], tool.tool_type, tool.location, "Put in"])
