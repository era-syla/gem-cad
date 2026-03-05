import cadquery as cq

# Parametric dimensions
shank_radius = 5.0
shank_length = 25.0
head_bottom_radius = 10.0
head_top_radius = 5.0
head_height = 12.0

# Create the shank (cylinder)
shank = cq.Workplane("XY").circle(shank_radius).extrude(shank_length)

# Create the head (truncated cone) on top of the shank
# We create a new workplane on top of the shank
head = (
    shank.faces(">Z")
    .workplane()
    .circle(head_bottom_radius)
    .workplane(offset=head_height)
    .circle(head_top_radius)
    .loft(combine=True)
)

# Assign the final object to 'result'
result = head