import math
from Intersection import Intersection
from AOI import AOI
import json
import datetime
import time
import csv
import numpy as np


class GazeDetection:
    file_name_raw = ''
    header_file_row = []

    header_file_annotation = []
    config_file_name = 'config/cam_config.json'
    header_csv_config_file_name = 'config/header_csv_config.json'

    config_annotation_file_name = "config/aoi_config_filled.json"
    aoi_list = []

    TRANSFORMED_COORDS_GAZE = 0.0
    TRANSFORMED_GAZES = 0.0

    matrix_cache = {
        "cam_1": None,
        "cam_2": None,
        "cam_3": None,
        "cam_4": None
    }

    write_csv = False

    def __init__(self):
        self.setCameraMatrix()
        self.createAOIs()
        self.prepairLogging()

    def setCameraMatrix(self):
        with open(self.config_file_name, 'r') as f:
            config = json.load(f)
            self.matrix_cache["cam_1"] = self.get_transformation_matrix(config["cam_1"])
            self.matrix_cache["cam_2"] = self.get_transformation_matrix(config["cam_2"])
            self.matrix_cache["cam_3"] = self.get_transformation_matrix(config["cam_3"])
            self.matrix_cache["cam_4"] = self.get_transformation_matrix(config["cam_4"])

    def prepairLogging(self):
        if (self.write_csv):
            self.header_file_row = self.read_config(self.header_csv_config_file_name)['raw_header']
            self.header_file_annotation = self.read_config(self.header_csv_config_file_name)['annotation_header']
            self.create_raw_log_file()

    def createAOIs(self):
        self.config_annotation = self.read_config(self.config_annotation_file_name)
        for aoi in self.config_annotation:
            self.aoi_list.append(AOI([aoi["aoi_x_0"], aoi["aoi_y_0"], aoi["aoi_z_0"]],
                                     [aoi["aoi_x_1"], aoi["aoi_y_1"], aoi["aoi_z_1"]],
                                     [aoi["aoi_x_2"], aoi["aoi_y_2"], aoi["aoi_z_2"]],
                                     [aoi["cross_hair_x"], aoi["cross_hair_y"], aoi["cross_hair_z"]],
                                     aoi["color"], aoi["aoi_id"], aoi["name"]))

    # data evaluation called if new gaze data is detected
    def main_method(self, body):
        if (self.write_csv):
            self.save_to_raw_log_file(body)
        try:
            return self.transform_data(body)
        except Exception as identifier:
            return {
                "aoi_hits": "null (exception)"
            }

    # FILE OPERATION METHODS ---------------------------------------------------------
    def read_config(self, file_name):
        with open(file_name, encoding='utf-8') as f:
            return json.load(f)

    def create_log_file(self, test_person_id):
        self.file_name_annotation = str(test_person_id) + "_annotation_" + str(
            datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S')) + '.csv'
        self.write_to_csv_annotation(self.header_file_annotation)

    def create_raw_log_file(self):
        self.file_name_raw = 'gaze_raw_' + str(
            datetime.datetime.fromtimestamp(time.time()).strftime('%Y_%m_%d_%H:%M:%S')) + '.csv'
        self.write_to_csv(self.header_file_row)

    def write_to_csv(self, row):
        with open('data/' + self.file_name_raw, 'a') as csvFile:
            file_writer = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(row)

    def write_to_csv_annotation(self, row):
        with open('annotation/' + self.file_name_annotation, 'a') as csvFile:
            file_writer = csv.writer(csvFile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
            file_writer.writerow(row)

    def save_to_raw_log_file(self, data):
        row = self.map_values(data)
        self.write_to_csv(row)

    def map_values(self, data):
        return_row = [
            data["client_id"],
            time.mktime(time.gmtime()),
            data["face_id"],
            data["frame_number"],
            data["landmark_detection_success"],
            data["landmark_detection_confidence"],
            data["gaze_direction_0_x"],
            data["gaze_direction_0_y"],
            data["gaze_direction_0_z"],
            data["gaze_direction_0_x"],
            data["gaze_direction_0_y"],
            data["gaze_direction_0_z"],
            data["gaze_angle_x"],
            data["gaze_angle_y"],
            data["pose_Tx"],
            data["pose_Ty"],
            data["pose_Tz"],
            data["pose_Rx"],
            data["pose_Ry"],
            data["pose_Rz"]
        ]

        number = 0
        while (number <= 55):
            return_row.append(data["eye_lmk_x_" + str(number)])
            number += 1

        number = 0
        while (number <= 55):
            return_row.append(data["eye_lmk_y_" + str(number)])
            number += 1

        number = 0
        while (number <= 55):
            return_row.append(data["eye_lmk_X_" + str(number)])
            number += 1

        number = 0
        while (number <= 55):
            return_row.append(data["eye_lmk_Y_" + str(number)])
            number += 1

        number = 0
        while (number <= 55):
            return_row.append(data["eye_lmk_Z_" + str(number)])
            number += 1

        # if (self.annotation_state):
        #    return_row.insert(1, self.annotation_test_person_id)
        #    return_row.insert(2, self.annotation_pos)
        #    return_row.insert(3, self.annotation_aoi)
        return return_row


    # TRANSFORM COORDINATES METHODS ---------------------------------------------------------

    def get_eye_center(self,row, start, stop):
        center_x = 0
        center_y = 0
        center_z = 0
        for mark in range(start, stop):
            center_x += np.array(row['eye_lmk_X_%d' % mark])
            center_y += np.array(row['eye_lmk_Y_%d' % mark])
            center_z += np.array(row['eye_lmk_Z_%d' % mark])
        return center_x / 8, center_y / 8, center_z / 8


    # returns the Intersection
    def transform_data(self, body):
        eye_l_x, eye_l_y, eye_l_z = self.get_eye_center(body, 48, 56)
        eye_r_x, eye_r_y, eye_r_z = self.get_eye_center(body, 20, 28)

        COORDS_GAZE_Left = np.array([eye_l_x, eye_l_y, eye_l_z])
        COORDS_GAZE_Right = np.array([eye_r_x, eye_r_y, eye_r_z])

        GAZE_LEFT = np.array([body['gaze_direction_0_x'], body['gaze_direction_0_y'], body['gaze_direction_0_z']])
        GAZE_RIGHT = np.array([body['gaze_direction_1_x'], body['gaze_direction_1_y'], body['gaze_direction_1_z']])

        transformed_gaze_left,transformed_directions_left,detected_aois_with_cross_hair_dist_left = self.run_aoi_evaluation(
            self.aoi_list, self.matrix_cache[body['client_id']], COORDS_GAZE_Left, GAZE_LEFT)

        transformed_gaze_right,transformed_directions_right,detected_aois_with_cross_hair_dist_right = self.run_aoi_evaluation(
            self.aoi_list, self.matrix_cache[body['client_id']], COORDS_GAZE_Right, GAZE_RIGHT)

        return {
            "left":{
                "aoi_hits": detected_aois_with_cross_hair_dist_left,
                "gaze_start": transformed_gaze_left.tolist(),
                "gaze_direction": transformed_directions_left.tolist()
            },
            "right":{
                "aoi_hits": detected_aois_with_cross_hair_dist_right,
                "gaze_start": transformed_gaze_right.tolist(),
                "gaze_direction": transformed_directions_right.tolist()
            }
        }

    # calculates the Intersection
    def run_aoi_evaluation(self, aois, transformation_matrix, coordinates, gazes):
        #print('run_aoi_evaluation')
        # normierte Blickrichtung auf Startkoordinaten addieren
        gazes = np.array([gazes])
        coordinates = np.array([coordinates])
        gaze_ends = np.swapaxes(np.swapaxes(coordinates, 0, 1) + np.swapaxes(gazes, 0, 1) * 10000, 0, 1)
        # transformieren
        transformed_coordinates = self.apply_transformation(coordinates, transformation_matrix, swap=False)
        transformed_gaze_ends = self.apply_transformation(gaze_ends, transformation_matrix, swap=False)

        # Blickrichtung zurückrechnen und normalisieren
        transformed_directions = transformed_gaze_ends - transformed_coordinates
        transformed_directions = transformed_directions[0]
        transformed_gaze = np.array([self.normalize(transformed_directions)])

        # Intersektion Ojekte erstellen
        intersections = self.get_all_aois_intersection(transformed_coordinates, transformed_gaze, aois)

        # TODO was genau soll hier passieren??
        # Kürzeste Entfernung für jeden Punkt
        # distances = np.array([self.set_closest_intersection_and_get_distance(intersections[i]) for i in range(len(intersections))])
        # print('distances')
        # print(distances)
        detected_aois_with_cross_hair_dist = []

        for intersect in intersections:
            if (intersect.is_hit):
                detected_aois_with_cross_hair_dist.append([intersect.aoi.title, intersect.dist_cross_hair_end])

        # Start- und Endpunkte der Blicke (Start = Ende, wenn kein Schnittpunkt => Entfernung INF)
        # gaze_starts, gaze_ends = self.get_gaze_pairs(transformed_coordinates, transformed_gaze, distances)

        # gaze_starts = np.swapaxes(gaze_starts, 0, 1)
        # gaze_ends = np.swapaxes(gaze_ends, 0, 1)

        return transformed_gaze,transformed_directions,detected_aois_with_cross_hair_dist

    def get_transformation_matrix(self, cam_config):
        rot_x = self.rotate_x(math.radians(cam_config['rot_x']))
        rot_y = self.rotate_y(math.radians(cam_config['rot_y']))
        rot_z = self.rotate_z(math.radians(cam_config['rot_z']))

        s_x = self.scale_x(cam_config['s_x'])
        s_y = self.scale_y(cam_config['s_y'])
        s_z = self.scale_z(cam_config['s_z'])

        d = self.translate(cam_config['t_x'], cam_config['t_y'],cam_config['t_z'])

        return self.scale_x(-1) @ self.rotate_y(math.radians(-90)) @ d @ s_z @ s_y @ s_x @ rot_z @ rot_y @ rot_x @ self.scale_y(-1)

    # used in run_aoi_evaluation
    def apply_transformation(self, x, tr, swap=True):
        x = np.swapaxes(x, 0, 1)
        x = np.swapaxes(x, 0, 1)
        x = np.insert(x, 3, 1, axis=1)
        # print('x post insert')
        # Transponieren weil matrix vorne stehen muss
        x = x @ tr.T
        x = np.delete(x, 3, axis=1)
        if swap:
            return np.swapaxes(x, 0, 1)
            # return x
        else:
            return x

    # HELPER METHODS ----------------------------------------------------------------

    # used in run_aoi_evaluation
    def normalize(self, x):
        retVal = x / np.linalg.norm(x)
        # if math.isnan(retVal):
        #    return 0
        # else:
        # return retVal
        return retVal

    def translate(self, x, y, z):
        return np.array([
            [1, 0, 0, x],
            [0, 1, 0, y],
            [0, 0, 1, z],
            [0, 0, 0, 1]
        ])

    def rotate_x(self, phi):
        return np.array([
            [1, 0, 0, 0],
            [0, math.cos(phi), -math.sin(phi), 0],
            [0, math.sin(phi), math.cos(phi), 0],
            [0, 0, 0, 1]
        ])

    def rotate_y(self, phi):
        return np.array([
            [math.cos(phi), 0, math.sin(phi), 0],
            [0, 1, 0, 0],
            [-math.sin(phi), 0, math.cos(phi), 0],
            [0, 0, 0, 1]
        ])

    def rotate_z(self, phi):
        return np.array([
            [math.cos(phi), -math.sin(phi), 0, 0],
            [math.sin(phi), math.cos(phi), 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def scale_x(self, factor):
        return np.array([
            [factor, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def scale_y(self, factor):
        return np.array([
            [1, 0, 0, 0],
            [0, factor, 0, 0],
            [0, 0, 1, 0],
            [0, 0, 0, 1]
        ])

    def scale_z(self, factor):
        return np.array([
            [1, 0, 0, 0],
            [0, 1, 0, 0],
            [0, 0, factor, 0],
            [0, 0, 0, 1]
        ])

    # used in run_aoi_evaluation
    def get_all_aois_intersection(self, start_point, direction, aois):
        #print(start_point)
        #print(direction)
        # return np.array(
        # [self.get_single_aois_intersection(start_points[i], directions[i], aois) for i in range(len(start_points))])
        return [Intersection(start_point[0], direction[0], aoi) for aoi in aois]

    def set_closest_intersection_and_get_distance(self, intersection):
        closest = min(intersection, key=lambda x: x.distance)
        if closest.distance < np.inf:
            closest.aoi.points.append(closest.get_target())
        return closest.distance

    def get_gaze_pairs(self, coords, directions, distances):
        start_list = []
        end_list = []
        for i in range(len(coords)):
            if distances[i] < np.inf:
                start_list.append(coords[i])
                end_list.append(coords[i] + self.normalize(directions[i]) * distances[i])
        return np.array(start_list), np.array(end_list)

