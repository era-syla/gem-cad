import cadquery as cq

# Parameters for the extrusion model
length = 800.0         # Total length of the bar
profile_size = 20.0    # Width/Height of the profile (e.g., 20mm for 2020 extrusion)
slot_width = 6.0       # Width of the slot opening
slot_depth = 5.0       # Depth of the slot
center_hole_dia = 5.0  # Diameter of the central bore
corner_radius = 1.0    # Radius for corner fillets

# 1. Create the base solid: A square extrusion with rounded corners
base = (
    cq.Workplane("XY")
    .rect(profile_size, profile_size)
    .extrude(length)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Define the cutters
# We create cutter solids representing the negative volume of the slots and hole
# A cutter height of slot_depth*2 ensures it crosses the boundary of the profile cleanly

# Vertical cutter profile (for Top/Bottom slots)
v_cutter = (
    cq.Workplane("XY")
    .rect(slot_width, slot_depth * 2)
    .extrude(length)
)

# Horizontal cutter profile (for Left/Right slots)
h_cutter = (
    cq.Workplane("XY")
    .rect(slot_depth * 2, slot_width)
    .extrude(length)
)

# Center hole cutter
hole_cutter = (
    cq.Workplane("XY")
    .circle(center_hole_dia / 2.0)
    .extrude(length)
)

# 3. Position cutters and subtract from base
offset_dist = profile_size / 2.0

result = (
    base
    .cut(v_cutter.translate((0, offset_dist, 0)))    # Cut Top Face
    .cut(v_cutter.translate((0, -offset_dist, 0)))   # Cut Bottom Face
    .cut(h_cutter.translate((offset_dist, 0, 0)))    # Cut Right Face
    .cut(h_cutter.translate((-offset_dist, 0, 0)))   # Cut Left Face
    .cut(hole_cutter)                                # Cut Center Hole
)