import argparse
import math
import os
import sys
import time

import numpy
import pylsl
import pyxdf

# how close the timestamps of two samples are allowed to be (in seconds) before they will be sent as a single chunk
MINIMUM_SAMPLE_DISTANCE = 0.01


def add_metadata(src, dest):
    if src is None:
        return

    if isinstance(src, list):
        if len(src) == 1:
            add_metadata(src[0], dest)
            return
        else:
            raise ValueError('src has to be a dict or a list with size 1 which can be unboxed. For a bigger list there'
                             'would be no way to retrieve the children\'s names.')

    if isinstance(src, dict):
        for key, value in src.items():

            if not isinstance(value, list):
                raise ValueError('Only lists are expected here.')

            for element in value:
                if isinstance(element, dict):
                    child = dest.append_child(key)
                    add_metadata(element, child)
                else:
                    if element:
                        dest.append_child_value(key, element)
                    else:
                        dest.append_child_value(key, "")
        return

    raise ValueError('The source may only consist out of nested lists and dicts.')


parser = argparse.ArgumentParser(description='Replays previously recorded LSL streams.')
parser.add_argument('filepath', type=str, help='The path to the xdf[z] file')
parser.add_argument('--only-certain-streams', '-oc', dest='selectedStreamIndices', type=int, nargs='+',
                    default=None, help='Subset of streams to be replayed. The streams are specified by their index.')
parser.add_argument('--no-delay', '-nd', action='store_false', dest='noDelay',
                    help='Whether samples should be pushed in \"real time\" or as fast as'
                         ' possible. This breaks LSL\'s clock synchronization mechanism,'
                         ' so only use this option if you ignore all timestamps anyway and'
                         'also will not re-record the replayed streams.')
args = parser.parse_args()

streams, fileInfo = pyxdf.load_xdf(args.filepath)

selectedStreamIndices = args.selectedStreamIndices

fileName = os.path.basename(args.filepath)

if selectedStreamIndices is not None:
    # removes duplicates
    selectedStreamIndices = set(selectedStreamIndices)
else:
    selectedStreamIndices = list(range(0, len(streams)))  # when no streams are specified all streams will be send

if max(selectedStreamIndices) >= len(streams):
    sys.exit("Only " + str(len(streams)) + " streams were recorded. Therefore there is no stream with index "
             + str(max(selectedStreamIndices)))

outlets = []
nextSampleOfStream = []  # index of the next sample of each stream that will be send
chunk_sizes = []  # how many samples should be published at once
for i in range(0, len(streams)):
    outlets.append(None)
    nextSampleOfStream.append(0)
    chunk_sizes.append(1)

print("Creating outlets")
print("\t[index]\t[name]")
for streamIndex in selectedStreamIndices:
    recordedInfo = streams[streamIndex]['info']

    stream_name = recordedInfo['name'][0]
    stream_type = recordedInfo['type'][0]
    stream_channel_format = recordedInfo['channel_format'][0]
    stream_channel_count = int(
        recordedInfo['channel_count'][0])  # load_xdf only returns strings; therefore casting is necessary
    stream_nominal_srate = float(recordedInfo['nominal_srate'][0])
    stream_source_id = recordedInfo['source_id'][0]
    if stream_source_id is None:
        stream_source_id = "Replay - Stream: " + stream_name + " - Type: " + stream_type
    stream_source_id += " (replayed from " + fileName + ")"

    outletInfo = pylsl.StreamInfo(stream_name, stream_type, stream_channel_count, stream_nominal_srate, stream_channel_format,
                            stream_source_id)

    recordedMetadata = recordedInfo['desc']
    outletMetadata = outletInfo.desc()

    add_metadata(recordedMetadata, outletMetadata)

    outlets[streamIndex] = pylsl.StreamOutlet(outletInfo)
    print("\t" + str(streamIndex) + "\t" + stream_name)

    # calculates how many samples will be send as a chunk; 1 means that each sample is send individually
    if stream_nominal_srate != 0:  # 0 means 'variable sampling rate'
        chunk_sizes[streamIndex] = max(1, math.floor(MINIMUM_SAMPLE_DISTANCE * stream_nominal_srate))

