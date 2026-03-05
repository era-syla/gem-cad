import cadquery as cq

# Parametric dimensions
# Top plate dimensions
top_length = 100.0  # Length of the top horizontal plate
top_width = 50.0    # Width of the top horizontal plate
top_thickness = 2.0 # Thickness of the top plate

# Vertical plate dimensions
vertical_height = 80.0  # Height of the vertical section
vertical_width = 40.0   # Width of the vertical section (along top_width direction)
vertical_thickness = 10.0 # Thickness of the vertical section (along top_length direction)

# Create the top plate
# We center it on the XY plane for easier alignment
top_plate = cq.Workplane("XY").box(top_length, top_width, top_thickness)

# Create the vertical plate
# We position it underneath the top plate.
# The top plate is centered at Z=0 and has thickness/2 up and down.
# Let's shift the whole top plate up by thickness/2 so its bottom face is at Z=0.
top_plate = top_plate.translate((0, 0, top_thickness / 2))

# Create vertical support
# It is centered in X and Y, and extends downwards from Z=0
vertical_plate = (
    cq.Workplane("XY")
    .rect(vertical_thickness, vertical_width)
    .extrude(-vertical_height)
)

# Combine the parts
# Since we want a single solid, we union them.
result = top_plate.union(vertical_plate)

# If you were running this in an interactive environment (like CQ-Editor),
# you would typically see 'show_object(result)'.
# The prompt asks for a variable 'result' containing the final geometry.