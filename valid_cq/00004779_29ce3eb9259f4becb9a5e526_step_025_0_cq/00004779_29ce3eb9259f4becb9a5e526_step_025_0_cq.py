import cadquery as cq

# Parametric dimensions
plate_width = 100.0
plate_height = 100.0
thickness = 5.0
fillet_radius = 5.0

# Hole pattern parameters
center_hole_dia = 5.0
inner_hole_spacing = 20.0  # Spacing for the inner X pattern
outer_hole_spacing_x = 35.0 # X spacing for the vertical columns
outer_hole_spacing_y = 25.0 # Y spacing for the vertical columns

# Slot parameters
slot_length_long = 40.0
slot_length_short = 20.0
slot_width = 5.0
slot_offset_y_long = 30.0
slot_offset_y_short = 42.0

# Create the base plate
result = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)

# 1. Center hole
result = result.faces(">Z").workplane().hole(center_hole_dia)

# 2. Inner "X" pattern holes (4 holes surrounding center)
# Located at roughly (+/- 10, +/- 10) if center is (0,0)
inner_pts = [
    (inner_hole_spacing/2, inner_hole_spacing/2),
    (inner_hole_spacing/2, -inner_hole_spacing/2),
    (-inner_hole_spacing/2, inner_hole_spacing/2),
    (-inner_hole_spacing/2, -inner_hole_spacing/2),
]
result = result.faces(">Z").workplane().pushPoints(inner_pts).hole(center_hole_dia)

# 3. Outer vertical columns of holes
# These seem to be aligned vertically on the left and right sides.
# Let's assume 3 holes on each side column shown in the middle section.
outer_pts = [
    # Right column
    (outer_hole_spacing_x, 0),
    (outer_hole_spacing_x, outer_hole_spacing_y),
    (outer_hole_spacing_x, -outer_hole_spacing_y),
    # Left column
    (-outer_hole_spacing_x, 0),
    (-outer_hole_spacing_x, outer_hole_spacing_y),
    (-outer_hole_spacing_x, -outer_hole_spacing_y),
]
# The holes in the outer columns look slightly larger in the image, or same size. 
# Let's assume slightly larger based on visual weight, or stick to uniform. 
# Looking closely, the central 5 holes look uniform. The outer columns look uniform.
# Let's keep them uniform for simplicity, or slightly larger (6mm).
result = result.faces(">Z").workplane().pushPoints(outer_pts).hole(6.0)


# 4. Slots
# There are horizontal slots at the top and bottom.
# A long pair and a short pair.

# Long slots (inner top/bottom)
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(0, slot_offset_y_long), (0, -slot_offset_y_long)])
    .slot2D(slot_length_long, slot_width)
    .cutThruAll()
)

# Short slots (outer top/bottom corners)
# These are actually pairs of slots, not single centered slots.
# Top left, Top right, Bottom left, Bottom right.
# Visually looking at the image, the top row has two short slots, not one long one?
# Wait, looking closer:
# Top section: One long central slot, two shorter slots on the sides.
# Actually, looking at the crop, it looks like:
# Top row: Two short slots near the corners.
# Second row down: One long slot in the middle.
# Let's re-examine. 
# The image shows:
# Top-most features: Two short horizontal slots near corners.
# Just below that: Two long horizontal slots (one left, one right? No, looks like one wide one? 
# No, looking at the shadows, it's a symmetric pattern.
# Let's look at the "Top" grouping.
# It has a long slot spanning the center.
# Above that long slot, there are two shorter slots at the corners.
# Let's correct the logic.

# Create the long slots (Top and Bottom, centered)
# Actually, looking at the specific image provided:
# There is a long slot pattern at Y +/- 30ish.
# But wait, looking at the connectivity...
# Let's look at the top half. 
# There is a wide horizontal slot.
# Above it (higher Y), there are two smaller slots on the left and right.
# Same for the bottom.

# Long centered slots
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(0, 25.0), (0, -25.0)]) # Adjusted Y offset based on visual
    .slot2D(40.0, 5.0)
    .cutThruAll()
)

# Corner slots
# Located at corners, oriented horizontally.
corner_slot_dx = 30.0
corner_slot_dy = 40.0
corner_slot_length = 15.0

corner_pts = [
    (corner_slot_dx, corner_slot_dy),
    (-corner_slot_dx, corner_slot_dy),
    (corner_slot_dx, -corner_slot_dy),
    (-corner_slot_dx, -corner_slot_dy),
]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(corner_pts)
    .slot2D(corner_slot_length, 5.0)
    .cutThruAll()
)

# Additional holes near the corner slots?
# The image shows holes roughly aligned with the ends of the long slots.
# Let's add the corner holes that are part of the outer column but near the top/bottom.
# The previous outer_pts handled the middle 3 vertical ones. 
# There seem to be holes near the ends of the plate in that same vertical line.
outer_corner_pts = [
    (outer_hole_spacing_x, 40.0), # Near top right
    (-outer_hole_spacing_x, 40.0), # Near top left
    (outer_hole_spacing_x, -40.0), # Near bottom right
    (-outer_hole_spacing_x, -40.0), # Near bottom left
]
# Wait, these interfere with the corner slots I just made.
# Let's look really closely at the image.
# Center: 1 hole.
# Around center: 4 holes in diamond/square.
# Left/Right columns: 3 holes each vertically.
# Top/Bottom blocks:
#   - One long horizontal slot.
#   - Above that slot (towards edge), two smaller horizontal slots.
#   - It looks like there are no extra holes in the very corners, just the slots.

# Refined Plan:
# Base Plate: 100x100
# Center Hole: (0,0)
# Inner Square Pattern: (+/- 15, +/- 15)
# Side Columns: (+/- 35, 0), (+/- 35, +/- 20)
# Long Slots: Centered at (0, +/- 32), length ~45
# Short Corner Slots: Centered at (+/- 30, +/- 42), length ~20

# Let's rebuild the hole/slot logic with these more precise visual estimates.

# Reset result for the refined logic
result = (
    cq.Workplane("XY")
    .rect(plate_width, plate_height)
    .extrude(thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)

# 1. Circular Holes
# Center
holes = [(0,0)]
# Inner Square (4 holes)
inner_dist = 14.0
holes.extend([
    (inner_dist, inner_dist), (inner_dist, -inner_dist),
    (-inner_dist, inner_dist), (-inner_dist, -inner_dist)
])
# Side Columns (6 holes total, 3 per side)
side_x = 32.0
side_y_step = 18.0
holes.extend([
    (side_x, 0), (side_x, side_y_step), (side_x, -side_y_step),
    (-side_x, 0), (-side_x, side_y_step), (-side_x, -side_y_step)
])

result = result.faces(">Z").workplane().pushPoints(holes).hole(5.5)

# 2. Long Slots (Top and Bottom middle)
long_slot_y = 30.0
long_slot_len = 40.0
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(0, long_slot_y), (0, -long_slot_y)])
    .slot2D(long_slot_len, slot_width)
    .cutThruAll()
)

# 3. Short Slots (Corners)
short_slot_x = 28.0
short_slot_y = 42.0
short_slot_len = 20.0
short_slots_pts = [
    (short_slot_x, short_slot_y),
    (-short_slot_x, short_slot_y),
    (short_slot_x, -short_slot_y),
    (-short_slot_x, -short_slot_y),
]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(short_slots_pts)
    .slot2D(short_slot_len, slot_width)
    .cutThruAll()
)