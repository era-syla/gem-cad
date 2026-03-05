import cadquery as cq

# --- Parameter Definitions ---
# Overall dimensions
L_base = 100.0
W_base = 40.0
H_base = 8.0

# Top block dimensions
W_top = 25.0
H_top = 22.0
L_top = L_base
R_fillet = 5.0

# Cutout feature dimensions
notch_spacing = 32.0       # Distance between centers of the two side notches
notch_radius = 4.0         # Radius of the vertical cylindrical notches
belly_radius = 22.0        # Radius of the large central curve
belly_depth = 2.5          # Depth of the central curve cut relative to the front face

# --- Geometry Construction ---

# 1. Create the Base Plate
# Centered at X=0, Y=0. Z ranges from 0 to H_base
base = cq.Workplane("XY").box(L_base, W_base, H_base, centered=(True, True, False))

# 2. Create the Top Block
# Align the back edge of the top block with the back edge of the base.
# Base Y range: -20 to +20 (for width 40). Back edge is at Y = +20.
# Top block width is 25. Back edge at +20 means front edge is at -5.
# Center Y of top block = 20 - (25/2) = 7.5.
y_top_center = (W_base / 2) - (W_top / 2)

top_block = (
    cq.Workplane("XY")
    .workplane(offset=H_base)
    .center(0, y_top_center)
    .box(L_top, W_top, H_top, centered=(True, True, False))
)

# Apply fillets to the vertical edges of the top block
top_block = top_block.edges("|Z").fillet(R_fillet)

# 3. Create Cutters for the front face features
# Front face location Y coordinate
y_front_face = (W_base / 2) - W_top

# Define workplane for cutters starting at the top of the base
cutter_wp = cq.Workplane("XY").workplane(offset=H_base)

# Left Notch Cutter (Cylinder)
cutter_left = (
    cutter_wp
    .center(-notch_spacing / 2, y_front_face)
    .circle(notch_radius)
    .extrude(H_top)
)

# Right Notch Cutter (Cylinder)
cutter_right = (
    cq.Workplane("XY")
    .workplane(offset=H_base)
    .center(notch_spacing / 2, y_front_face)
    .circle(notch_radius)
    .extrude(H_top)
)

# Central "Belly" Cutter (Large Cylinder)
# Calculates position to achieve desired cut depth at the center
# We want the cylinder to penetrate the block by `belly_depth` at X=0.
# The cylinder is positioned in front of the face (negative Y relative to face).
y_belly_center = (y_front_face + belly_depth) - belly_radius

cutter_belly = (
    cq.Workplane("XY")
    .workplane(offset=H_base)
    .center(0, y_belly_center)
    .circle(belly_radius)
    .extrude(H_top)
)

# Combine all cutters into a single object
cutters = cutter_left.union(cutter_right).union(cutter_belly)

# 4. Subtract cutters from the top block
top_block_cut = top_block.cut(cutters)

# 5. Union the base and the modified top block
result = base.union(top_block_cut)