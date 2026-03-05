import cadquery as cq

# --- Parameters ---
length = 300.0        # Total length of the linkage
width = 25.0          # Width of the linkage arm
height = 12.0         # Overall height (Z dimension)
wall_thickness = 2.5  # Thickness of the web and flanges
hole_diam = 6.0       # Diameter of the pivot holes
hole_spacing = 30.0   # Distance between the two holes at the near end

# --- Derived Dimensions ---
# The base shape is defined by a slot/stadium profile.
# slot2D length is the distance between the centers of the two end arcs.
c2c_length = length - width

# --- Modeling ---

# 1. Create the base solid block
# We start with a 2D stadium shape (slot) and extrude it to the full height.
# This creates a solid block with rounded ends.
base = (
    cq.Workplane("XY")
    .slot2D(c2c_length, width)
    .extrude(height)
)

# 2. Create the C-channel cutout
# We create a rectangular solid that represents the empty space inside the C-channel.
# This cuts through the length of the part, leaving the top/bottom flanges and the rear web.

# Calculate the dimensions of the void
cut_height = height - (2 * wall_thickness)  # Leave material for top and bottom flanges
cut_depth_y = width - wall_thickness        # Leave material for the web
cut_length = length + 20.0                  # Ensure cut goes fully through the rounded ends

# Calculate the position offset to align the cut correctly.
# We assume the web is located at the -Y side of the part.
# The base is centered at Y=0, spanning [-width/2, width/2].
# The web occupies [-width/2, -width/2 + wall_thickness].
# The cut should occupy [-width/2 + wall_thickness, width/2 + overhang].
# A rectangle of width 'cut_depth_y' centered at 0 spans [-cut_depth_y/2, cut_depth_y/2].
# We need to shift it so its min Y aligns with the inner web face.
# Shift = (Target Min Y) - (Current Min Y)
#       = (-width/2 + wall_thickness) - (-(width - wall_thickness)/2)
#       = wall_thickness / 2.0
y_offset = wall_thickness / 2.0
z_offset = wall_thickness  # Shift up to preserve the bottom flange

cutout = (
    cq.Workplane("XY")
    .rect(cut_length, cut_depth_y)
    .extrude(cut_height)
    .translate((0, y_offset, z_offset))
)

# Apply the cut to the base to form the channel
body = base.cut(cutout)

# 3. Add Holes
# We add holes through the flanges (Z-axis).
# Hole locations relative to the center of the part (X=0, Y=0).
# Far end hole (+X)
x_far = c2c_length / 2.0
# Near end holes (-X)
x_near_tip = -c2c_length / 2.0
x_near_inner = -c2c_length / 2.0 + hole_spacing

result = (
    body.faces(">Z").workplane()
    .pushPoints([(x_far, 0), (x_near_tip, 0), (x_near_inner, 0)])
    .hole(hole_diam)
)