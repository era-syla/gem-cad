import cadquery as cq

# Parametric dimensions
# Main vertical L-plate dimensions
v_plate_height = 100.0
v_plate_width_1 = 80.0  # Left wing width
v_plate_width_2 = 40.0  # Right wing width
v_plate_thickness = 2.0

# Top horizontal block dimensions
top_block_length = 80.0
top_block_width = 50.0
top_block_thickness = 15.0

# Side block dimensions
side_block_height = 40.0
side_block_width = 15.0
side_block_thickness = 40.0 # Length along the other axis

# Angled chute/bracket dimensions
chute_base_depth = 25.0 # How far it sticks out
chute_width = 25.0
chute_wall_thickness = 2.0
chute_front_height = 10.0
chute_back_height = 40.0

# 1. Create the Vertical L-shaped Plate
# We'll model this as two perpendicular plates joined at a corner.
# Plate 1 (The large face visible on the left)
plate1 = cq.Workplane("XZ").box(v_plate_width_1, v_plate_height, v_plate_thickness) \
    .translate((-v_plate_width_1/2, v_plate_height/2, 0))

# Plate 2 (The perpendicular face)
plate2 = cq.Workplane("YZ").box(v_plate_thickness, v_plate_height, v_plate_width_2) \
    .translate((0, v_plate_height/2, v_plate_width_2/2))

# Combine to form the L-corner
l_plate = plate1.union(plate2)

# 2. Create the Top Horizontal Block
# It sits on top of the left wing of the L-plate.
top_block = cq.Workplane("XY").box(top_block_length, top_block_width, top_block_thickness) \
    .translate((-top_block_length/2 + v_plate_thickness/2, 
                -top_block_width/2 + v_plate_thickness/2, 
                v_plate_height + top_block_thickness/2))

# 3. Create the Side Block
# It attaches to the right wing of the L-plate, near the top.
side_block = cq.Workplane("YZ").box(side_block_thickness, side_block_height, side_block_width) \
    .translate((side_block_width/2 + v_plate_thickness/2, 
                v_plate_height - side_block_height/2, 
                side_block_thickness/2 + v_plate_width_2/2)) # Adjusted Z to align with end

# 4. Create the Angled Chute/Bracket feature
# This is a U-shaped profile with angled side walls.
# We will create a profile and extrude it, then subtract the inner volume.

# Local coordinates for the chute placement:
# It's attached to Plate 1, near the corner.
chute_x_pos = -chute_width/2 - v_plate_thickness/2 # Centered relative to its own width, shifted left
chute_y_pos = v_plate_height - chute_back_height/2 # Near top
chute_z_pos = chute_base_depth/2 + v_plate_thickness/2

# Basic block for the chute body
chute_solid_block = cq.Workplane("XY") \
    .box(chute_width, chute_base_depth, chute_back_height) \
    .translate((chute_x_pos, chute_z_pos, chute_y_pos))

# Create the cutting tool for the angled top
# We define a wedge or simply cut with a plane. Let's create a cutting shape.
cut_angle_shape = cq.Workplane("YZ") \
    .lineTo(0, chute_back_height) \
    .lineTo(chute_base_depth, chute_front_height) \
    .lineTo(chute_base_depth, chute_back_height) \
    .close() \
    .extrude(chute_width + 10) \
    .translate((chute_x_pos - (chute_width + 10)/2, 
                v_plate_thickness/2, 
                v_plate_height - chute_back_height))

# Create the inner pocket for the chute (shelling effect)
inner_pocket = cq.Workplane("XY") \
    .box(chute_width - 2*chute_wall_thickness, 
         chute_base_depth - chute_wall_thickness, 
         chute_back_height) \
    .translate((chute_x_pos, 
                chute_z_pos + chute_wall_thickness/2, 
                chute_y_pos + chute_wall_thickness)) # Shift up slightly so bottom remains

# Form the basic chute shape
chute = chute_solid_block.cut(cut_angle_shape)
chute = chute.cut(inner_pocket)

# 5. Assemble all parts
result = l_plate.union(top_block).union(side_block).union(chute)

# Final orientation adjustment to match the isometric view in the image
# The image shows Z up, Y right, X left-ish.
# Our construction: Z up, X left (-X), Y back (+Y). 
# Rotating to match view better if exported.
result = result.rotate((0,0,0), (0,0,1), 90)