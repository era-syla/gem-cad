import cadquery as cq

# Parameters
outer_radius = 50.0
inner_radius = 20.0
thickness = 10.0
angle = 90.0

# Feature dimensions
slot_width = 8.0
slot_depth = 20.0
tab_width = 8.0
tab_depth = 5.0
hole_diameter = 4.0

# Create the base sector shape
# We start with a solid cylinder and cut it to form the sector
base = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .extrude(thickness)
)

# Create a cutting tool to isolate the sector (roughly 90 degrees)
# We create a large box to subtract everything except the first quadrant
cutter = (
    cq.Workplane("XY")
    .rect(outer_radius * 3, outer_radius * 3)
    .extrude(thickness)
    .translate((-outer_radius * 1.5, -outer_radius * 1.5, 0)) # Move to quadrant 3
)
# Additional cutter for the top-left quadrant to ensure only top-right remains
cutter2 = (
    cq.Workplane("XY")
    .rect(outer_radius * 3, outer_radius * 3)
    .extrude(thickness)
    .translate((-outer_radius * 1.5, outer_radius * 1.5, 0)) # Move to quadrant 2
)
# Additional cutter for bottom-right
cutter3 = (
    cq.Workplane("XY")
    .rect(outer_radius * 3, outer_radius * 3)
    .extrude(thickness)
    .translate((outer_radius * 1.5, -outer_radius * 1.5, 0)) # Move to quadrant 4
)

# Apply the cuts to get the quarter pie
sector = base.cut(cutter).cut(cutter2).cut(cutter3)

# Create the inner curved cut (the arc cutout on the left/top side)
inner_cut = (
    cq.Workplane("XY")
    .circle(inner_radius)
    .extrude(thickness)
)
result = sector.cut(inner_cut)

# --- Add Specific Details ---

# 1. The stepped notches on the straight edges
# Vertical edge (Y-axis aligned face) notches
notch1 = (
    cq.Workplane("YZ")
    .rect(tab_width, thickness)
    .extrude(tab_depth)
    .translate((0, thickness/2, outer_radius - 10))
    .rotate((0,0,0), (0,0,1), 90) # Rotate to align with Y axis face
)

notch2 = (
    cq.Workplane("YZ")
    .rect(tab_width, thickness)
    .extrude(tab_depth)
    .translate((0, thickness/2, outer_radius - 25))
    .rotate((0,0,0), (0,0,1), 90)
)

# Horizontal edge (X-axis aligned face) notches
notch3 = (
    cq.Workplane("XZ")
    .rect(tab_width, thickness)
    .extrude(tab_depth)
    .translate((outer_radius - 10, thickness/2, 0))
)

notch4 = (
    cq.Workplane("XZ")
    .rect(tab_width, thickness)
    .extrude(tab_depth)
    .translate((outer_radius - 25, thickness/2, 0))
)

# Subtract notches to create the "teeth" look
result = result.cut(notch1).cut(notch2).cut(notch3).cut(notch4)

# 2. The large angled slot in the middle
# This looks like a rectangular pocket angled relative to the axes
slot_length = 30.0
slot_w = 6.0

middle_slot = (
    cq.Workplane("XY")
    .transformed(offset=(25, 25, thickness - 3.0), rotate=(0, 0, 45))
    .rect(slot_length, slot_w)
    .extrude(-5.0) # Depth of the slot
)

# A small hole inside the slot
slot_hole = (
    cq.Workplane("XY")
    .transformed(offset=(25, 25, thickness - 3.0), rotate=(0, 0, 45))
    .circle(1.5)
    .extrude(-10.0) # Through hole
)

result = result.cut(middle_slot).cut(slot_hole)

# 3. The circular hole near the inner radius
# Located roughly at 45 degrees near the inner curve
hole_pos_r = inner_radius + 8.0
hole_pos_x = hole_pos_r * 0.707 # cos(45)
hole_pos_y = hole_pos_r * 0.707 # sin(45)

corner_hole = (
    cq.Workplane("XY")
    .translate((hole_pos_x, hole_pos_y, 0))
    .circle(hole_diameter / 2)
    .extrude(thickness)
)

result = result.cut(corner_hole)

# 4. Refine the shape: The "stepped" look on top
# The image shows the top face isn't perfectly flat, it has a lowered section
# closer to the X-axis edge.
step_cut = (
    cq.Workplane("XY")
    .workplane(offset=thickness)
    .rect(outer_radius, outer_radius)
    .extrude(-2.0) # Step down depth
    .translate((outer_radius/2, -outer_radius/4, 0)) 
)
# We only want this step on the lower half (relative to the diagonal)
# This is a simplification to approximate the visual topology
result = result.cut(step_cut)

# Final cleanup/orientation if needed
# (None applied here as standard Z-up orientation is used)