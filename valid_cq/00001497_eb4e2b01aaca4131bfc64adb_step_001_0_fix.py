import cadquery as cq

# Dimensions based on image analysis
total_length = 120
total_width = 20
thick_section_length = 35
thick_height = 8
thin_height = 3

# Create the thin long arm portion
thin_arm = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .rect(total_length, total_width)
    .extrude(thin_height)
)

# Create the thick section at the left end
thick_block = (
    cq.Workplane("XY")
    .moveTo(-total_length/2 + thick_section_length/2, 0)
    .rect(thick_section_length, total_width)
    .extrude(thick_height)
)

# Combine
result = thin_arm.union(thick_block)

# Add a step/ledge on the thick section - small raised portion on right side of thick block
ledge = (
    cq.Workplane("XY")
    .moveTo(-total_length/2 + thick_section_length + 5, 0)
    .rect(8, total_width)
    .extrude(thin_height + 2)
)
result = result.union(ledge)

# Cut the large hole in the thick section
hole_x = -total_length/2 + thick_section_length/2
result = (
    result
    .faces(">Z")
    .workplane()
    .center(hole_x, 0)
    .circle(7)
    .cutThruAll()
)

# Cut a slot/notch from the top of the thick section (the U-shaped cutout visible)
notch = (
    cq.Workplane("XY")
    .workplane(offset=thin_height)
    .moveTo(hole_x + 8, 0)
    .rect(10, 10)
    .extrude(thick_height - thin_height)
)
result = result.cut(notch)

# Cut two small holes in the thin arm section
hole1_x = total_length/2 - 25
hole2_x = total_length/2 - 45

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([(hole1_x, 0), (hole2_x, 0)])
    .circle(3)
    .cutThruAll()
)

# Apply chamfer to the far end of the thin arm
result = (
    result
    .faces(">Z")
    .edges(">X")
    .chamfer(1.5)
)