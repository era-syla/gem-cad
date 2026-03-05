import cadquery as cq

# Geometric Parameters
length = 120.0       # Total length of the rail
width = 30.0         # Total width of the profile
height = 6.0         # Total height of the profile
groove_depth = 2.5   # Depth of the central concave channel
groove_radius = 12.0 # Radius of the cutting tool for the channel
fillet_radius = 2.5  # Radius for rounding the top edges

# 1. Create the base rectangular block
# The box is created centered at the origin (0,0,0)
# Z ranges from -height/2 to +height/2
base = cq.Workplane("XY").box(length, width, height)

# 2. Setup the cutting tool for the central groove
# Calculate the position of the cylinder to achieve the desired depth
top_z = height / 2.0
# The bottom of the groove is at (top_z - groove_depth)
# The center of the cylinder must be one radius above that point
cutter_center_z = (top_z - groove_depth) + groove_radius

# Create the cylindrical cutter
# We draw on the YZ plane to create a profile perpendicular to the length (X)
# Then extrude along X to create the cutting rod
cutter = (
    cq.Workplane("YZ")
    .moveTo(0, cutter_center_z)
    .circle(groove_radius)
    .extrude(length * 2, both=True) # Extrude symmetrically to ensure it covers the base
)

# 3. Perform the boolean cut and fillet operations
result = (
    base
    .cut(cutter)                 # Subtract the cylinder from the base
    .edges("|X")                 # Select all edges parallel to the length (X-axis)
    .edges(">Z")                 # Filter to keep only the top-most edges (should contain 4 edges)
    .fillet(fillet_radius)       # Round the shoulders and the groove transition
)