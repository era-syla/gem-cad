import cadquery as cq

# ==========================================
# Parameters
# ==========================================
length = 200.0        # Total length of the part along the X axis
width = 40.0          # Width of the top flange
height = 20.0         # Height of the vertical lip/flange
thickness = 3.0       # Material thickness
cut_offset = 40.0     # Longitudinal distance for the angle cut (miter)
hole_diam = 12.0      # Diameter of the mounting holes
hole_spacing = 30.0   # Center-to-center distance between holes

# ==========================================
# Modeling
# ==========================================

# 1. Create the base L-profile extrusion
# We define the cross-section on the YZ plane.
# The origin (0,0,0) is placed at the top-left outer corner.
# - Y axis corresponds to the top flange width.
# - Z axis corresponds to the vertical flange height (downwards).
result = (
    cq.Workplane("YZ")
    .polyline([
        (0, 0),                       # Outer corner
        (width, 0),                   # End of top flange
        (width, -thickness),          # Top flange thickness
        (thickness, -thickness),      # Inner corner
        (thickness, -height),         # Bottom of vertical flange (inner)
        (0, -height),                 # Bottom of vertical flange (outer)
        (0, 0)                        # Close the loop
    ])
    .close()
    .extrude(length)
)

# 2. Apply angled cuts to the ends
# The part is cut to form a trapezoidal shape on the top face.
# The 'front' edge (with the vertical lip, Y=0) is the long base.
# The 'back' edge (Y=width) is the short base.

# Cut the left end
result = (
    result.faces(">Z")                # Select the top face (Z=0)
    .workplane()
    .polyline([
        (0, 0),                       # Front-left tip (preserved)
        (0, width),                   # Back-left corner (removed)
        (cut_offset, width)           # Point on back edge
    ])
    .close()
    .cutThruAll()                     # Cut through the entire solid
)

# Cut the right end
result = (
    result.faces(">Z")
    .workplane()
    .polyline([
        (length, 0),                  # Front-right tip (preserved)
        (length, width),              # Back-right corner (removed)
        (length - cut_offset, width)  # Point on back edge
    ])
    .close()
    .cutThruAll()
)

# 3. Create the mounting holes
# Holes are centered on the top flange face and spaced symmetrically
center_x = length / 2.0
center_y = width / 2.0

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([
        (center_x - hole_spacing / 2.0, center_y),
        (center_x + hole_spacing / 2.0, center_y)
    ])
    .hole(hole_diam)
)