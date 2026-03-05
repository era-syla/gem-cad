import cadquery as cq

# Main flange disk
outer_radius = 50
outer_thickness = 8
hub_radius = 8
hub_height = 3
center_hole_radius = 4

# Create the main disk (flange)
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(outer_thickness)
)

# Add hub/boss in the center (slightly raised)
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(hub_radius)
    .extrude(hub_height)
)

# Cut center hole through everything
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(center_hole_radius)
    .cutThruAll()
)

# Add groove rings on top face of main disk
# Two concentric grooves near the outer edge
groove_depth = 1.5
groove_width = 1.5

result = (
    result
    .faces(">Z")
    .workplane()
    .circle(outer_radius - 6)
    .circle(outer_radius - 6 - groove_width)
    .cutBlind(-groove_depth)
)

result = (
    result
    .faces(">Z")
    .workplane()
    .circle(outer_radius - 10)
    .circle(outer_radius - 10 - groove_width)
    .cutBlind(-groove_depth)
)

# Add bolt holes in a circular pattern on the flange
bolt_hole_radius = 2.5
bolt_circle_radius = outer_radius - 9
num_bolts = 8

result = (
    result
    .faces(">Z")
    .workplane()
    .polarArray(bolt_circle_radius, 0, 360, num_bolts)
    .circle(bolt_hole_radius)
    .cutThruAll()
)