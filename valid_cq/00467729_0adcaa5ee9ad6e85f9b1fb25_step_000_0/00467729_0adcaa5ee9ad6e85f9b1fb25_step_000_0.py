import cadquery as cq

# Parametric dimensions for the rectangular plate
length = 120.0   # Total length along the X-axis
height = 20.0    # Vertical height along the Z-axis
thickness = 2.0  # Thickness along the Y-axis

# Create the 3D model
# We use the XY workplane and create a box.
# The dimensions map to (x_length, y_length, z_length) in the box command.
# This orients the plate standing up on its edge, matching the isometric view.
result = cq.Workplane("XY").box(length, thickness, height)