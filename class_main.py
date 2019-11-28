import class_kitchen


if __name__ == '__main__':

    myKitchen = class_kitchen.Kitchen("My Kitchen")
    myKitchen.initialize_kitchen_from_config(myKitchen)

    coffee_Machines = myKitchen.getInteractiveAppliances("coffeeMachine")
    coffee_Machines[0].brewing()

    water_heaters = myKitchen.getInteractiveAppliances("waterHeater")
    water_heaters[0].heating()


