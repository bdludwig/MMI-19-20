import time
import pylsl
import queue
from threading import Thread


class LslEventBroadcaster(Thread):

    def __init__(self, event_queue):
        self.event_queue = event_queue
        outlet_info = pylsl.StreamInfo("Kitchen Devices",
                                   "event markers",
                                   4,
                                   pylsl.IRREGULAR_RATE,
                                   pylsl.cf_string,
                                   "ID_Kitchen_Devices")

        outlet_info.desc().append_child_value("manufacturer", "UR Informationswissenschaft MMI 2019_2020")
        channels = outlet_info.desc().append_child("channels")

        devices_events_channel = channels.append_child("channel")
        devices_events_channel.append_child_value("label", "Device ID")
        devices_events_channel.append_child_value("type", "event markers")
        devices_events_channel.append_child_value("Zusatzinfo", "ID")

        devices_events_channel = channels.append_child("channel")
        devices_events_channel.append_child_value("label", "Device Type")
        devices_events_channel.append_child_value("type", "event markers")
        devices_events_channel.append_child_value("Zusatzinfo", "Device Type")

        devices_events_channel = channels.append_child("channel")
        devices_events_channel.append_child_value("label", "Device Location")
        devices_events_channel.append_child_value("type", "event markers")
        devices_events_channel.append_child_value("Zusatzinfo", "Device Location")

        devices_events_channel = channels.append_child("channel")
        devices_events_channel.append_child_value("label", "Nutzer Aktion")
        devices_events_channel.append_child_value("type", "event markers")
        devices_events_channel.append_child_value("Zusatzinfo", "put in / take out")

        self.outlet = pylsl.StreamOutlet(outlet_info)

        Thread.__init__(self)
        self.daemon = True
        self.start()

    def run(self):
        while True:
            try:
                input_value = self.event_queue.get(block=False)
            except queue.Empty:
                # No new input
                pass
            else:
                self.outlet.push_sample(input_value)

