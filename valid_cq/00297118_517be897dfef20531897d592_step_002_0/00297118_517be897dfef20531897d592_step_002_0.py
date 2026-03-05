import cadquery as cq

# Parametric dimensions
total_length = 100.0
width = 20.0
height = 10.0

# Geometry parameters based on image analysis
cutout_radius = 12.0      # Radius of the cylindrical cut that defines the curved faces
neck_width = 6.0          # Width of the lower connecting bar
neck_height = 4.0         # Height of the lower connecting bar
boss_length = 5.0         # Length (along X) of the central tab
boss_height = 7.0         # Total height of the central tab from the bottom

# 1. Create the Main Body (Split into two by a central cut)
# Start with the bounding box of the entire part
base_block = cq.Workplane("XY").box(total_length, width, height)

# Create a cylindrical cutter to remove the material in the center
# The cutter is a vertical cylinder centered at (0,0)
cutter = cq.Workplane("XY").circle(cutout_radius).extrude(height * 2)

# Subtract the cylinder to create the two opposing concave faces
# This creates the "high" sections with the curved step-down profile
split_body = base_block.cut(cutter)

# 2. Create the Neck (The connecting bridge)
# Calculate Z-offset to align the neck with the bottom of the part
# Base block is centered at Z=0 (spanning -5 to +5), so bottom is -5
z_offset_neck = - (height / 2) + (neck_height / 2)

# The neck is a rectangular bar connecting the two halves
# Length is set to ensure it fully overlaps with the concave faces of the main body
neck_length = cutout_radius * 2.5 
neck = cq.Workplane("XY") \
    .workplane(offset=z_offset_neck) \
    .box(neck_length, neck_width, neck_height)

# 3. Create the Central Boss (The tab sticking up in the middle)
# Calculate Z-offset to align boss relative to bottom
z_offset_boss = - (height / 2) + (boss_height / 2)

boss = cq.Workplane("XY") \
    .workplane(offset=z_offset_boss) \
    .box(boss_length, neck_width, boss_height)

# 4. Combine all features into the final solid
result = split_body.union(neck).union(boss)