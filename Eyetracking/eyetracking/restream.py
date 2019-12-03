import csv
from GazeDetection import GazeDetection

def callback(message):
    global outlet
    try:
        gaze = gazeDetection.main_method(message)
        print('gaze:')
        print(gaze)
    except Exception as e:
        print(e)

def readcsvPanda(path):
    input_file = csv.DictReader(open(path))
    for row in input_file:
        message=dict(row)
        for key in message:
            if key !='client_id':
                message[key]=float(message[key])
        callback(message)

if __name__ == "__main__":
    gazeDetection = GazeDetection()
    readcsvPanda('data/gaze_raw_2019_11_30_22:14:14.csv')

