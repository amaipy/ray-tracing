from Pigment import Solid, Checker
import math 
class Object:
    def __init__(self, pigment, finishing, tp):
        self.pigment = pigment
        self.finishing = finishing
        self.tp = tp

    def color(self, point):
        if isinstance(self.pigment, Solid):
            return self.pigment.color
        elif isinstance(self.pigment, Checker):
            val = math.floor(point[0] / self.pigment.side) + math.floor(point[1] / self.pigment.side) + math.floor(point[2] / self.pigment.side)
            val = val % 2

            if not val:
                return self.pigment.f_color
            else:
                return self.pigment.s_color
        else:
            s = self.pigment.p0[0] * point[0] + self.pigment.p0[1] * point[1] + self.pigment.p0[2] * point[2] + self.pigment.p0[3]
            r = self.pigment.p1[0] * point[0] + self.pigment.p1[1] * point[1] + self.pigment.p1[2] * point[2] + self.pigment.p1[3]
            i = (int)(r * self.pigment.height) % self.pigment.height
            j = (int)(s * self.pigment.width) % self.pigment.width
            if i < 0:
                i += self.pigment.height
            if j < 0:
                j += self.pigment.width
            return self.pigment.data[i][j]
