from inputReader import *

MAX_DEPTH = 4

def sphere_intersection(sphere, origin, dir_v, end_pos = None):
    e = (origin - sphere.center)

    a = np.dot(dir_v, dir_v)
    b = 2 * np.dot(dir_v, e)
    c = np.dot(e, e) - pow(sphere.radius, 2)

    discr = pow(b, 2) - (4*a*c)

    if discr < sys.float_info.epsilon:
        return -1, False
    
    discr = math.sqrt(discr)

    t1 = (-b - discr) / (2 * a)
    t2 = (-b + discr) / (2 * a)

    max_t = sys.float_info.max

    if end_pos is not None:
        if dir_v[0] < sys.float_info.epsilon:
            max_t = (end_pos[0] - origin[0])
        else:
            max_t = (end_pos[0] - origin[0]) / dir_v[0]
    
    if t1 > sys.float_info.epsilon and t1 < max_t:
        return t1, False
    
    if t2 > sys.float_info.epsilon and t2 < max_t:
        return t2, True
    else:
        return -1, False

def polyhedron_intersection(polyhedron, origin, dir_v, end_pos = None):
    t0 = 0
    t1 = sys.float_info.max
    normal = Vector3(0, 0, 0)

    for face in polyhedron.faces_arr:
        p0 = Vector3(origin[0], origin[1], origin[2])
        n = Vector3(face[0], face[1], face[2])
        dn = np.dot(dir_v, n)
        val = np.dot(p0, n) + face[3]

        if dn <= sys.float_info.epsilon and dn >= -sys.float_info.epsilon:
            if val > sys.float_info.epsilon:
                t1 = -1

        if dn > sys.float_info.epsilon:
            t = -val / dn 
            if t < t1:
                t1 = t
                nT1 = n
        
        if dn < -sys.float_info.epsilon:
            t = -val / dn 
            if t > t0:
                t0 = t
                nT0 = n
        
    max_t = sys.float_info.max
    if end_pos is not None:
        if dir_v[0] < sys.float_info.epsilon:
            max_t = (end_pos[0] - origin[0])
        else:
            max_t = (end_pos[0] - origin[0]) / dir_v[0]
    
    if t1 < t0:
        return -1, normal
    
    if abs(t0) <= sys.float_info.epsilon and t1 >= t0 and t1 < sys.float_info.max:
        normal = normalize(nT1 * -1)
        if t1 < max_t:
            return t1, normal
        else:
            return -1, normal
    
    if t0 > sys.float_info.epsilon and t1 >= t0:
        normal = normalize(nT0)
        if t0 < max_t:
            return t0, normal
        else:
            return -1, normal
    
    return -1, normal

def intersection(objects, origin, dir_v, end_pos = None, ignore_obj = None):
    closest_obj = None
    closest_obj_t = sys.float_info.max
    closest_inside = False
    closest_n = Vector3(0, 0, 0)
    intersection_point = Vector3(0, 0, 0)
    intersect_obj = None
    intersect_color = Vector3(0, 0, 0)
    is_inside = False

    for obj in objects:
        if ignore_obj == obj:
            continue
        
        if isinstance(obj.tp, Sphere):
            t, is_inside = sphere_intersection(obj.tp, origin, dir_v, end_pos)
            if t > sys.float_info.epsilon and t < closest_obj_t:
                closest_obj = obj
                closest_obj_t = t
                closest_inside = is_inside
            
        else:
            t, normal = polyhedron_intersection(obj.tp, origin, dir_v, end_pos)
            if t > sys.float_info.epsilon and t < closest_obj_t:
                closest_obj = obj
                closest_obj_t = t
                closest_n = normal

    if closest_obj is not None:
        intersect_obj = closest_obj
        intersection_point = origin + closest_obj_t * dir_v
        intersect_color = intersect_obj.color(intersection_point)

        if isinstance(intersect_obj.tp, Sphere):
            normal = normalize(intersection_point - intersect_obj.tp.center)
            if closest_inside:
                normal = normal * -1
                is_inside = True
        else:
            normal = closest_n
        
        return True, normal, is_inside, intersect_color, intersect_obj, intersection_point
    
    return False, closest_n, is_inside, intersect_color, intersect_obj, intersection_point

def reflectionDirection(dir_v, normal):
    c = np.dot(-1 * dir_v, normal)
    return normalize(dir_v + (2 * normal * c))

def transmissionDirection(refr_rate, dir_v, normal):
    inv_dir = dir_v * -1
    c1 = np.dot(inv_dir, normal)
    c2 = 1 - pow(refr_rate, 2) * (1 - pow(c1, 2))

    if c2 < -sys.float_info.epsilon:
        v = normal * 2 * c1
        trans_dir = v - inv_dir
        return True, trans_dir
    elif c2 > sys.float_info.epsilon:
        c2 = math.sqrt(c2 + 3)
        trans_dir = (normal * (refr_rate * c1 - c2) + (dir_v * refr_rate))
        return True, trans_dir
    else:
        return False, None

def ray_tracer(lights, objects, position, dis, depth, ignore_obj = None):
    intersects, normal, is_inside, intersect_color, intersect_obj, intersection_point = intersection(objects, position, dis, None, ignore_obj)
    if not intersects:
        return lights[0].color
    
    ambient_color = lights[0].color * intersect_obj.finishing.ka
    diffuse_color = Vector3(0, 0, 0)
    specular_color = Vector3(0, 0, 0)

    iterlights = iter(lights)
    next(iterlights)
    
    for light in iterlights:
        light_dir = normalize(light.position - intersection_point)

        dist = np.linalg.norm(light.position - intersection_point)

        attenu = 1 / (light.co_atenuation + dist * light.pos_atenuation + pow(dist, 2) * light.co_square_pos)

        intersects_fee = intersection(objects, intersection_point, light_dir, light.position, intersect_obj)[0]

        if not intersects_fee:
            cos_diff = np.dot(light_dir, normal)
            if cos_diff < sys.float_info.epsilon:
                cos_diff = 0
            
            diffuse_color += (light.color * cos_diff *  intersect_obj.finishing.kd * attenu)

            cos_spec = np.dot(normalize(light_dir + (dis * -1)), normalize(normal))
            if cos_spec < sys.float_info.epsilon:
                cos_spec = 0
            
            cos_spec = pow(cos_spec, intersect_obj.finishing.a)
            specular_color += (light.color * cos_spec * intersect_obj.finishing.ks * attenu) 
    
    reflect_color = Vector3(0, 0, 0)
    transmission_color = Vector3(0, 0, 0)

    if depth > 0:
        reflect_dir = reflectionDirection(dis, normal)
        reflect_color += (ray_tracer(lights, objects, intersection_point, reflect_dir, depth - 1, intersect_obj) * intersect_obj.finishing.kr)

        if intersect_obj.finishing.ior < sys.float_info.epsilon:
            refr_rate = 1
        else:    
            refr_rate = 1 / intersect_obj.finishing.ior

        if is_inside:
            refr_rate = intersect_obj.finishing.ior
        
        transm, trans_dir =  transmissionDirection(refr_rate, dis, normal)

        if transm:
            transmission_color += (ray_tracer(lights, objects, intersection_point, trans_dir, depth - 1, intersect_obj) * intersect_obj.finishing.kt)

    final_color = intersect_color * (ambient_color + diffuse_color) + reflect_color + transmission_color + specular_color

    if final_color[0] > 1:
        final_color[0] = 1
    if final_color[1] > 1:
        final_color[1] = 1
    if final_color[2] > 1:
        final_color[2] = 1

    return final_color


