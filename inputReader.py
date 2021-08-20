from vectormath import Vector3
import numpy as np
import re
from Camera import Camera
from Screen import Screen
from Light import Light
from Finishing import Finishing
from Object import Object
from Sphere import Sphere
from Polyhedron import Polyhedron
import Pigment
import math 
import sys

def normalize(vector):
    norm = np.linalg.norm(vector)
    if norm < sys.float_info.epsilon: 
        return vector
    else:
        return vector / np.linalg.norm(vector)

def project(f_vector, s_vector):
    dot_prod = np.dot(f_vector, s_vector)
    mag_2 = pow(np.linalg.norm(f_vector), 2)
    factor = dot_prod / mag_2
    return f_vector * factor

def screen_params(camera, width, height):
    screen = Screen(0, 0, 0, 0, 0, 0, 0)
    screen.height = 2 * math.tan(math.radians(camera.y_opening / 2)) * np.linalg.norm(camera.center - camera.position)
    screen.width = (screen.height * width) / height
    screen.r_dir = normalize(np.cross(camera.direction, camera.up))
    screen.b_dir = normalize(camera.up * -1)
    screen.top_left = camera.center - (screen.r_dir * (screen.width / 2)) + (camera.up * (screen.height / 2))
    screen.pixel_w = screen.width / width
    screen.pixel_h = screen.height / height
    return screen

def return_scene_params(path, width, height):
    camera = Camera(None, None, None, None, 0)
    lights = []
    pigments = []
    finishings = []
    objects = []
    aux_texmap = None
    aux_polyhedron = None
    aux_obj = None
    read_light = False
    read_pigments = False
    read_finishings = False
    read_objs = False
    texmap_args = 0
    polyhedron_faces = 0
    read_texmap = False
    read_polyhedron = False
    faces_arr = []
    with open(path, 'r') as reader:
        line_count = 0
        count_lights = 0
        count_pigments = 0
        count_finishings = 0
        count_objs = 0
        for line in reader:
            line_vars = list(filter(None, re.sub(r"\s+", '  ', line).split('  ')))
            if line_count == 0:
                camera.position = Vector3(float(line_vars[0]), float(line_vars[1]), float(line_vars[2]))
            elif line_count == 1:
                center = Vector3(float(line_vars[0]), float(line_vars[1]), float(line_vars[2]))
                camera.center = center
                camera.direction = normalize(center - camera.position)
            elif line_count == 2:
                up = normalize(Vector3(float(line_vars[0]), float(line_vars[1]), float(line_vars[2])))
                up -= project(camera.direction, up)
                camera.up = normalize(up)                    
            elif line_count == 3:
                camera.y_opening = float(line_vars[0])
            elif line_count == 4:
                count_lights = int(line_vars[0])
                read_light = True
            elif read_light:
                lights.append(Light(Vector3(float(line_vars[0]), float(line_vars[1]), float(line_vars[2])), Vector3(float(line_vars[3]), float(line_vars[4]), float(line_vars[5])), Vector3(float(line_vars[6]), float(line_vars[7]), float(line_vars[8]))))
                count_lights -= 1
                if count_lights == 0:
                    read_light = False
                    read_pigments = True
            elif read_pigments:
                if count_pigments == 0:
                    count_pigments = int(line_vars[0])
                else:
                    if line_vars[0] == 'solid':
                        pigments.append(Pigment.Solid(Vector3(float(line_vars[1]), float(line_vars[2]), float(line_vars[3]))))
                        count_pigments -= 1
                    elif line_vars[0] == 'checker':
                        pigments.append(Pigment.Checker(Vector3(float(line_vars[1]), float(line_vars[2]), float(line_vars[3])), Vector3(float(line_vars[4]), float(line_vars[5]), float(line_vars[6])), float(line_vars[7])))
                        count_pigments -= 1
                    elif line_vars[0] == 'texmap':
                        aux_texmap = Pigment.Texmap(line_vars[1], None, None)
                        read_texmap = True
                        texmap_args = 2
                    elif read_texmap:
                        if texmap_args == 2:
                            aux_texmap.p0 = [float(line_vars[0]), float(line_vars[1]), float(line_vars[2]), float(line_vars[3])]
                        elif texmap_args == 1:
                            aux_texmap.p1 = [float(line_vars[0]), float(line_vars[1]), float(line_vars[2]), float(line_vars[3])]
                        texmap_args -= 1
                        if texmap_args == 0:
                            read_texmap = False
                            count_pigments -= 1
                            aux_texmap.load_tex()
                            pigments.append(aux_texmap)
                    if count_pigments == 0:
                        read_pigments = False
                        read_finishings = True
            elif read_finishings:
                if count_finishings == 0:
                    count_finishings = int(line_vars[0])
                else:
                    finishings.append(Finishing(float(line_vars[0]), float(line_vars[1]), float(line_vars[2]), float(line_vars[3]), float(line_vars[4]), float(line_vars[5]), float(line_vars[6])))
                    count_finishings -= 1
                    if count_finishings == 0:
                        read_finishings = False
                        read_objs = True
            elif read_objs:
                if count_objs == 0:
                    count_objs = int(line_vars[0])
                else:
                    if line_vars[2] == 'sphere':
                        objects.append(Object(pigments[int(line_vars[0])], finishings[int(line_vars[1])], Sphere(Vector3(float(line_vars[3]), float(line_vars[4]), float(line_vars[5])), float(line_vars[6]))))
                    elif line_vars[2] == 'polyhedron':
                        faces_arr = []
                        aux_obj = Object(pigments[int(line_vars[0])], finishings[int(line_vars[1])], None)
                        aux_polyhedron = Polyhedron(int(line_vars[3]), [])
                        polyhedron_faces = int(line_vars[3])
                        read_polyhedron = True
                    elif read_polyhedron: 
                        faces_arr.append([float(line_vars[0]), float(line_vars[1]), float(line_vars[2]), float(line_vars[3])])
                        polyhedron_faces -= 1
                        if polyhedron_faces == 0:
                            aux_polyhedron.faces_arr = faces_arr
                            aux_obj.tp = aux_polyhedron
                            objects.append(aux_obj)
                            read_polyhedron = False
            line_count += 1
    screen = screen_params(camera, width, height)
    return camera, lights, pigments, finishings, objects, screen
