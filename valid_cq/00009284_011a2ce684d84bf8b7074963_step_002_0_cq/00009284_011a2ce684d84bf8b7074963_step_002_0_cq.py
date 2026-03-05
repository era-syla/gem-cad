import cadquery as cq

# -- Parameters --
# All dimensions are estimated based on visual proportions
length = 100.0      # Total length of the extrusion
base_width = 20.0   # Width of the main block
base_height = 15.0  # Height of the main block
wall_thick = 5.0    # Thickness of the vertical wall
wall_height = 25.0  # Total height of the vertical wall from bottom
lip_width = 5.0     # Width of the small lip at the bottom right
lip_height = 2.0    # Thickness of the bottom right lip
top_rib_width = 2.0 # Width of the small rib on top of the wall
top_rib_height = 2.0 # Height of the small rib

# -- Modeling --

# We will define the cross-section profile on the YZ plane and extrude it along X.
# Coordinates are relative to a local origin, let's say bottom-left corner of the main block.

# Points for the profile
# Start at bottom-left corner (0,0)
pts = [
    (0, 0),                         # Bottom-left corner
    (base_width, 0),                # Bottom of main block, start of lip
    (base_width + lip_width, 0),    # End of bottom lip
    (base_width + lip_width, lip_height), # Top of bottom lip (right edge)
    (base_width, lip_height),       # Back to vertical wall face
    (base_width, wall_height),      # Top right corner of wall (before rib)
    (base_width - (wall_thick - top_rib_width)/2, wall_height), # Start of top rib
    (base_width - (wall_thick - top_rib_width)/2, wall_height + top_rib_height), # Top right of rib
    (base_width - (wall_thick + top_rib_width)/2, wall_height + top_rib_height), # Top left of rib
    (base_width - (wall_thick + top_rib_width)/2, wall_height), # Back down from rib
    (base_width - wall_thick, wall_height), # Top left of wall
    (base_width - wall_thick, base_height), # Intersection with base block top
    (0, base_height),               # Top-left of base block
    (0, 0)                          # Close the loop
]

# Create the profile and extrude
result = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(length)
)

# Center the object visually if needed, or leave it defined from origin
# result = result.translate((-length/2, -(base_width + lip_width)/2, 0))