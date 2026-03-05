import cadquery as cq

# Main plate dimensions
plate_length = 120
plate_width = 70
plate_height = 10

# Recessed rectangle dimensions
recess_length = 80
recess_width = 45
recess_depth = 2

# Corner hole parameters
hole_diameter = 8
hole_depth = plate_height
corner_offset_x = 15
corner_offset_y = 12

# Build the base plate
result = (
    cq.Workplane("XY")
    .box(plate_length, plate_width, plate_height)
)

# Add recessed rectangle on top face
result = (
    result
    .faces(">Z")
    .workplane()
    .rect(recess_length, recess_width)
    .cutBlind(recess_depth)
)

# Add corner mounting holes (counterbore style - simple through holes)
result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([
        (-plate_length/2 + corner_offset_x, -plate_width/2 + corner_offset_y),
        ( plate_length/2 - corner_offset_x, -plate_width/2 + corner_offset_y),
        (-plate_length/2 + corner_offset_x,  plate_width/2 - corner_offset_y),
        ( plate_length/2 - corner_offset_x,  plate_width/2 - corner_offset_y),
    ])
    .circle(hole_diameter / 2)
    .cutThruAll()
)

# Add small radius fillets to the recess edges
result = (
    result
    .faces(">Z")
    .edges("not %Line")
    .fillet(1.5)
)