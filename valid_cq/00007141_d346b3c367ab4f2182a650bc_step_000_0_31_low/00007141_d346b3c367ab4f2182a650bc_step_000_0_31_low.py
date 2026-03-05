import cadquery as cq

# Parameters
base_length = 100.0
base_width = 40.0
base_height = 15.0

pin_radius = 3.0
pin_height = 10.0
pin_dist_x = 70.0
pin_dist_y = 25.0

cutout_length = 60.0
cutout_start_width = 2.0
cutout_end_width = 15.0
cutout_depth = 5.0
sphere_radius = 6.0

# Base block
result = cq.Workplane("XY").box(base_length, base_width, base_height)

# Pins
pins = (
    cq.Workplane("XY")
    .workplane(offset=base_height / 2)
    .pushPoints([(-pin_dist_x / 2, -pin_dist_y / 2), (pin_dist_x / 2, pin_dist_y / 2)])
    .cylinder(pin_height, pin_radius)
)

# Dome on pins
domes = (
    cq.Workplane("XY")
    .workplane(offset=base_height / 2 + pin_height / 2)
    .pushPoints([(-pin_dist_x / 2, -pin_dist_y / 2), (pin_dist_x / 2, pin_dist_y / 2)])
    .sphere(pin_radius)
)

result = result.union(pins).union(domes)

# Cutout shape
cutout_sketch = (
    cq.Sketch()
    .segment((-cutout_length/2, cutout_start_width/2), (cutout_length/2, cutout_end_width/2))
    .segment((cutout_length/2, -cutout_end_width/2))
    .segment((-cutout_length/2, -cutout_start_width/2))
    .close()
    .assemble()
)

cutout = (
    cq.Workplane("XY")
    .workplane(offset=base_height/2)
    .center(0, 0)
    .placeSketch(cutout_sketch)
    .extrude(-cutout_depth, combine=False)
)

result = result.cut(cutout)

# Spherical cutout at the end
sphere_cut = (
    cq.Workplane("XY")
    .workplane(offset=base_height/2)
    .center(cutout_length/2, 0)
    .sphere(sphere_radius)
)

result = result.cut(sphere_cut)

# Side cutout
side_cut = (
    cq.Workplane("XY")
    .workplane(offset=base_height/2)
    .center(cutout_length/2 - 10, base_width/2)
    .box(20, 10, cutout_depth*2, centered=(True, False, True))
)

result = result.cut(side_cut)
