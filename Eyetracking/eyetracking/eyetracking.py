import json
import subprocess
import threading
import ast

import pylsl
from GazeDetection import GazeDetection
import time

def startSingelCam(name, device, callback):
    print('start:' + name + ' ' + device)
    proc = subprocess.Popen('/Users/mmi/Desktop/Eyetracking/OpenFace/build/bin/FeatureExtraction ' + device, shell=True,
                            stdout=subprocess.PIPE)
    while True:
        input = proc.stdout.readline()
        input = input.decode('utf-8').rstrip()
        # print(input)
        if input.startswith("<relevant_entry>") and input.endswith('</relevant_entry>'):
            # print("Message received!" + str(time.time()))
            message_to_push = str(input)[16:len(input) - 17]
            # print('push message:')
            message_to_push = ast.literal_eval(message_to_push)
            message_to_push['timestamp'] = time.time()
            message_to_push['client_id'] = name
            #print(message_to_push)
            callback(message_to_push)

outlet=None
def createLSL():
    global outlet
    outlet_info = pylsl.StreamInfo(
        "MMIEyetrackingStream",  # name
        "Eyetracking data",  # type
        2,  # channel_count
        pylsl.IRREGULAR_RATE,  # samplerate
        pylsl.cf_string,  # channel_format
        "MMIID1")  # source_id

    channels = outlet_info.desc().append_child("channels")

    eyeleft_channel = channels.append_child("channel")
    eyeleft_channel.append_child_value("label","left eye channel")
    eyeleft_channel.append_child_value("type", "left eye")
    eyeleft_channel.append_child_value("additional_info","eyetracking data for the left eye")

    eyeright_channel = channels.append_child("channel")
    eyeright_channel.append_child_value("label","right eye channel")
    eyeright_channel.append_child_value("type", "right eye")
    eyeright_channel.append_child_value("additional_info","eyetracking data for the right eye")

    outlet = pylsl.StreamOutlet(outlet_info)

def callback(message):
    global outlet
    try:
        output = gazeDetection.main_method(message)
        print(json.dumps(output))
        outlet.push_sample([json.dumps(output['left']), json.dumps(output['right'])])
    except Exception as e:
        print(e)

if __name__ == "__main__":
    gazeDetection = GazeDetection()
    createLSL()
    cam1 = threading.Thread(target=startSingelCam, args=['cam_3', '-device 0', callback])
    cam1.start()
    '''cam2 = threading.Thread(target=startSingelCam, args=['cam_4', '-device 3', callback])
    cam2.start()
    cam3 = threading.Thread(target=startSingelCam, args=['cam_3', '-device 1', callback])
    cam3.start()
    cam4 = threading.Thread(target=startSingelCam, args=['cam_4', '-device 2', callback])
    cam4.start()'''
