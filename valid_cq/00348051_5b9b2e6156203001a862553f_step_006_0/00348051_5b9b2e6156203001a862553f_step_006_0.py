import cadquery as cq

# Parameters for dimensions
plate_width = 220.0
plate_length = 320.0
thickness = 5.0
fillet_radius = 8.0

# Feature dimensions
long_slot_w = 160.0
long_slot_h = 24.0
long_slot_y_pos = 100.0

small_slot_w = 40.0
small_slot_h = 24.0
small_slot_y_pos = -80.0
small_slot_x_offset = 60.0

hole_diameter = 4.5

# 1. Create the base plate with filleted corners
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_length, thickness)
    .edges("|Z")
    .fillet(fillet_radius)
)

# 2. Cut the top long slot
result = (
    result.faces(">Z")
    .workplane()
    .center(0, long_slot_y_pos)
    .rect(long_slot_w, long_slot_h)
    .cutThruAll()
)

# 3. Cut the two bottom small slots
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(-small_slot_x_offset, small_slot_y_pos), 
                 (small_slot_x_offset, small_slot_y_pos)])
    .rect(small_slot_w, small_slot_h)
    .cutThruAll()
)

# 4. Define hole positions
# Top row: 4 holes distributed along the top edge
top_holes = [(-70, 140), (-25, 140), (25, 140), (70, 140)]

# Flank holes: 2 holes on the sides of the long slot
flank_holes = [(-95, 100), (95, 100)]

# Mid-side holes: 2 holes near the side edges in the middle section
mid_holes = [(-95, 0), (95, 0)]

# Bottom holes: Pairs of holes beneath each small slot
# Left pair and Right pair
bottom_holes = [(-70, -135), (-50, -135), (50, -135), (70, -135)]

all_hole_locations = top_holes + flank_holes + mid_holes + bottom_holes

# 5. Drill all holes
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(all_hole_locations)
    .hole(hole_diameter)
)