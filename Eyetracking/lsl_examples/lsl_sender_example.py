import time
import pylsl

outlet_info = pylsl.StreamInfo(
    "Teststream",  # name
    "event markers",  # type
    2,  # channel_count
    pylsl.IRREGULAR_RATE,  # samplerate
    pylsl.cf_string,  # channel_format
    "TestID123")  # source_id
outlet_info.desc().append_child_value("manufacturer",
                                      "UR Informationswissenschaft")

channels = outlet_info.desc().append_child("channels")

test_channel1 = channels.append_child("channel")
test_channel1.append_child_value(
    "label",
    "testchannel1")
test_channel1.append_child_value("type", "event markers")
test_channel1.append_child_value("Zusatzinfo",
                                 "Dies ist der erste Testchannel!")

test_channel2 = channels.append_child("channel")
test_channel2.append_child_value(
    "label",
    "testchannel2")
test_channel1.append_child_value("type", "event markers")
test_channel1.append_child_value("Zusatzinfo",
                                 "Dies ist der zweite Testchannel!")


outlet = pylsl.StreamOutlet(outlet_info)

while True:
    outlet.push_sample(["eins!", "zwei!"])
    time.sleep(1)
