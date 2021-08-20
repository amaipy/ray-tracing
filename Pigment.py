import re
from vectormath import Vector3
import numpy as np

class Solid:
    def __init__(self, color):
        self.color = color

class Checker:
    def __init__(self, f_color, s_color, side):
        self.f_color = f_color
        self.s_color = s_color
        self.side = side
    
class Texmap:
    def __init__(self, tex_path, p0, p1):
        self.tex_path = tex_path
        self.p0 = p0
        self.p1 = p1
        self.data = None
        self.height = 0
        self.width = 0
    
    def load_tex(self):
        typ = None
        pass_header = False
        pass_width = False
        width = 0
        height = 0
        #max_color = 0
        data = []
        with open(self.tex_path, 'rb') as f:

            for count, ln in enumerate(f):

                if count == 0:
                    typ = ln.decode()
                    typ = list(filter(None, re.sub(r"\s+", '  ', typ).split('  ')))[0]

                elif not pass_header:
                    if not ln.decode()[0] == '#':
                        line = ln.decode()
                        line = list(filter(None, re.sub(r"\s+", '  ', line).split('  ')))
                        if not pass_width:
                            width = int(line[0])
                            height = int(line[1])
                            pass_width = True
                        else:
                            #max_color = int(line[0])
                            pass_header = True

                else:
                    data = ln

        k = 0
        array = np.empty((height, width), dtype=list)
        for i in range(height):
            for j in range(width):
                r = data[k] & 0xFF
                k += 1
                g = data[k] & 0xFF
                k += 1
                b = data[k] & 0xFF
                k += 1
                array[i][j] = [r/255, g/255, b/255]
        
        self.height = height
        self.width = width
        self.data = array