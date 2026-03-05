import cadquery as cq

# Build the assembly: two cylindrical columns with slots, a hex nut section, and a rod

# Parameters
col_radius = 8
col_height = 80
slot_width = 3
slot_depth = 4

# Column 1 (left) - cylinder with two opposing slots
col1 = (
    cq.Workplane("XY")
    .cylinder(col_height, col_radius)
)

# Cut slots into column 1
slot1 = (
    cq.Workplane("XY")
    .box(slot_width, slot_depth * 2, col_height + 2)
    .translate((col_radius - slot_depth/2, 0, col_height/2))
)

slot2 = (
    cq.Workplane("XY")
    .box(slot_width, slot_depth * 2, col_height + 2)
    .translate((-(col_radius - slot_depth/2), 0, col_height/2))
)

col1 = col1.cut(slot1).cut(slot2)

# Also add a vertical ridge/rib on the side
rib1 = (
    cq.Workplane("XY")
    .box(2, 2, col_height)
    .translate((col_radius + 1, 0, col_height/2))
)
col1 = col1.union(rib1)

# Column 2 (right) - similar but with rod/screw mechanism at bottom
col2 = (
    cq.Workplane("XY")
    .cylinder(col_height, col_radius)
    .translate((22, 0, 0))
)

# Cut slots into column 2
slot3 = (
    cq.Workplane("XY")
    .box(slot_width, slot_depth * 2, col_height + 2)
    .translate((22 + col_radius - slot_depth/2, 0, col_height/2))
)

slot4 = (
    cq.Workplane("XY")
    .box(slot_width, slot_depth * 2, col_height + 2)
    .translate((22 - (col_radius - slot_depth/2), 0, col_height/2))
)

col2 = col2.cut(slot3).cut(slot4)

# Add small rib on col2
rib2 = (
    cq.Workplane("XY")
    .box(2, 2, col_height)
    .translate((22 + col_radius + 1, 0, col_height/2))
)
col2 = col2.union(rib2)

# Hex nut section below column 2
hex_nut = (
    cq.Workplane("XY")
    .polygon(6, 18)
    .extrude(12)
    .translate((22, 0, -12))
)

# Rod below hex nut
rod = (
    cq.Workplane("XY")
    .cylinder(50, 3)
    .translate((22, 0, -12 - 25))
)

# Rod tip (small disk)
rod_tip = (
    cq.Workplane("XY")
    .cylinder(2, 5)
    .translate((22, 0, -12 - 50 - 1))
)

# Combine everything
result = col1.union(col2).union(hex_nut).union(rod).union(rod_tip)