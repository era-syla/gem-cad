import cadquery as cq

# Parametric dimensions
shaft_radius = 5.0
shaft_length = 50.0

# The head is composed of a conical section and a top cylinder
# Dimensions for the conical flange part
cone_base_radius = 8.0  # The widest part of the flange
cone_top_radius = 5.0   # Matches the top cylinder
cone_height = 5.0

# Dimensions for the top cylindrical cap
top_cap_radius = 5.0
top_cap_height = 4.0

# Chamfer for the very top edge
top_chamfer = 0.5

# Create the main shaft
shaft = cq.Workplane("XY").circle(shaft_radius).extrude(shaft_length)

# Create the conical flange on top of the shaft
# The shaft was extruded upwards, so we work on the top face
cone = (
    shaft.faces(">Z")
    .workplane()
    .circle(cone_base_radius)
    .workplane(offset=cone_height)
    .circle(cone_top_radius)
    .loft(combine=True)
)

# Create the top cylindrical cap on top of the cone
top_cap = (
    cone.faces(">Z")
    .workplane()
    .circle(top_cap_radius)
    .extrude(top_cap_height)
)

# Apply a chamfer to the top edge of the cap
result = top_cap.faces(">Z").edges().chamfer(top_chamfer)

# Ensure the 'result' variable is set as requested
if 'show_object' in globals():
    show_object(result)