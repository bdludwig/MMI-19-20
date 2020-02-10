import Kitchen_Devices.Smart_Kitchen_Classes.class_kitchen as kitchen
import Kitchen_Devices.Smart_Kitchen_Classes.LSL_Integration.lsl_broadcaster as lsl
import time
import Kitchen_Devices.Python_Server.server as serv
import queue

if __name__ == '__main__':
    event_queue = queue.Queue()

    myKitchen = kitchen.Kitchen("My Kitchen", event_queue)
    myKitchen.initialize_kitchen_from_config(myKitchen)

    kitchen_server = serv.SocketServer('', 65432, myKitchen)

    event_broadcaster = lsl.LslEventBroadcaster(event_queue)

    while True:
        # Loop for testing and keeping Server and Broadcast Thread alive
        # event_queue.put(["Test1", "Test2", "Test3", "Test4"])
        time.sleep(5)



