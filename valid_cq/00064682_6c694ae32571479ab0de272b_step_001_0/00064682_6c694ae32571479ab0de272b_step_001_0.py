import cadquery as cq

# Parametric dimensions for the part geometry
plate_thickness = 2.0
height = 80.0
width = 80.0

# Define coordinate values based on the visual proportions
# Placing the geometry roughly centered around the origin
x_right = 40.0
y_top = 40.0
y_bottom_right = -10.0  # The vertical edge doesn't go all the way down
x_top_flat_end = -10.0  # End of the top horizontal segment
x_chamfer_end = -25.0   # End of the corner cut
y_chamfer_end = 30.0
x_bottom_left = -30.0
y_bottom_left = -30.0

# Arc intermediate point to control curvature (bulge)
x_arc_mid = -36.0
y_arc_mid = 0.0

# Create the 3D model
result = (
    cq.Workplane("XY")
    .moveTo(x_right, y_bottom_right)       # Start at Bottom Right
    .lineTo(x_right, y_top)                # Vertical Right Edge
    .lineTo(x_top_flat_end, y_top)         # Horizontal Top Edge
    .lineTo(x_chamfer_end, y_chamfer_end)  # Top-Left Chamfer
    .threePointArc((x_arc_mid, y_arc_mid), (x_bottom_left, y_bottom_left)) # Left Curved Edge
    .close()                               # Angled Bottom Edge (closes the loop)
    .extrude(plate_thickness)
)