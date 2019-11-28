import json
import class_furniture
import class_appliance


class Kitchen:

    def __init__(self, name):
        self.name = name
        self.furnitureList = []
        self.applianceList = []

    @staticmethod
    def initialize_furniture(self, data):
        for key, value in data.items():
            if key == "storage":
                for x in data["storage"]:
                    buffer = class_furniture.furniture(x["name"], x["location"])
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
                    buffer = class_appliance.stove(x["status"],x["operable"], x["hotplate1"], x["hotplate2"], x["hotplate3"], x["hotplate4"])
                    self.applianceList.append(buffer)

    @staticmethod
    def initialize_kitchen_from_config(self):
        with open("Kitchen_Config/config.json") as config:
            kitchen_config = json.load(config)

        self.initialize_interactive_appliances(self, kitchen_config["interactiveAppliance"])
        self.initialize_furniture(self, kitchen_config["furniture"])

        for x in self.applianceList:
            print(type(x).__name__)

        for x in self.furnitureList:
            print(x.name)

    def getInteractiveAppliances(self, appliance):
        #Returns a List of the Appliances, depending on the name of the appliances
        appliances = []
        for x in self.applianceList:
            if type(x).__name__ == appliance:
                appliances.append(x)
        return appliances

