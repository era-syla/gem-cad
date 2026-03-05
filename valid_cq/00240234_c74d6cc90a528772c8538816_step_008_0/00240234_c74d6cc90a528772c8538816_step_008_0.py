import cadquery as cq

# Parameters for the frame geometry
length = 80.0          # Outer length
width = 40.0           # Outer width
height = 5.0           # Total height
rim_thickness = 1.5    # Thickness of the top outer edge wall
ledge_width = 3.0      # Width of the inner recessed step/ledge
step_depth = 1.5       # Depth of the recess from the top surface

# 1. Create the base block
# We start with a solid block representing the outer bounds
result = cq.Workplane("XY").box(length, width, height)

# 2. Cut the Recess (Rabbet)
# This removes material from the top to create the inner ledge
# The cut dimensions are the outer dimensions minus twice the rim thickness
recess_length = length - 2 * rim_thickness
recess_width = width - 2 * rim_thickness

result = (
    result.faces(">Z")
    .workplane()
    .rect(recess_length, recess_width)
    .cutBlind(-step_depth)
)

# 3. Cut the Through Hole
# This removes the center material completely
# The hole dimensions are reduced further by the ledge width
hole_length = recess_length - 2 * ledge_width
hole_width = recess_width - 2 * ledge_width

result = (
    result.faces(">Z")
    .workplane()
    .rect(hole_length, hole_width)
    .cutThruAll()
)