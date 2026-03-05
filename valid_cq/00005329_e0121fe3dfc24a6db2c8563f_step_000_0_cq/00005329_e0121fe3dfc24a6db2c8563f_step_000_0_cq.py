import cadquery as cq

# Parameters
total_length = 80.0
total_width = 30.0

# Head section (the thicker block)
head_length = 35.0
head_height = 15.0
slant_length = 8.0  # Horizontal distance of the front slant
recess_depth = 2.0
rim_thickness = 2.0

# Tail section (the thinner plate)
tail_length = total_length - head_length
tail_thickness = 2.5
tail_rail_height = 4.0  # Height of the side rails on the tail
tail_rail_width = 1.5

# Slot parameters
slot_width = 1.5
slot_length = 8.0
slot_position_z = 6.0 # From bottom
slot_position_x = -head_length / 2 + 10 # Approximate position relative to head center

# Create the base geometry
# 1. Build the Head Section
# Start with a simple block
head = cq.Workplane("XY").box(head_length, total_width, head_height)

# Create the slanted front face
# We'll cut a wedge off the front
wedge = (
    cq.Workplane("XY")
    .workplane(offset=head_height/2) # Start at top
    .moveTo(-head_length/2, 0) # Front edge
    .rect(slant_length * 2, total_width + 5) # Oversized rect to cut
    .rotate((0,0,0), (0,1,0), 45) # Rotate to create angle. Adjusting via separate loft strategy might be cleaner, but subtractive works
)
# A cleaner way to make the slant: Loft or Chamfer?
# Let's try a Chamfer approach on the specific edge.
# Find the bottom-front edge.
head = head.edges("<X and <Z").chamfer(slant_length)

# Create the recess on top of the head
# Select top face, offset inward to leave a rim, cut down
head = (
    head.faces(">Z")
    .workplane()
    .rect(head_length - rim_thickness*2, total_width - rim_thickness*2)
    .cutBlind(-recess_depth)
)

# Create the side slot on the head
# Select the side face, draw slot, cut through
head = (
    head.faces(">Y")
    .workplane()
    .moveTo(slot_position_x, slot_position_z - head_height/2)
    .slot2D(slot_length, slot_width, angle=90)
    .cutBlind(-total_width) # Cut through both sides or just one? Image suggests maybe just one or through. Assume through for symmetry or deep blind.
)


# 2. Build the Tail Section
# The tail extends from the back of the head.
# It sits flush with the top (mostly), but the image shows the head is taller.
# Let's align the top of the tail slightly below the top rim of the head.

tail_z_offset = head_height/2 - recess_depth - tail_thickness/2 # Align with the recessed floor
tail_center_x = head_length/2 + tail_length/2

tail_plate = (
    cq.Workplane("XY")
    .workplane(offset=tail_z_offset)
    .center(tail_center_x, 0)
    .box(tail_length, total_width, tail_thickness)
)

# Add rails to the tail (underneath)
rail_z_offset = tail_z_offset - tail_thickness/2 - (tail_rail_height - tail_thickness)/2
left_rail = (
    cq.Workplane("XY")
    .workplane(offset=rail_z_offset)
    .center(tail_center_x, -total_width/2 + tail_rail_width/2)
    .box(tail_length, tail_rail_width, tail_rail_height - tail_thickness)
)
right_rail = (
    cq.Workplane("XY")
    .workplane(offset=rail_z_offset)
    .center(tail_center_x, total_width/2 - tail_rail_width/2)
    .box(tail_length, tail_rail_width, tail_rail_height - tail_thickness)
)

# Combine parts
result = head.union(tail_plate).union(left_rail).union(right_rail)

# Small notch on the side of the tail (visible in image)
notch_width = 4.0
notch_depth = 1.0
notch_x_pos = head_length/2 + 5.0 # Just past the junction

result = (
    result.faces(">Y[1]") # Select the side face of the tail
    .workplane(centerOption="CenterOfBoundBox")
    .moveTo(notch_x_pos - tail_center_x, 0) # Adjust relative coordinates
    .rect(notch_width, tail_thickness + 5) # Cut vertically
    .cutBlind(-notch_depth)
)

# Fillet/Chamfer the back corners of the tail slightly
result = result.edges(">X").fillet(0.5)

# The transition from head to tail: The head has a back wall.
# The current union creates a solid intersection.
# The image shows the head's rim extends slightly over the tail or forms a step.
# The current geometry aligns the tail plate with the floor of the head recess, which is consistent with injection molded sliders.

# Optional: Add the small lip on the front of the recess if needed, but the cutBlind handled the main recess.

# Refine the slot - make it only on one side as per typical injection molding design (or both). Let's keep it through for simplicity or modify to blind if needed.
# The image shows it on the visible side. The code cuts all the way through (-total_width).

# Final assignment
result = result