import cadquery as cq

# Parameters
flange_width = 40
flange_height = 30
flange_thickness = 4
corner_radius = 6

tube_outer_radius = 10
tube_inner_radius = 5
tube_length = 25

hole_radius = 3
hole_offset_x = 14
hole_offset_y = 10

# Create the flange plate (rounded rectangle)
flange = (
    cq.Workplane("YZ")
    .rect(flange_width, flange_height)
    .extrude(flange_thickness)
)

# Round the corners of the flange
flange = (
    flange
    .edges("|X")
    .fillet(corner_radius)
)

# Create the tube/cylinder extending from the flange
tube = (
    cq.Workplane("YZ")
    .circle(tube_outer_radius)
    .extrude(tube_length)
)

# Combine flange and tube
result = flange.union(tube)

# Add a fillet at the junction between tube and flange
# First, let's add a boss/fillet transition
transition = (
    cq.Workplane("YZ")
    .circle(tube_outer_radius + 2)
    .extrude(2)
)

result = result.union(transition)

# Hollow out the tube (through hole)
result = (
    result
    .faces("<X")
    .workplane()
    .circle(tube_inner_radius)
    .cutThruAll()
)

# Add mounting holes in the flange corners
result = (
    result
    .faces(">X")
    .workplane()
    .pushPoints([
        (hole_offset_y, hole_offset_x),
        (-hole_offset_y, hole_offset_x),
        (hole_offset_y, -hole_offset_x),
        (-hole_offset_y, -hole_offset_x),
    ])
    .circle(hole_radius)
    .cutThruAll()
)