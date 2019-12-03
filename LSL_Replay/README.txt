From https://bitbucket.org/ur-infwiss/lsl_replay

This script is intended for debugging purposes of LSL related programs.

It replays all LSL data that were captured during a previous session using the official LabRecorder (which can be
downloaded here: ftp://sccn.ucsd.edu/pub/software/LSL/Apps/)

INSTALLATION
This script should run on any operating system that is supported by python. It was tested under Windows using Python 3.7.0.
It's only dependencies are an installed python interpreter and the LSL library for python.
To install the library type "python -m pip install pylsl" into the powershell / bash

USAGE
A script invocation has to match this pattern: python .\lsl_replay.py PATH_OF_THE_RECORDING [--only-certain LIST_OF_NUMBERS] [--no-delay]
PATH_OF_THE_RECORDING: The path to the previously created xdf/xdfz recording. This parameter is MANDATORY
--only-certain: This argument is optional. It is meant to specify the LSL streams that should be replayed. It has to be
                followed by a list (which may NOT be comma separated) of the desired stream's indices. Not providing
                this arguments leads to all streams being replayed.
--no-delay:     This flag is optional. If it is set all recorded data will be flushed 'all at once'; if not the
                recorded data will be played in 'real time'.

EXAMPLE
python .\lsl_replay.py C:\Users\<placeholder>\lsl_recordings\demo_recording.xdfz --only-certain 1 3 --no-delay
This command will only play the streams 1 and 3 whose data will be flushed all at once.