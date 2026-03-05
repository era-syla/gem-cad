import cadquery as cq

# --- Parameters ---
# Main housing dimensions
box_length = 60.0
box_width = 40.0
box_height = 20.0
wall_thickness = 2.0
floor_thickness = 2.0

# Slot configuration
num_slots = 5
# Calculate slot width based on fixed wall thickness
# Width = (num_slots * slot_width) + ((num_slots + 1) * wall_thickness)
slot_width = (box_width - ((num_slots + 1) * wall_thickness)) / num_slots

# Hinge dimensions
hinge_od = 12.0
hinge_id = 8.0
hinge_x_offset = -box_length / 2 + hinge_od / 2
hinge_y_offset = -box_width / 2 - hinge_od / 2 + 1.5 # 1.5mm overlap

# --- 1. Main Body Generation ---
# Base block
main_body = cq.Workplane("XY").box(box_length, box_width, box_height)

# Create cuts for slots
# Slots run along X axis
slot_cutter = (
    cq.Workplane("XY")
    .rect(box_length - 2 * wall_thickness, slot_width)
    .extrude(box_height - floor_thickness)
    .translate((0, 0, floor_thickness/2)) # Shift up to leave floor
)

# Apply cuts in a pattern
for i in range(num_slots):
    # Calculate Y position for each slot
    # Start from -width/2, add first wall, add half slot width, add i * pitch
    y_pos = -box_width/2 + wall_thickness + slot_width/2 + i * (slot_width + wall_thickness)
    
    # Move the cutter to the correct Y position
    current_cut = slot_cutter.translate((0, y_pos, (box_height - (box_height - floor_thickness))/2))
    main_body = main_body.cut(current_cut)

# Create the hinge cylinder
hinge = (
    cq.Workplane("XY")
    .circle(hinge_od / 2)
    .circle(hinge_id / 2)
    .extrude(box_height)
    .translate((hinge_x_offset, hinge_y_offset, -box_height/2))
)

# Create a bridge to connect the hinge to the main body
bridge = (
    cq.Workplane("XY")
    .rect(hinge_od, hinge_od)
    .extrude(box_height)
    .translate((hinge_x_offset, hinge_y_offset + hinge_od/2, -box_height/2))
)

# Fuse hinge assembly to main body
main_body = main_body.union(hinge).union(bridge)


# --- 2. Left Part (Comb Insert) ---
# A bar with protrusions that match the slots
comb_spine_thickness = 4.0
comb_tooth_length = 5.0
comb_height = 10.0
comb_width = box_width - 2*wall_thickness # Fits inside outer walls roughly

# Create the spine
left_part = (
    cq.Workplane("XY")
    .box(comb_spine_thickness, comb_width, comb_height)
    .translate((-box_length/2 - 15, 0, -box_height/2 + comb_height/2))
)

# Add teeth
# The comb in the image has 4 teeth.
# We'll align them with the first 4 slots for visual similarity
comb_tooth = (
    cq.Workplane("XY")
    .box(comb_tooth_length, slot_width - 0.5, comb_height) # Slightly smaller than slot
)

for i in range(4):
    y_pos = -box_width/2 + wall_thickness + slot_width/2 + i * (slot_width + wall_thickness)
    tooth_pos_x = -box_length/2 - 15 + comb_spine_thickness/2 + comb_tooth_length/2
    
    current_tooth = comb_tooth.translate((tooth_pos_x, y_pos, -box_height/2 + comb_height/2))
    left_part = left_part.union(current_tooth)


# --- 3. Right Part (End Clip) ---
# A small plate with a hinge-like loop
clip_thickness = 4.0
clip_width = 20.0
clip_height = 15.0

# Base plate
right_part = (
    cq.Workplane("XY")
    .box(clip_thickness, clip_width, clip_height)
    .translate((box_length/2 + 15, 0, -box_height/2 + clip_height/2))
)

# Loop feature on the clip
clip_loop = (
    cq.Workplane("XY")
    .circle(4)
    .circle(2)
    .extrude(5)
    .rotate((1,0,0), (0,0,0), 90) # Rotate to be horizontal
    .translate((box_length/2 + 15, 0, -box_height/2 + clip_height + 2.5))
)

# Alternative: Vertical loop as seen in the rightmost part of image
clip_loop_vertical = (
    cq.Workplane("XY")
    .circle(3.5)
    .circle(2.0)
    .extrude(clip_height)
    .translate((box_length/2 + 15 - clip_thickness/2, -clip_width/2 + 3.5, -box_height/2))
)

right_part = right_part.union(clip_loop_vertical)

# --- Final Assembly ---
# Combine all parts into one result object for visualization
result = main_body.union(left_part).union(right_part)