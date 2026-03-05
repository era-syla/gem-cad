import cadquery as cq

# Parametric dimensions
length = 100.0       # Total length of the beam
width = 15.0         # Width of the cross-section
height = 15.0        # Height of the cross-section
groove_depth = 3.5   # Depth of the concave cut on top and bottom

# Coordinates for the cross-section profile on the YZ plane
# The origin (0,0) is at the center of the cross-section
x_left = -width / 2.0
x_right = width / 2.0
y_top = height / 2.0
y_bot = -height / 2.0

# Midpoints for the concave arcs
# Top groove dips down, bottom groove dips up
y_top_mid = y_top - groove_depth
y_bot_mid = y_bot + groove_depth

# Generate the model
# We draw the profile on the YZ plane and extrude along the X axis
result = (
    cq.Workplane("YZ")
    .moveTo(x_left, y_top)                  # Start at Top-Left
    .threePointArc((0, y_top_mid), (x_right, y_top))  # Arc to Top-Right (concave)
    .lineTo(x_right, y_bot)                 # Line to Bottom-Right
    .threePointArc((0, y_bot_mid), (x_left, y_bot))   # Arc to Bottom-Left (concave)
    .close()                                # Close the shape (Line to Top-Left)
    .extrude(length)
)