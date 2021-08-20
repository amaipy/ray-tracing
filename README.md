# ray-tracing

Simple Ray Tracing algorithm implemented with Python 3.8.

It was made as an assignment for the Computer Graphics course at UFMG in the first term of 2020 (01/2020).

## Instructions 

* It is required to have Python 3.8 (or later) installed. Additionally, the packages `vectormath` and `numpy` are required (just run on terminal `pip install package_name`). 

* To use, run on terminal:

 `python main.py input.in output.ppm`

* It is possible to input the width and height of the picture, for example: 

 `python main.py input.in output.ppm 100 100`
 
 will output a ppm file with 100x100px
 
## Implementation

From a descriptive input file `input.in`, the algorithm outputs a rendered `out.ppm` file. 

Depending on the input, it can take hours to complete.

All example files were run, with the respective output numbered (test1.in generated out1.ppm).

All the basic requirements (as described below) were implemented.

### Input file

The description of the scene is made by a text file with 5 well-defined sections:

_(Translated from the assignment specifications)_

#### 1) Camera Description

The description of the camera that captures the scene described in the file is in the first 4 lines of the
file. The first 3 lines contain 3 floating point quantities each, which
correspond, respectively, to the coordinates of the central position of the camera (coordinates of the
eye), to the coordinates of the position the camera is facing (coordinates of the center of the
projection plane) and finally the coordinates of a third point, in the direction of which the normal
camera is pointing, thus describing the orientation of the camera. In the fourth line of the
file, we have a floating point quantity that represents the camera aperture in relation to
to the Y axis. This fourth parameter summarily describes the window visible in the projection plane.

#### 2) Description of Lights

The next line of the configuration file after the camera description should contain a
integer, greater than zero, representing how many lights are present in the scene.
Then, each of these lights is detailed, with one in each subsequent line. For each light,
the description will consist of 9 floating point quantities saying: the 3 coordinates of the light source,
the color of the light emitted by the source, in RGB format (with magnitude between 0 and 1) and 3 parameters of
attenuation of the respective light source, the first parameter being a constant coefficient of
attenuation, the second the attenuation proportional to the distance from the light source and finally the
attenuation coefficient proportional to the square of the distance from the light source. The first light source 
described in the file is ambient light, and its coordinates are present in the description.
merely to simplify the file format.

#### 3) Description of Pigments

After defining each of the light sources, the text file will contain a new line containing
a positive integer with a number of pigments present in the scene. These pigments
are in turn described, one in each subsequent line. The program must behave by the
minus 3 distinct types of pigments, which are determined by a string at the beginning of each
line: solid, checker and texmap. Solid pigment consists of a solid color, which is
specified by the RGB values (between 0 and 1). The checker pigment corresponds to a texture
procedural that produces a 3d checkered pattern. For this pattern, 
two colors (also in RGB, between 0 and 1) and a corresponding seventh floating-point magnitude
to the length of the sides of the pattern's cube, are required. Finally, the textmap pigment corresponds to
a basic texture. As arguments for this pigment, in addition to the file containing the texture
itself, in ppm format, 8 floating point quantities are passed. To
transforming the coordinates of a 3D point to the 2D coordinates of the texture is used
linear combination, ie 4 floating point numbers are used to calculate each
texture coordinate. In other words, there are two 4-element vectors, P0 and P1 passed
as an argument for the texture and given a 3D point in homogeneous coordinates, PC, the color of the
PC point will be given by the color coordinate (s, r) in the texture where s = P0 . PC and r = P1 . PC.


#### 4) Description of Finishes

Then, the text file brings the description of the surface finishes existing in the scene,
following the same format: a line containing an integer with the number of finishes, and
each finish on a subsequent line. The description of each finish is quite simple and
consists of 7 floating point values: ka (ambient light coefficient), kd (coefficient
of diffused light), ks (specular light coefficient), α (exponent for specular reflection). These 4
first parameters have to do with the interaction properties of the surface with the
light sources, and are similar to the properties of the Phong model. The next 3
parameters are already related to the ray tracing algorithm itself:
kr, kt and ior. The first is the reflection coefficient (kr) and if it is greater than zero,
means that the surface reflects light and the reflected ray must be followed and the color obtained
added to the final color, weighted by the coefficient. kt is the transmission coefficient, and
at a value greater than zero, it means that the surface transmits light and the transmitted ray
must be followed and the obtained color added to the final color weighted by this coefficient. To
calculation of the transmitted radius uses Snell's law where the third parameter is needed,
which is the ratio between the refractive indices of the environment (n1) and the refractive index of the
material (n2), that is, ior = n1/n2.

#### 5) Description of Objects

Finally, the file contains a description of the surfaces that make up the scene. Again the
format is the same: an integer containing the number of surfaces present in the scene, described
one on each subsequent line. The description of each surface consists of an integer with
reference to the surface pigment, followed by another integer with reference to the finish
her. Then, the type of surface is described, which can be of two types: spheres and polyhedra
convex. Spheres are described by the string “sphere” followed by 4 floating point numbers,
that is, the coordinates (x, y, z) of the center of the sphere, and the radius. Convex polyhedra are
described by the string "polyhedron", followed by an integer for the number of faces of the polyhedron, and the
then, each face on a new line, the coefficients of the equation of the plane that contains the face. The
convex polyhedron would be defined by the intersection of the semi-spaces defined by the planes of the
faces. 
