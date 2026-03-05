import cadquery as cq
import math

# --- Parameters ---
# Main Body dimensions
body_dia = 24.0
body_radius = body_dia / 2.0
body_length = 85.0
cut_angle = 45.0  # Degrees

# End Cap / Groove dimensions
cap_length = 15.0
groove_width = 0.8
groove_depth = 0.5

# Stem assembly dimensions
stem_x_pos = cap_length / 2.0
nut_size_flats = 8.0  # Hex nut size
nut_height = 3.5
stem_dia = 3.0
stem_height = 55.0

# Knob dimensions
knob_dia = 12.0
knob_height = 8.0
slot_width = 2.0
slot_depth = 3.0
hole_dia = 3.0

# --- Modeling ---

# 1. Main Cylindrical Body
# Create cylinder along X-axis
main_body = (
    cq.Workplane("YZ")
    .circle(body_radius)
    .extrude(body_length)
)

# 2. Angled Cut
# Define a cutter box. We position it at the bottom-end corner of the cylinder
# and rotate it so it slices the top-front section off.
# Pivot point: Bottom of the cylinder at the far end (max X, min Z)
pivot_pt = cq.Vector(body_length, 0, -body_radius)

# Create the cutter
# We rotate -45 degrees around Y to make the cutting plane slope back-and-up.
# The box extends in +X (local), which corresponds to Up-and-Right in global, 
# removing the material above the diagonal.
cutter = (
    cq.Workplane("YZ")
    .transformed(offset=pivot_pt, rotate=cq.Vector(0, -cut_angle, 0))
    .box(100, 100, 100, centered=(False, True, True))
)

main_body = main_body.cut(cutter)

# 3. Groove
# Create a ring to subtract from the body to form the groove
groove_cutter = (
    cq.Workplane("YZ")
    .workplane(offset=cap_length)
    .circle(body_radius + 2.0)  # Outer boundary (clearance)
    .circle(body_radius - groove_depth)  # Inner boundary (cut depth)
    .extrude(groove_width)
)

main_body = main_body.cut(groove_cutter)

# 4. Hex Nut Base
# Calculate circumdiameter for polygon: D = Size / (sqrt(3)/2)
nut_poly_dia = nut_size_flats / (math.sqrt(3) / 2.0)

nut = (
    cq.Workplane("XY")
    .workplane(offset=body_radius - 1.5)  # Sink slightly into cylinder
    .center(stem_x_pos, 0)
    .polygon(6, nut_poly_dia)
    .extrude(nut_height + 1.5)
)
# Add a small fillet to top of nut for realism
nut = nut.edges(">Z").fillet(0.4)

# 5. Vertical Stem
stem_z_start = body_radius + nut_height
stem = (
    cq.Workplane("XY")
    .workplane(offset=stem_z_start)
    .center(stem_x_pos, 0)
    .circle(stem_dia / 2.0)
    .extrude(stem_height)
)

# 6. Top Knob
knob_z_start = stem_z_start + stem_height
knob = (
    cq.Workplane("XY")
    .workplane(offset=knob_z_start)
    .center(stem_x_pos, 0)
    .circle(knob_dia / 2.0)
    .extrude(knob_height)
)
# Fillet top and bottom edges of knob
knob = knob.edges("not(|Z)").fillet(0.8)

# 7. Slot and Hole in Knob
slot_cutter = (
    cq.Workplane("XY")
    .workplane(offset=knob_z_start + knob_height)
    .center(stem_x_pos, 0)
    .rect(knob_dia * 1.5, slot_width)
    .extrude(-slot_depth)
)

hole_cutter = (
    cq.Workplane("XY")
    .workplane(offset=knob_z_start + knob_height)
    .center(stem_x_pos, 0)
    .circle(hole_dia / 2.0)
    .extrude(-(slot_depth + 2.0))
)

# Apply cuts to knob
knob = knob.cut(slot_cutter).cut(hole_cutter)

# --- Final Assembly ---
result = (
    main_body
    .union(nut)
    .union(stem)
    .union(knob)
)