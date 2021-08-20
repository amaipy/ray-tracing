from rayTracer import *

def print_values(camera, lights, pigments, finishings, objects, screen):
    print('camera')
    print('position : {0}'.format(camera.position))
    print('center : {0}'.format(camera.center))
    print('direction : {0}'.format(camera.direction))
    print('up : {0}'.format(camera.up))
    print('y_opening : {0}'.format(camera.y_opening))
    print('lights: {0}'.format(len(lights)))
    for light in lights:
        print('light')
        print('position : {0}'.format(light.position))
        print('color : {0}'.format(light.color))
        print('co_atenuation : {0}'.format(light.co_atenuation))
        print('pos_atenuation : {0}'.format(light.pos_atenuation))
        print('co_square_pos : {0}'.format(light.co_square_pos))
    print('pigments: {0}'.format(len(pigments)))
    for pigment in pigments:
        print('pigment')
        print('type: {0}'.format(pigment.__class__.__name__))
        if isinstance(pigment, Pigment.Solid):
            print('color: {0}'.format(pigment.color))
        elif isinstance(pigment, Pigment.Checker):
            print('f_color: {0}'.format(pigment.f_color))
            print('s_color: {0}'.format(pigment.s_color))
            print('side: {0}'.format(pigment.side))
        else:
            print('tex_path: {0}'.format(pigment.tex_path))
            print('p0: {0}'.format(pigment.p0))
            print('p1: {0}'.format(pigment.p1))
    print('finishings: {0}'.format(len(finishings)))
    for finishing in finishings:
        print('finishing')
        print('ka: {0}'.format(finishing.ka))
        print('kd: {0}'.format(finishing.kd))
        print('ks: {0}'.format(finishing.ks))
        print('a: {0}'.format(finishing.a))
        print('kr: {0}'.format(finishing.kr))
        print('kt: {0}'.format(finishing.kt))
        print('ior: {0}'.format(finishing.ior))
    print('objects: {0}'.format(len(objects)))
    for object_ in objects:
        print('object')
        print('pigment: {0}'.format(object_.pigment))
        print('finishing: {0}'.format(object_.finishing))
        print('type: {0}'.format(object_.tp.__class__.__name__))
        if isinstance(object_.tp, Sphere):
            print('center: {0}'.format(object_.tp.center))
            print('radius: {0}'.format(object_.tp.radius))
        else:
            print('num_faces: {0}'.format(object_.tp.num_faces))
            print('faces_arr: {0}'.format(object_.tp.faces_arr))
    print('screen')
    print('width : {0}'.format(screen.width))
    print('height : {0}'.format(screen.height))
    print('r_dir : {0}'.format(screen.r_dir))
    print('b_dir : {0}'.format(screen.b_dir))
    print('top_left : {0}'.format(screen.top_left))
    print('pixel_w : {0}'.format(screen.pixel_w))
    print('pixel_h : {0}'.format(screen.pixel_h))

def write_scene(camera, lights, objects, screen, output, width, height):
    with open(output, 'w') as writer:
        writer.write("P3\n")
        writer.write("{0} {1}\n".format(width, height))
        writer.write("255\n")

        pixel_r = screen.pixel_w * screen.r_dir
        pixel_b = screen.pixel_h * screen.b_dir

        for h in range(height):
            for w in range(width):
                pos = Vector3(screen.top_left[0], screen.top_left[1], screen.top_left[2])
                pos += w * pixel_r
                pos += h * pixel_b
                dis = normalize(pos - camera.position)
                p = ray_tracer(lights, objects, camera.position, dis, MAX_DEPTH)
                writer.write("{0} {1} {2}\n".format(int(p[0] * 255), int(p[1] * 255), int(p[2] * 255)))

def main():
    width = 800
    height = 600
    if len(sys.argv) < 3:
        print('Uso: main.py input.in output.ppm')
        sys.exit()
    if len(sys.argv) > 3:
        width = int(sys.argv[3])
        if len(sys.argv) == 5:
            height = int(sys.argv[4])
    input_path = sys.argv[1]
    output_path = sys.argv[2]
    camera, lights,  pigments, finishings, objects, screen = return_scene_params(input_path, width, height)
    #print_values(camera, lights,  pigments, finishings, objects, screen)
    write_scene(camera, lights, objects, screen, output_path, width, height)
    
if __name__== "__main__":
    main()