import numpy as np


class AOI(object):
    '''
    P1-----------P2
    |             |
    |  cross_hair |
    |             |
    P3-----------P4

    v1: P1--->P2
    v2: P1--->P3

    cross_hair['cross_hair_x']: cross_hair_x
    cross_hair['cross_hair_y']: cross_hair_y
    cross_hair['cross_hair_z']: cross_hair_y

    x: min x
    y: min y
    z: min z

    w: x dim
    h: y dim
    d: z dim

    points: gaze hits
    '''

    def __init__(self, p1, p2, p3, cross_hair, color, aoi_id, title):
        self.title = title
        self.aoi_id = aoi_id
        self.color = color
        self.p1 = np.array(p1, dtype=float)
        self.p2 = np.array(p2, dtype=float)
        self.p3 = np.array(p3, dtype=float)
        self.v1 = np.array(self.p2 - self.p1, dtype=float)
        self.v2 = np.array(self.p3 - self.p1, dtype=float)
        self.p4 = np.array(self.p1 + self.v1 + self.v2, dtype=float)
        self.n = np.array(np.cross(self.v1, self.v2), dtype=float)
        self.x = min(self.p1[0], self.p2[0], self.p3[0], self.p4[0])
        self.y = min(self.p1[1], self.p2[1], self.p3[1], self.p4[1])
        self.z = min(self.p1[2], self.p2[2], self.p3[2], self.p4[2])
        self.w = max(self.p1[0], self.p2[0], self.p3[0], self.p4[0]) - self.x
        self.h = max(self.p1[1], self.p2[1], self.p3[1], self.p4[1]) - self.y
        self.d = max(self.p1[2], self.p2[2], self.p3[2], self.p4[2]) - self.z
        self.cross_hair_x = cross_hair[0]
        self.cross_hair_y = cross_hair[1]
        self.cross_hair_z = cross_hair[2]
        self.points = []
