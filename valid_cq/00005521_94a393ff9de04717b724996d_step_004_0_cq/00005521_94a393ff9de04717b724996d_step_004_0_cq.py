import cadquery as cq

# Parametric dimensions
block_length = 40.0
block_width = 30.0
block_height = 15.0
cylinder_radius = 4.0
cylinder_length = 5.0  # Length of protrusion from the face

# Create the main rectangular body
# Centered on the XY plane for symmetry
main_body = cq.Workplane("XY").box(block_length, block_width, block_height)

# Create the first cylinder on the right face (+X)
# We select the face with the maximum X coordinate
right_cylinder = (
    main_body.faces(">X")
    .workplane()
    .circle(cylinder_radius)
    .extrude(cylinder_length)
)

# Create the second cylinder on the left face (-X)
# We use the result of the previous operation and select the face with minimum X
# Note: Since the previous extrude added geometry in +X, the minimum X face 
# is still the original left face of the box.
result = (
    right_cylinder.faces("<X")
    .workplane()
    .circle(cylinder_radius)
    .extrude(cylinder_length)
)

# Alternatively, a more robust way to select the original face without relying on history
# is to start a new workplane relative to the origin or combine objects.
# However, the chaining method above is standard CadQuery practice.

# To strictly match the visual "split line" in the middle, it's just a visual artifact 
# of how the geometry might be constructed or rendered, but physically it's one solid.
# If a groove was needed, we would cut it. Assuming it's a solid block.