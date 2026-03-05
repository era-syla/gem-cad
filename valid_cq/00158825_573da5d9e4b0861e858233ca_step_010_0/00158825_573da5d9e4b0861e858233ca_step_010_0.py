import cadquery as cq

# --- Parameters ---
# Overall dimensions
L_base = 200.0       # Length of the main horizontal beam
W_base = 50.0        # Width of the beam
H_base = 120.0       # Height of the legs (overall height of bottom section)
thickness = 3.0      # Material thickness

# Tower dimensions
L_tower = 50.0       # Length of the top tower section
H_tower = 70.0       # Height of the tower section above the base
leg_width = 8.0      # Width of the vertical support strips for the tower

# Hole dimensions
hole_diam = 6.0

# --- Construction ---

# 1. Base: Inverted U-channel
# Create the outer block
base_outer = cq.Workplane("XY").rect(L_base, W_base).extrude(-H_base)

# Create the inner cutout to form the U-shape (legs and top plate)
# We cut from the bottom upwards, stopping short of the top by 'thickness'
# The cut extends the full length to leave open ends
base_cutout = (
    cq.Workplane("XY")
    .workplane(offset=-H_base)
    .rect(L_base, W_base - 2 * thickness)
    .extrude(H_base - thickness)
)

base = base_outer.cut(base_cutout)

# Add holes to the base top surface
# Positioning two holes on the left side of the bracket
base = (
    base.faces(">Z")
    .workplane()
    .center(-L_base / 4, 0)
    .pushPoints([(0, 0), (-25, 0)])
    .hole(hole_diam)
)

# 2. Tower: Structure on the right side
# Calculated position to align flush with the right end
tower_x_pos = (L_base / 2) - (L_tower / 2)

# Start with a solid block for the tower
tower_block = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .center(tower_x_pos, 0)
    .box(L_tower, W_base, H_tower, centered=(True, True, False))
)

# Cut 1: Longitudinal cut (along X) to open the sides (Left/Right)
# This leaves the Front and Back walls
cut_sides = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .center(tower_x_pos, 0)
    .rect(L_tower + 10, W_base - 2 * thickness) # +10 to ensure clean cut through length
    .extrude(H_tower - thickness)
)

# Cut 2: Transverse cut (along Y) to open the centers of the Front/Back walls
# This leaves the four corner legs
cut_windows = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .center(tower_x_pos, 0)
    .rect(L_tower - 2 * leg_width, W_base + 10) # +10 to ensure clean cut through width
    .extrude(H_tower - thickness)
)

# Apply cuts to the tower block
tower = tower_block.cut(cut_sides).cut(cut_windows)

# Add hole to the center of the tower top plate
tower = (
    tower.faces(">Z")
    .workplane()
    .hole(hole_diam)
)

# 3. Final Assembly
result = base.union(tower)