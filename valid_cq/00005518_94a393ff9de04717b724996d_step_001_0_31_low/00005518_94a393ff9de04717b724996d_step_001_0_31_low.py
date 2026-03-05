import cadquery as cq

# Parameters
outer_width = 100.0
outer_height = 60.0
thickness = 5.0
frame_width = 10.0
cylinder_radius = 8.0
cylinder_length = 15.0

# Calculate inner dimensions
inner_width = outer_width - 2 * frame_width
inner_height = outer_height - 2 * frame_width

# Create the rectangular frame
frame = (
    cq.Workplane("XY")
    .rect(outer_width, outer_height)
    .rect(inner_width, inner_height)
    .extrude(thickness)
)

# Add the cylinder at the bottom right corner
cylinder_x = outer_width / 2
cylinder_y = -outer_height / 2

result = (
    frame
    .faces(">Z").workplane()
    .center(cylinder_x, cylinder_y)
    .circle(cylinder_radius)
    .extrude(cylinder_length, both=True)
)

# The frame face '>Z' is at z=thickness, so extruding 'both=True' will center it there.
# Let's adjust to match the image where the cylinder passes through the corner.
result = (
    cq.Workplane("XY")
    .rect(outer_width, outer_height)
    .rect(inner_width, inner_height)
    .extrude(thickness)
)

cylinder = (
    cq.Workplane("XY")
    .center(cylinder_x, cylinder_y)
    .circle(cylinder_radius)
    .extrude(thickness + 5) # protrudes from the front
)

# Re-evaluating the cylinder position and extrusion based on the image
# The cylinder seems to be at the bottom right corner, centered on the vertex, protruding equally from both sides of the frame.
result = (
    cq.Workplane("XY")
    .rect(outer_width, outer_height)
    .rect(inner_width, inner_height)
    .extrude(thickness)
)

cylinder = (
    cq.Workplane("XY", origin=(cylinder_x, cylinder_y, thickness/2))
    .circle(cylinder_radius)
    .extrude(cylinder_length / 2, both=True)
)

result = result.union(cylinder)
