import cadquery as cq

# Main block dimensions
block_length = 80
block_width = 50
block_height = 20

# Create main rectangular block
result = cq.Workplane("XY").box(block_length, block_width, block_height)

# Create the central slot/cutout (rounded rectangle)
slot_length = 50
slot_width = 25
slot_depth = block_height  # full depth cutout

# Cut the central slot through the top
result = (result
    .faces(">Z")
    .workplane()
    .slot2D(slot_length, slot_width, angle=0)
    .cutThruAll()
)

# Add corner mounting holes
hole_diameter = 5
hole_inset_x = block_length / 2 - 10
hole_inset_y = block_width / 2 - 10

result = (result
    .faces(">Z")
    .workplane()
    .pushPoints([
        (hole_inset_x, hole_inset_y),
        (hole_inset_x, -hole_inset_y),
        (-hole_inset_x, hole_inset_y),
        (-hole_inset_x, -hole_inset_y),
    ])
    .hole(hole_diameter)
)

# Add the side cylinder/boss on the left side
cyl_radius = 6
cyl_length = 12
cyl_hole_radius = 2

# Position the cylinder on the left face, centered vertically
side_cylinder = (cq.Workplane("XY")
    .transformed(offset=cq.Vector(-block_length/2 - cyl_length/2, -8, 0))
    .workplane(origin=(0, 0, 0))
)

# Create the side protrusion
result = (result
    .faces("<X")
    .workplane(origin=(0, 0, 0))
    .center(0, -block_height/2 + block_height/2)  # center on face
    .pushPoints([(-8, 0)])
    .circle(cyl_radius)
    .extrude(cyl_length)
)

# Add hole through the cylinder
result = (result
    .faces("<X")
    .workplane()
    .pushPoints([(-8, 0)])
    .hole(cyl_hole_radius * 2)
)