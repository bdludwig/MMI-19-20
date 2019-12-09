import class_kitchen

# import http.server
# import socketserver

if __name__ == '__main__':
    # Initalisieren der Küche:
    myKitchen = class_kitchen.Kitchen("My Kitchen")
    myKitchen.initialize_kitchen_from_config(myKitchen)

    # Man bekommt eine Liste mit allen Kaffemaschinenobjekten:
    coffee_Machines = myKitchen.getInteractiveAppliances("coffeeMachine")
    coffee_Machines[0].brewing()

    # Man bekommt eine Liste mit allen Wasserkochern:
    water_heaters = myKitchen.getInteractiveAppliances("waterHeater")
    water_heaters[0].heating()

    # Man bekommt eine Liste mit allen Werkzeugen:
    Tools = myKitchen.getTools()
    for tool in Tools:
        print("Der Gegenstand " + tool.tool_id + " befindet sich in " + myKitchen.getLocationWithId(tool.tool_id))

