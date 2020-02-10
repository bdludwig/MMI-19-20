import queue
import pylsl

import lsl_inlet_reader
import lsl_stream_processor

streams = pylsl.resolve_stream()
if streams:
    print("Currently available lsl streams:")
    for stream in streams:
        available_stream = ("name: {}, type: {}, number of channels: {}".
                            format(stream.name(), stream.type(),
                                   stream.channel_count()))
        print(available_stream)
else:
    print("At the moment no lsl stream could be found.")

# Init speech lsl stream for writing in queue
inlet_infos = pylsl.resolve_byprop("name", "Teststream")
print("Found stream.")
input_queue = queue.Queue()
inlet_readers = [
    lsl_inlet_reader.LSLInletReader(stream_info, input_queue)
    for stream_info in inlet_infos
]
while True:
    try:
        input_value = input_queue.get(block=False)
    except queue.Empty:
        # No new input
        pass
    else:
        inlet, sample, timestamp = input_value
        inlet_info = inlet.info()
        channel_id = lsl_stream_processor.get_channel_by_label(inlet_info, "testchannel2")
        sample = sample[channel_id]
        print("New input: {}".format(sample))
