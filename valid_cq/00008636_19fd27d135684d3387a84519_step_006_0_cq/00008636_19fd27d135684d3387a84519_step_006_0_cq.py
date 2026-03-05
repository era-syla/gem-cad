import cadquery as cq

# Parametric dimensions
shank_diameter = 2.0
shank_length = 20.0
head_diameter = 4.0
head_thickness = 1.5
point_length = 2.5

# Derived dimensions
shank_radius = shank_diameter / 2.0
head_radius = head_diameter / 2.0

# Create the head (cylinder)
# Centered at origin for easier alignment, but we'll extrude it upwards or downwards.
# Let's build it stacking along the Z axis.
head = cq.Workplane("XY").circle(head_radius).extrude(head_thickness)

# Create the shank (cylinder)
# Extrude from the bottom of the head
shank = (
    head.faces("<Z")
    .workplane()
    .circle(shank_radius)
    .extrude(shank_length)
)

# Create the point (cone)
# Extrude/loft from the end of the shank to a point
# We select the face at the very end of the current geometry (the end of the shank)
point = (
    shank.faces("<Z")
    .workplane()
    .circle(shank_radius)  # Base of the cone matches shank
    .workplane(offset=point_length)
    .circle(0.0001)        # Tip of the cone (effectively a point)
    .loft()
)

# Combine all parts into the final result
result = point