import cadquery as cq

# --- Parametric Dimensions (Standard 2020 Profile) ---
length = 300.0          # Total length of the extrusion
width = 20.0            # Profile width/height (20mm)
fillet_radius = 1.0     # Radius of the outer corners
center_hole_dia = 5.0   # Diameter of the central hole (tap size for M5/M6)
slot_opening = 6.0      # Width of the T-slot opening
slot_inner_w = 10.0     # Width of the inner T-slot cavity
slot_depth = 6.0        # Depth of the slot from the face
lip_thickness = 1.5     # Thickness of the retaining lip

# --- Modeling ---

# 1. Create the base solid block
# We create a box centered on X and Y, extending from Z=0 to Z=length
base = cq.Workplane("XY").box(width, width, length, centered=(True, True, False))

# 2. Add fillets to the outer corners
# Select vertical edges (parallel to Z)
result = base.edges("|Z").fillet(fillet_radius)

# 3. Create and subtract the central hole
center_hole = (
    cq.Workplane("XY")
    .circle(center_hole_dia / 2.0)
    .extrude(length)
)
result = result.cut(center_hole)

# 4. Create the T-Slot Cutter geometry
# We define the cross-section of one slot and extrude it.
# Coordinates are calculated relative to the center (0,0).
# The profile is defined for the "Top" face (Y+) and will be rotated.

y_face = width / 2.0
y_lip_end = y_face - lip_thickness
y_bottom = y_face - slot_depth
x_neck = slot_opening / 2.0
x_inner = slot_inner_w / 2.0

# Points for the T-slot polygon
# Note: y_face + 0.1 extends the cut slightly outside the block to ensure a clean surface cut
cutter_profile_pts = [
    (x_neck, y_face + 0.1),    # Start at opening edge
    (x_neck, y_lip_end),       # Down neck depth
    (x_inner, y_lip_end),      # Out to inner width
    (x_inner, y_bottom),       # Down to bottom of slot
    (-x_inner, y_bottom),      # Across bottom
    (-x_inner, y_lip_end),     # Up to lip
    (-x_neck, y_lip_end),      # In to neck width
    (-x_neck, y_face + 0.1)    # Back out to surface
]

# Create the cutter solid object
slot_cutter = (
    cq.Workplane("XY")
    .polyline(cutter_profile_pts)
    .close()
    .extrude(length)
)

# 5. Apply the cuts to all four faces
for i in range(4):
    angle = 90.0 * i
    # Rotate the cutter around the Z-axis (0,0,1) at the origin (0,0,0)
    rotated_cutter = slot_cutter.rotate((0, 0, 0), (0, 0, 1), angle)
    result = result.cut(rotated_cutter)

# The variable 'result' now contains the final 3D geometry