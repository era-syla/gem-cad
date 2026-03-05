import cadquery as cq

# --- Parameter Definitions ---
# Main Table Dimensions
table_length = 200.0
table_width = 100.0
table_thickness = 5.0

# Leg Dimensions
leg_height = 40.0  # Height of legs below the table
leg_size = 5.0     # Square profile side length

# Hexagon Hole Parameters
hex_radius = 12.0  # Radius of the circumscribed circle for the hexagon
hex_offset_x = -50.0 # Distance from center along the X axis

# Side Cutout Parameters
cutout_width = 10.0
cutout_depth = 2.0 # How far into the side it cuts

# --- Geometry Construction ---

# 1. Create the main tabletop
# We center it on XY plane for easier symmetric operations
tabletop = cq.Workplane("XY").box(table_length, table_width, table_thickness)

# 2. Create the legs
# We'll define a single leg sketch and extrude it, then translate/mirror or locate them
# Locating at vertices is a robust way to handle this.

# Let's find the bottom face of the table to attach legs
bottom_face = tabletop.faces("<Z")

# Calculate leg positions relative to center
leg_x_offset = (table_length / 2) - (leg_size / 2)
leg_y_offset = (table_width / 2) - (leg_size / 2)

legs = (
    bottom_face
    .rect(table_length - leg_size, table_width - leg_size, forConstruction=True) # Construction rect to find corners
    .vertices() # Select the 4 corners of that rect
    .rect(leg_size, leg_size) # Draw square profile at each corner
    .extrude(leg_height) # Extrude downwards
)

# 3. Cut the hexagonal hole
# Select top face, move to position, draw polygon, cut
with_hex_hole = (
    legs.faces(">Z")
    .workplane()
    .center(hex_offset_x, 0)
    .polygon(6, hex_radius * 2) # CadQuery polygon takes diameter (width across corners usually)
    .cutThruAll()
)

# 4. Cut the small notch on the side
# Looking at the image, there is a small semi-circular or rectangular cutout on the long edge.
# It looks like a small rectangular notch or a wire passthrough.
with_side_notch = (
    with_hex_hole
    .faces(">Y") # Select the "back" face (or front depending on view)
    .workplane()
    .center(0, -table_thickness / 2) # Center horizontally, align with bottom edge of top plate
    .rect(cutout_width, cutout_depth * 2) # Make rect tall enough to cut through the edge
    .cutThruAll()
)

# Combine into final result
result = with_side_notch