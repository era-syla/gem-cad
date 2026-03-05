import cadquery as cq

# Parametric dimensions
width = 40.0         # Width of the rectangular section
length = 40.0        # Length from back edge to center of the arc
height = 30.0        # Thickness of the block
radius = 20.0        # Radius of the rounded end (half of total width usually)
hole_dia = 12.0      # Diameter of the through hole
c_bore_dia = 20.0    # Diameter of the counterbore
c_bore_depth = 10.0  # Depth of the counterbore

# The total length of the part is length + radius
# The total width is usually 2 * radius, but let's keep them somewhat independent for parametric flexibility, 
# assuming width = 2*radius for a perfect tangent fit.
if width != 2 * radius:
    # Adjust width to match the radius for a smooth rounded end if desired, 
    # or keep them separate if it's a specific design. 
    # For this specific "U-shape" or "tombstone" look, width usually equals 2*radius.
    width = 2 * radius

# Create the base shape
# We will draw on the XY plane.
# Strategy:
# 1. Draw a rectangle for the back part.
# 2. Add a circle (or arc) for the front part.
# 3. Extrude.
# Alternatively, using CadQuery's sketch features or primitives.

# Method: Construct a sketch with lines and an arc
result = (
    cq.Workplane("XY")
    # Start at the back-left corner
    .moveTo(0, 0)
    .lineTo(length, 0)           # Line to the center of the arc
    .threePointArc((length + radius, width/2), (length, width)) # Arc to the other side
    .lineTo(0, width)            # Line back to the back-left
    .close()                     # Close the shape
    .extrude(height)
)

# Add the counterbored hole
# The hole is concentric with the arc, which is centered at (length, width/2)
hole_center_x = length
hole_center_y = width / 2

result = (
    result
    .faces(">Z") # Select top face
    .workplane()
    .moveTo(hole_center_x, hole_center_y)
    .cboreHole(hole_dia, c_bore_dia, c_bore_depth)
)

# Optional: If the origin needs to be centered differently, moves can be applied.
# The current origin (0,0,0) is at the bottom-back-left corner.