import cadquery as cq
import math

# --- Parameters ---

# Main Body Dimensions
body_diameter = 20.0
body_length = 60.0
slant_angle = 50.0       # Angle of the cut face from vertical (degrees)
groove_pos = 5.0         # Distance from the flat back face
groove_width = 1.0
groove_depth = 0.5

# Stem Dimensions
stem_pos_x = 12.0        # Position along the cylinder from the back
stem_hex_flat = 6.0      # Hex nut width (flat-to-flat)
stem_hex_height = 2.5
stem_rod_diameter = 2.0
stem_rod_length = 35.0

# Head Dimensions
head_diameter = 9.0
head_height = 5.0
head_chamfer = 0.5
head_slot_width = 1.5
head_slot_depth = 2.0
head_hole_diameter = 2.5

# --- Modeling ---

# 1. Main Cylindrical Body
# Create cylinder along X axis starting from origin
body = cq.Workplane("YZ").circle(body_diameter / 2.0).extrude(body_length)

# Slanted Cut at the end
# We create a cutter object (a large box) and rotate it to slice the end of the cylinder.
# The cut is anchored at the bottom-most point of the cylinder's end face to preserve the length there.
cut_anchor = (body_length, 0, -body_diameter / 2.0)
cutter_size = body_diameter * 4

cutter = (
    cq.Workplane("YZ", origin=cut_anchor)
    .rect(cutter_size, cutter_size)
    .extrude(cutter_size)  # Extrudes in +X direction initially
    # Rotate "back" around the Y-axis centered at the anchor point
    .rotate(cut_anchor, (body_length, 1, -body_diameter / 2.0), -slant_angle)
)

# Apply the cut
body = body.cut(cutter)

# Groove near the back
# Create a ring shaped cutter
groove_cutter = (
    cq.Workplane("YZ", origin=(groove_pos, 0, 0))
    .circle(body_diameter / 2.0 + 5.0)  # Outer radius (large enough to clear body)
    .circle(body_diameter / 2.0 - groove_depth)  # Inner radius (groove floor)
    .extrude(groove_width)
)

# Apply the groove cut
body = body.cut(groove_cutter)


# 2. Stem Assembly
# Define the connection point on the top surface of the cylinder
stem_origin = (stem_pos_x, 0, body_diameter / 2.0)

# Hexagonal Base (Nut)
# Calculate circumradius for the polygon based on flat-to-flat width
# flat_width = sqrt(3) * radius => radius = width / sqrt(3)
# CadQuery polygon uses diameter (2 * radius)
hex_circum_dia = stem_hex_flat / (math.sqrt(3) / 2.0)

stem = (
    cq.Workplane("XY", origin=stem_origin)
    .polygon(6, hex_circum_dia)
    .extrude(stem_hex_height)
)

# Vertical Rod
stem = (
    stem.faces(">Z").workplane()
    .circle(stem_rod_diameter / 2.0)
    .extrude(stem_rod_length)
)

# Cylindrical Head
stem = (
    stem.faces(">Z").workplane()
    .circle(head_diameter / 2.0)
    .extrude(head_height)
)

# Head Features: Top Chamfer
stem = stem.faces(">Z").edges().chamfer(head_chamfer)

# Head Features: Slot
# Cut a slot perpendicular to the main cylinder axis (along Y-axis locally)
stem = (
    stem.faces(">Z").workplane()
    .rect(head_slot_width, head_diameter * 1.5) # Width x Length (Long in Y)
    .cutBlind(-head_slot_depth)
)

# Head Features: Central Hole
stem = (
    stem.faces(">Z").workplane()
    .circle(head_hole_diameter / 2.0)
    .cutBlind(-head_height)
)

# 3. Combine Result
# Union the main body and the stem assembly
result = body.union(stem)