import cadquery as cq

# Main cube body
cube_size = 40

# Create the main cube
main_body = cq.Workplane("XY").box(cube_size, cube_size, cube_size)

# Create a notch/cutout on the lower left front area
# The notch appears to be on the lower-left corner of the front face
notch_size = 12
notch_depth = 8

# Cut a rectangular notch from the lower-left front corner
notch = (
    cq.Workplane("XY")
    .box(notch_size, notch_depth, notch_size)
    .translate((-cube_size/2 + notch_size/2, -cube_size/2 + notch_depth/2, -cube_size/2 + notch_size/2))
)

main_body = main_body.cut(notch)

# Create a ring/loop on the right side lower area
ring_center_x = cube_size/2 + 8
ring_center_y = 0
ring_center_z = -cube_size/2 + 8

ring_outer_r = 8
ring_inner_r = 5
ring_thickness = 4

# Create the ring by revolving or using torus-like approach
# Make a torus for the ring
ring = (
    cq.Workplane("XZ")
    .transformed(offset=cq.Vector(ring_center_x, ring_center_z, 0))
    .circle(ring_outer_r)
    .extrude(ring_thickness)
)

# Actually let's build a proper ring using difference of cylinders
ring_outer = (
    cq.Workplane("YZ")
    .transformed(offset=cq.Vector(0, ring_center_z, ring_center_x))
    .circle(ring_outer_r)
    .extrude(ring_thickness)
)

ring_inner = (
    cq.Workplane("YZ")
    .transformed(offset=cq.Vector(0, ring_center_z, ring_center_x))
    .circle(ring_inner_r)
    .extrude(ring_thickness + 2)
    .translate((0, 0, -1))
)

ring_solid = ring_outer.cut(ring_inner)

# Create a small connector/stem from the cube to the ring
stem = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(cube_size/2 + ring_thickness/2, 0, ring_center_z))
    .box(ring_thickness, ring_thickness * 0.8, ring_thickness * 0.8)
)

# Combine everything
result = main_body.union(ring_solid).union(stem)