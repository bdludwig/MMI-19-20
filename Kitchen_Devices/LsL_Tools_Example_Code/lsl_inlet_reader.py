import pylsl
import queue
import threading
from typing import List, Generic, TypeVar

SampleType = TypeVar('SampleType')


class LSLInletReader(Generic[SampleType]):
    """
    An instance represents one "stream reading thread" that is used by StreamProcessor.
    """
    def __init__(self,
                 stream_info: pylsl.StreamInfo,
                 sample_sink: 'queue.Queue[(pylsl.StreamInlet, List[SampleType], float)]'):
        """
        Provide the stream that should be red and the queue where its output shall be pushed.

        :param stream_info: The pylsl.StreamInfo of the input stream that shall be red by this thread.
        :param sample_sink: A queue that is shared by all instances. Whenever a sample was pulled by the stream
                            a tuple (<stream info>, <sample>, <corrected timestamp>) will be put in the queue.
        """
        self.sample_sink = sample_sink
        thread_name = "Reader for stream " + stream_info.name()
        self.thread: threading.Thread = threading.Thread(target=self.sample_reader_loop,
                                                         args=(stream_info,),
                                                         name=thread_name)
        self.thread.start()

    def sample_reader_loop(self, stream_info: pylsl.StreamInfo):
        inlet: pylsl.StreamInlet = pylsl.StreamInlet(stream_info)
        while True:
            sample, timestamp = inlet.pull_sample()
            self.sample_sink.put((inlet, sample, timestamp + inlet.time_correction()))
