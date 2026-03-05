import cadquery as cq

# --- Parametric Dimensions ---
length = 200.0          # Total length of the part
width = 30.0            # Total width of the U-channel shape
base_thickness = 4.0    # Thickness of the bottom base
wall_thickness = 4.0    # Thickness of the side walls

# Dimensions for the tapered/stepped left wall
left_wall_start_h = 20.0  # Height at the tall end (left side in image)
left_wall_end_h = 5.0     # Height at the short end (left side in image)

# Dimensions for the right wall (seems more uniform but has a cutout)
right_wall_h = 15.0       # Base height of the right wall
right_wall_cutout_depth = 5.0 # Depth of the cutout section

# Step parameters for the left wall
num_steps = 4
step_length = length / num_steps

# --- Modeling ---

# 1. Base Plate
# Create the base rectangle
base = cq.Workplane("XY").box(length, width, base_thickness)

# 2. Right Wall (Uniform height for now)
# Positioned at +Y edge
right_wall = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness/2)
    .center(0, width/2 - wall_thickness/2)
    .box(length, wall_thickness, right_wall_h, centered=(True, True, False))
)

# 3. Left Wall (Stepped and Tapered)
# This is the complex part. It looks like a wedge shape with steps cut out of it, 
# or a series of blocks of decreasing height.
# Looking at the image, the left wall has a continuous slope on the bottom edge? 
# No, the bottom is flat. The top edge is stepped.
# Let's model it as a series of blocks.

left_wall_parts = []
# Calculate step height drop per step to go from start_h to end_h
height_drop = (left_wall_start_h - left_wall_end_h) / (num_steps - 1)

current_x = -length/2 + step_length/2
current_h = left_wall_start_h

for i in range(num_steps):
    # Each step is a block
    step = (
        cq.Workplane("XY")
        .workplane(offset=base_thickness/2)
        .center(current_x, -width/2 + wall_thickness/2)
        .box(step_length, wall_thickness, current_h, centered=(True, True, False))
    )
    left_wall_parts.append(step)
    
    current_x += step_length
    current_h -= height_drop

# Combine base and walls
result = base.union(right_wall)
for part in left_wall_parts:
    result = result.union(part)

# 4. Refinement: Tapered cut on the right wall?
# The image shows the right wall (the one in the foreground on the right) is a simple rectangular prism wall.
# The left wall (foreground left) is the stepped one.
# Wait, let's re-orient based on the image.
# The image shows a long object.
# The front-most face is a long wall that tapers down from left to right.
# Behind it, there are "steps". This implies the front wall is TAPERED, and the back structure is stepped.
# actually, looking closer at the "steps":
# It looks like there are multiple internal ribs or a thick stepped wall BEHIND a thin tapered front wall.
# OR, it is a U-channel where one wall is tapered and the OTHER wall is stepped.

# Let's re-examine the geometry.
# It looks like a U-channel.
# The wall facing the viewer (Front Wall) starts tall on the left and tapers down to the right.
# The wall in the back (Back Wall) seems to be stepped.
# Or vice versa. Let's assume standard isometric view conventions.
# - The wall closest to us (bottom-left of image) is a solid, smooth, tapered wall.
# - The wall further away (top-left of image) appears to have steps on its top edge.
# - There is a base connecting them.

# Revised Strategy:
# 1. Create a Base.
# 2. Create the Front Wall (Tapered).
# 3. Create the Back Wall (Stepped).

# --- Revised Parameters ---
length = 100.0
width = 20.0
base_thick = 2.0
wall_thick = 2.0

# Front Wall (Tapered)
fw_height_start = 15.0
fw_height_end = 5.0

# Back Wall (Stepped)
bw_height_start = 12.0
bw_height_end = 4.0
bw_steps = 4

# --- Revised Modeling Code ---

# 1. Base
result = cq.Workplane("XY").box(length, width, base_thick)

# 2. Front Wall (The smooth tapered one)
# We will sketch the side profile on the XZ plane and extrude it in Y.
# The wall is located at -Y side of the base.

# Define the points for the tapered trapezoid
fw_pts = [
    (-length/2, 0),                 # Bottom Left
    (length/2, 0),                  # Bottom Right
    (length/2, fw_height_end),      # Top Right
    (-length/2, fw_height_start)    # Top Left
]

front_wall = (
    cq.Workplane("XZ")
    .workplane(offset=-width/2)  # Shift to the front edge
    .polyline(fw_pts)
    .close()
    .extrude(wall_thick)
    # Move it up so it sits on top of the base geometry-wise? 
    # Usually easier to extrude from base top, but side sketch is cleaner for taper.
    # Let's adjust Z position.
    .translate((0, 0, base_thick/2)) 
)

# 3. Back Wall (The stepped one)
# Located at +Y side.
# It consists of several rectangular blocks of decreasing height.

back_wall = cq.Workplane("XY") # Placeholder

step_len = length / bw_steps
current_x = -length/2 + step_len/2
# Linear interpolation for heights
h_step = (bw_height_start - bw_height_end) / (bw_steps - 1) if bw_steps > 1 else 0
current_h = bw_height_start

for i in range(bw_steps):
    # Create a block
    # Z-origin is base_thick/2 so it sits on the base
    # Y-origin is width/2 - wall_thick/2 to align with back edge
    
    blk = (
        cq.Workplane("XY")
        .workplane(offset=base_thick/2)
        .center(current_x, width/2 - wall_thick/2)
        .box(step_len, wall_thick, current_h, centered=(True, True, False))
    )
    
    if i == 0:
        back_wall = blk
    else:
        back_wall = back_wall.union(blk)
    
    current_x += step_len
    current_h -= h_step

# Combine all
result = result.union(front_wall).union(back_wall)

# Wait, looking at the image again very carefully.
# The steps are on the *inside*? No.
# The "Front" wall in the image (the one creating the silhouette at the bottom) is the TAPERED one.
# The "Back" wall (top of image) is the STEPPED one.
# My code does exactly this.
# However, the Front Wall in the image seems to start at X=0 and end at X=Length.
# The taper goes from tall (left) to short (right).
# In the image, the left side of the object has the tall end of the tapered wall.
# The right side has the short end.
# My code matches this (left is -x, right is +x).

# Let's refine dimensions to match the proportions in the image better.
# The object is very long and narrow.
length = 150.0
width = 25.0
base_thick = 3.0
wall_thick = 3.0

# Tapered wall
fw_h_tall = 25.0
fw_h_short = 5.0

# Stepped wall
# The first step seems slightly shorter than the tall end of the tapered wall.
bw_h_start = 20.0
bw_h_end = 8.0
steps = 4