# this is the easiest way to read from terminal in both python2 and python3
# https://stackoverflow.com/questions/21731043/use-of-input-raw-input-in-python-2-and-3
# raw_input (python2) has been renamed to input in python3
# input also exists in python2 but refers to a different function
try:
    # noinspection PyShadowingBuiltins
    input = raw_input
except NameError:
    pass

print("All outlets were created. Now you can connect your inlets...")
input("Press Enter to play the recorded data...")

virtualTimeOffset = 0
if args.noDelay:
    virtualTime = None
    for stream in streams:
        if virtualTime is None or stream['time_stamps'][0] < virtualTime:
            # determine when the recording started
            virtualTime = stream['time_stamps'][0]

    virtualTimeOffset = pylsl.local_clock() - virtualTime
    print("Offsetting replayed timestamps by " + str(virtualTimeOffset))

# replay the recording
while len(selectedStreamIndices) > 0:  # streams get removed from the list if there are no samples left to play
    nextStreamIndex = None
    nextBlockingTimestamp = None

    # determine which stream to send next
    for i in selectedStreamIndices:
        stream = streams[i]

        # when a chunk can be send depends on it's last sample's timestamp
        blockingElementIdx = nextSampleOfStream[i] + chunk_sizes[i] - 1
        blockingTimestamp = stream['time_stamps'][blockingElementIdx]

        if nextBlockingTimestamp is None or blockingTimestamp < nextBlockingTimestamp:
            nextStreamIndex = i
            nextBlockingTimestamp = blockingTimestamp

    # retrieve the data and timestamps to be send
    nextStream = streams[nextStreamIndex]
    chunkSize = chunk_sizes[nextStreamIndex]

    nextChunkRangeStart = nextSampleOfStream[nextStreamIndex]
    nextChunkRangeEnd = nextChunkRangeStart + chunkSize

    nextChunkTimestamps = nextStream['time_stamps'][nextChunkRangeStart: nextChunkRangeEnd]
    nextChunkValues = nextStream['time_series'][nextChunkRangeStart: nextChunkRangeEnd]

    # prepare the data (if necessary)
    if isinstance(nextChunkValues, numpy.ndarray):
        # load_xdf loads numbers into numpy arrays (strings will be put into lists). however, LSL doesn't seem to
        # handle them properly as providing data in numpy arrays leads to falsified data being sent. therefore the data
        # are converted to lists
        nextChunkValues = nextChunkValues.tolist()

    # load_xdf only returns floating point numbers which can not be pushed into an integer outlet
    if nextStream['info']['channel_format'][0] in ['int8', 'int16', 'int32', 'int64']:
        for sample_idx, sample in enumerate(nextChunkValues):
            for channel_idx, value in enumerate(sample):
                nextChunkValues[sample_idx][channel_idx] = int(value)

    nextSampleOfStream[nextStreamIndex] += chunkSize

    stream_length = int(nextStream['footer']['info']['sample_count'][0])
    # calculates a lower chunk_size if there are not enough samples left for a "complete" chunk
    if stream_length < nextSampleOfStream[nextStreamIndex] + chunkSize:
        chunk_sizes[nextStreamIndex] = stream_length - nextSampleOfStream[nextStreamIndex]

    # remove this stream from the list if there are no remaining samples
    if nextSampleOfStream[nextStreamIndex] >= stream_length:
        selectedStreamIndices.remove(nextStreamIndex)

    if args.noDelay:
        virtualTime = pylsl.local_clock() - virtualTimeOffset
        sleepDuration = nextBlockingTimestamp - virtualTime
        if sleepDuration > 0:
            time.sleep(sleepDuration)

    outlet = outlets[nextStreamIndex]
    nextStreamName = nextStream['info']['name'][0]
    if chunkSize == 1:
        print(str(nextChunkTimestamps[0] + virtualTimeOffset) + "\t" + nextStreamName + "\t" + str(nextChunkValues[0]))
        outlet.push_sample(nextChunkValues[0], nextChunkTimestamps[0] + virtualTimeOffset)
    else:
        # according to the documentation push_chunk can only be invoked with exactly one (the last) time stamp
        outlet.push_chunk(nextChunkValues, nextChunkTimestamps[-1] + virtualTimeOffset)
        # chunks are not printed to the terminal because they happen hundreds of times per second and therefore
        # would make the terminal output unreadable
