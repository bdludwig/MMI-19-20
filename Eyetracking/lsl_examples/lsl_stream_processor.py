import logging
import queue
from typing import List, Tuple, Optional

import pylsl
import xmltodict

from lsl_errors import *
from lsl_inlet_reader import LSLInletReader

logging.basicConfig(level=logging.INFO)


class StreamProcessor:
    """
    Read multiple lsl streams in threads and combine queue to one output stream.
    """
    INPUT_QUEUE_VALUE_TYPE = Tuple[pylsl.StreamInlet, List[Any], float]

    def __init__(self,
                 outlet_info: Optional[pylsl.StreamInfo],
                 inlets_predicate: str,
                 min_inlets: int = 1) -> None:
        """
        Specify output stream and predicate to select input streams.

        :param outlet_info: If not None this pylsl.StreamInfo will be used to
        generate a single output-stream.
        :param inlets_predicate: Predicate to select multiple output streams
                                 that will write to the queue (e.g.
                                 "type='fused arousal'").
        :param min_inlets: Number of minimum input streams the instance
        should wait for.
        """
        if outlet_info:
            self.outlet = pylsl.StreamOutlet(outlet_info)
        else:
            self.outlet = None
        logging.info("Waiting for %s streams with predicate %s.", min_inlets,
                     inlets_predicate)
        self.inlet_infos = pylsl.resolve_bypred(inlets_predicate, min_inlets)
        logging.info("Found streams.")
        self.input_queue: 'queue.Queue[' \
                          'StreamProcessor.INPUT_QUEUE_VALUE_TYPE]' = \
            queue.Queue()
        self.__inlet_readers = [LSLInletReader(stream_info, self.input_queue)
                                for stream_info in self.inlet_infos]


def get_channel_by_label(inlet_info: pylsl.StreamInfo,
                         channel_label: str) -> int:
    stream_info = xmltodict.parse(inlet_info.as_xml())
    stream_name = inlet_info.name()
    channels = stream_info["info"]["desc"]["channels"]["channel"]
    if not isinstance(channels, list):
        channels = [channels]
    person_channel = [index
                      for index, channel in enumerate(channels)
                      if channel["label"] == channel_label]
    number_of_channels = len(person_channel)
    if number_of_channels == 0:
        raise LslError(
            "A channel with given label {} could"
            "not be found in stream {}"
                .format(channel_label, stream_name))
    elif number_of_channels > 1:
        raise LslError(
            "Given label {} to select a single channel"
            "reslted in {} channels in stream {}"
                .format(channel_label,
                        number_of_channels,
                        stream_name))
    person_channel = person_channel[0]
    return person_channel
