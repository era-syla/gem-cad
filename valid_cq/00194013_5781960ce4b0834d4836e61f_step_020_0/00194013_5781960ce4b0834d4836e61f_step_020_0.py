import cadquery as cq

# Parametric dimensions for the part
length = 80.0            # Total length of the block (X-axis)
width = 30.0             # Total width of the block (Y-axis)
height = 25.0            # Total height of the block (Z-axis)
hole_spacing = 50.0      # Distance between hole centers
hole_diameter = 8.0      # Diameter of the through holes
cutout_width = 24.0      # Width of the flat inner section of the cutout
cutout_depth = 8.0       # Depth of the cutout from the front face
chamfer_x = 6.0          # Horizontal length of the angled transition

# Calculate coordinates for the 2D profile
# Origin is at the center of the block's bounding box in X and Y
x_max = length / 2.0
y_max = width / 2.0
y_min = -width / 2.0
x_chamfer_start = (cutout_width / 2.0) + chamfer_x
y_recess = y_min + cutout_depth

# Define points for the base profile (Top View)
# Starting from back-left corner and moving counter-clockwise
pts = [
    (-x_max, y_max),                 # Back Left
    (-x_max, y_min),                 # Front Left
    (-x_chamfer_start, y_min),       # Start of left chamfer
    (-cutout_width/2.0, y_recess),   # Bottom of left chamfer (recess start)
    (cutout_width/2.0, y_recess),    # Bottom of right chamfer (recess end)
    (x_chamfer_start, y_min),        # End of right chamfer
    (x_max, y_min),                  # Front Right
    (x_max, y_max)                   # Back Right
]

# Create the 3D model
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(height)
    .faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing / 2.0, 0), (hole_spacing / 2.0, 0)])
    .hole(hole_diameter)
)