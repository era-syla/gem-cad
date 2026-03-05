import cadquery as cq

# --- Parametric Dimensions ---
# Main body dimensions
main_width = 20.0     # X dimension
main_depth = 20.0     # Y dimension
main_height = 60.0    # Z dimension

# Bottom cylindrical post dimensions
post_diameter = 12.0
post_height = 10.0

# Top hole dimensions
hole_diameter = 10.0
hole_depth = 15.0  # Depth of the hole from top face

# --- Modeling ---

# 1. Create the main rectangular body
# Using a workplane on the XY plane and extruding up
main_body = (
    cq.Workplane("XY")
    .box(main_width, main_depth, main_height, centered=(True, True, False))
)

# 2. Add the cylindrical post at the bottom
# Select the bottom face (at Z=0), draw a circle, and extrude it downwards
# Note: Since the box starts at Z=0 and goes up, the bottom face is at Z=0.
# We extrude negative to go down.
result_with_post = (
    main_body.faces("<Z")
    .workplane()
    .circle(post_diameter / 2.0)
    .extrude(post_height)  # Workplane normal is pointing down, so positive extrusion adds material downward
)

# 3. Create the hole at the top
# Select the top face (at Z=main_height), draw a circle, and cut
result = (
    result_with_post.faces(">Z")
    .workplane()
    .circle(hole_diameter / 2.0)
    .cutBlind(-hole_depth)
)

# If running in an environment that supports show_object (like CQ-Editor), this will display it
# show_object(result)