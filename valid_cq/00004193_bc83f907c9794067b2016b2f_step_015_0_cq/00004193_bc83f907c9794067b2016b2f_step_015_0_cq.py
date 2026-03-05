import cadquery as cq

# --- Parameter Definitions ---

# Main block dimensions
block_length = 100.0
block_width = 60.0
block_height = 50.0

# Corner cutout dimensions
cutout_length = 30.0  # Length of the recessed area along the block length
cutout_width = 30.0   # Width of the recessed area along the block width
cutout_depth = 5.0    # Depth of the recess from the top surface

# Plate dimensions (the thin sheet floating above the cutout)
plate_thickness = 1.0
plate_offset_z = 20.0 # Height of plate relative to the main block top surface

# Support rods
rod_diameter = 1.0
rod_locations = [
    (-cutout_length + 2, -cutout_width + 2), # Inner corner
    (-cutout_length + 2, 2),                 # Near edge
    (2, -cutout_width + 2),                  # Near edge
    (2, 2)                                   # Outer corner
]

# Side notches
notch_width = 4.0
notch_depth = 4.0
notch_spacing = 20.0 # Distance between centers of notches

# --- Geometry Construction ---

# 1. Create the main rectangular block
main_block = cq.Workplane("XY").box(block_length, block_width, block_height)

# 2. Create the corner cutout
# We position the workplane on top and cut a rectangle from one corner.
# Let's target the "top-left" corner relative to the center origin for the cutout based on the image perspective.
# Assuming origin is center of the block.
# Cutout corner: Top (-Y), Left (-X) relative to standard view, but let's align with the image.
# In the image, the cutout is back-left.
cutout_x_pos = -block_length/2 + cutout_length/2
cutout_y_pos = block_width/2 - cutout_width/2

main_block_cut = (
    main_block
    .faces(">Z")
    .workplane()
    .center(cutout_x_pos, cutout_y_pos)
    .rect(cutout_length, cutout_width)
    .cutBlind(-cutout_depth)
)

# 3. Create the thin plate floating above the cutout
# The plate matches the cutout footprint but is positioned higher up.
plate = (
    cq.Workplane("XY")
    .workplane(offset=block_height/2 + plate_offset_z)
    .center(cutout_x_pos, cutout_y_pos)
    .rect(cutout_length, cutout_width)
    .extrude(plate_thickness)
)

# 4. Create the vertical support rods
# These connect the bottom of the cutout to the floating plate.
# The rods start at the bottom of the cutout (block_height/2 - cutout_depth)
# and go up past the plate or through it. 
# Based on image, they seem to stick up slightly above the plate.

rod_base_z = block_height/2 - cutout_depth
rod_height = cutout_depth + plate_offset_z + plate_thickness + 5.0 # Extra length sticking up

rods = cq.Workplane("XY").workplane(offset=rod_base_z)

# We need to position rods relative to the cutout center
cutout_center_x = -block_length/2 + cutout_length/2
cutout_center_y = block_width/2 - cutout_width/2

for rx, ry in rod_locations:
    # Adjust rod local coordinates to global coordinates based on cutout center
    # The rod_locations defined above were relative to the cutout corner roughly.
    # Let's simplify: position relative to cutout center
    # Redefining locations relative to the center of the cutout rect for clarity
    local_rod_pts = [
        (cutout_center_x - cutout_length/2 + 2, cutout_center_y + cutout_width/2 - 2), # Corner
        (cutout_center_x + cutout_length/2 - 2, cutout_center_y + cutout_width/2 - 2), # Corner
        (cutout_center_x - cutout_length/2 + 2, cutout_center_y - cutout_width/2 + 2), # Corner
        (cutout_center_x + cutout_length/2 - 2, cutout_center_y - cutout_width/2 + 2), # Corner
    ]
    
rods = (
    cq.Workplane("XY")
    .workplane(offset=rod_base_z)
    .pushPoints(local_rod_pts)
    .circle(rod_diameter/2)
    .extrude(rod_height)
)

# 5. Create the side notches
# These are on the top edge of the long face opposite the cutout side (or adjacent).
# Looking at image: Cutout is back-left. Notches are on front-right long edge.
# Let's put them on the +Y face top edge.

notch_y_pos = -block_width/2
notch_z_pos = block_height/2

notches = (
    main_block_cut
    .faces(">Y")
    .workplane(centerOption="CenterOfMass")
    .center(block_length/4, block_height/2) # Move to top right area of the face
    .pushPoints([(-notch_spacing/2, 0), (notch_spacing/2, 0)]) # Relative to new center
    .rect(notch_width, notch_depth * 2) # *2 depth because we are centered on edge
    .cutBlind(-notch_depth * 2) # Cut into the block
)

# 6. Combine everything
result = notches.union(plate).union(rods)