"""Example program to show how to read a multi-channel time series from LSL."""

import pylsl

# first resolve an EEG stream on the lab network
print("looking for Kitchen Devices Stream")
streams = pylsl.resolve_byprop('name', "Kitchen Devices")

if streams:
    print("Found Stream!")
else:
    print("Found no Stream")

# create a new inlet to read from the stream
inlet = pylsl.StreamInlet(streams[0])

while True:
    # get a new sample (you can also omit the timestamp part if you're not
    # interested in it)
    sample, timestamp = inlet.pull_sample()
    print(timestamp, sample)