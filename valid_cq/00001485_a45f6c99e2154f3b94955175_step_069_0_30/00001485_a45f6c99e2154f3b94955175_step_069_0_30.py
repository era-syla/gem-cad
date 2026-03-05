import cadquery as cq

# --- Parameters ---
# Main Body Dimensions
body_length = 18.0
body_width = 16.0
body_height = 12.0

# Clevis (Front Fork) Dimensions
clevis_straight_len = 8.0
clevis_gap = 7.0
ear_radius = body_height / 2.0
pin_diameter = 5.0
pin_boss_height = 2.0

# Tail (Back Connector) Dimensions
tail_stem_len = 8.0
tail_stem_width = 6.0
tail_tip_len = 2.5
tail_tip_width = 14.0  # Slightly narrower than body? Or similar. Using 14.

# Side Window Dimensions
window_width = 10.0
window_height = 7.0
window_depth = 1.5

# --- Modeling ---

# 1. Main Central Body
# Centered at origin for symmetry
main_body = cq.Workplane("XY").box(body_length, body_width, body_height)

# 2. Clevis (Front Section)
# Location: Attaches to the Front Face (X+) of the main body
# We construct the full solid first, then cut the gap.
# Pivot point X coordinate relative to origin
pivot_x = (body_length / 2.0) + clevis_straight_len

# Rectangular extension
clevis_base = (
    cq.Workplane("XY")
    .workplane(offset=body_length / 2.0)
    .center(0, 0)
    .box(clevis_straight_len, body_width, body_height, centered=(False, True, True))
)

# Rounded ends
clevis_ears = (
    cq.Workplane("XY")
    .moveTo(pivot_x, 0)
    .cylinder(body_height, ear_radius)
)

# 3. Tail (Back Section)
# Location: Attaches to the Back Face (X-)
# Stem
tail_stem = (
    cq.Workplane("XY")
    .workplane(offset=-body_length / 2.0)
    .center(0, 0)
    .box(tail_stem_len, tail_stem_width, body_height, centered=(False, True, True))
    .translate((-tail_stem_len, 0, 0)) # Move backwards
)

# T-Tip
tail_tip = (
    cq.Workplane("XY")
    .workplane(offset=-(body_length / 2.0 + tail_stem_len))
    .center(0, 0)
    .box(tail_tip_len, tail_tip_width, body_height, centered=(False, True, True))
    .translate((-tail_tip_len, 0, 0))
)

# Combine all solids into the base shape
result = main_body.union(clevis_base).union(clevis_ears).union(tail_stem).union(tail_tip)

# --- Cuts and Features ---

# 4. Clevis Slot (Gap between arms)
# Cut from the pivot tip back to the main body face
cut_len = clevis_straight_len + ear_radius
cut_center_x = (body_length / 2.0) + (cut_len / 2.0)

result = result.cut(
    cq.Workplane("XY")
    .box(cut_len, clevis_gap, body_height)
    .translate((cut_center_x, 0, 0))
)

# 5. Pin and Hole Mechanism (Asymmetric)
# Left Arm (Y+): Hole
# Right Arm (Y-): Pin Boss

# Cut Hole on +Y Arm
# We create a cutter cylinder positioned to intersect only the +Y arm
result = result.cut(
    cq.Workplane("XZ")
    .workplane(offset=body_width/2.0 + 1.0) # Start outside
    .moveTo(pivot_x, 0)
    .circle(pin_diameter / 2.0)
    .extrude(-(body_width - clevis_gap)/2.0 - 2.0) # Cut inward through the arm
)

# Add Pin Boss on -Y Arm (Outer face)
# We extrude a boss from the -Y face outwards
pin_boss = (
    cq.Workplane("XZ")
    .workplane(offset=-body_width/2.0)
    .moveTo(pivot_x, 0)
    .circle(pin_diameter / 2.0)
    .extrude(-pin_boss_height)
)
result = result.union(pin_boss)

# 6. Side Windows (Pockets on Main Body)
# Right Side (+Y)
result = result.cut(
    cq.Workplane("XZ")
    .workplane(offset=body_width/2.0)
    .moveTo(0, 0) # Center of body
    .rect(window_width, window_height)
    .extrude(-window_depth) # Cut into the body (opposing normal)
)

# Left Side (-Y)
result = result.cut(
    cq.Workplane("XZ")
    .workplane(offset=-body_width/2.0)
    .moveTo(0, 0)
    .rect(window_width, window_height)
    .extrude(window_depth)
)