import cadquery as cq

# --- Parametric Dimensions ---
length = 60.0       # Total length of the part
width = 15.0        # Width (depth) of the part
height = 20.0       # Height of the block
thickness = 6.0     # Wall thickness around the pipe cutouts

pipe_radius = 10.0  # Radius of the cutouts for the pipes
hole_diameter = 4.0 # Diameter of the central mounting hole

# Calculated dimensions
# Center-to-center distance approx derived from total length and radii
# Assuming symmetrical design with a central block
center_block_width = length - 4 * pipe_radius # Rough estimate, let's refine logic
# Better logic: The arc centers are usually set distances apart.
# Let's define it by the cutout centers.
cutout_offset = 15.0 # Distance from center to center of cutouts

# Refined Logic based on visual proportions:
# The part is a rectangular block with rounded outer corners and two large cylindrical cutouts.
# There is a central hole.

block_length = 60.0
block_width = 15.0
block_height = 20.0
fillet_radius = 5.0 # For the outer corners

# Cutout parameters
cutout_rad = 9.0    # Radius of the pipe holding area
cutout_spacing = 32.0 # Distance between the centers of the two cutouts
# The cutouts seem to go all the way through the height

# Central Hole parameters
center_hole_dia = 5.0

# --- Modeling ---

# 1. Create the base rectangular block
# Centered at origin for easier symmetry operations
base = cq.Workplane("XY").box(block_length, block_width, block_height)

# 2. Create the cylindrical cutouts
# We need two cylinders to subtract from the main block.
# They are spaced along the X axis.
# The cutouts are "U" shaped, meaning they break through one side (let's say -Y side).
# Looking at the image, the cutouts are on the 'front' face.

# Let's re-orient. Let's make the "L" shape profile in Z-Y plane or similar?
# No, boolean subtraction is easier.

# Cutout 1 (Left)
cutout_left = (
    cq.Workplane("XY")
    .workplane(offset=-block_height/2) # Start at bottom
    .center(-cutout_spacing/2, -block_width/2) # Move to left center, align edge
    .circle(cutout_rad)
    .extrude(block_height)
)

# Cutout 2 (Right)
cutout_right = (
    cq.Workplane("XY")
    .workplane(offset=-block_height/2)
    .center(cutout_spacing/2, -block_width/2)
    .circle(cutout_rad)
    .extrude(block_height)
)

# 3. Create the central mounting hole
# It goes through the center of the block, perpendicular to the cutouts.
# Looking at the image, the hole goes through the "thick" part between the clamps.
center_hole = (
    cq.Workplane("XY")
    .workplane(offset=-block_height/2) # Start at bottom
    .center(0, 0) # Center
    .circle(center_hole_dia / 2)
    .extrude(block_height)
)
# Wait, looking closer at the image, the hole axis is horizontal (Y-axis), 
# going through the central bridge.
# Let's correct the hole orientation.
center_hole_horizontal = (
    cq.Workplane("XZ")
    .center(0, 0) # Center of the face
    .circle(center_hole_dia / 2)
    .extrude(block_width * 2) # Make sure it goes all the way through
    .translate((0, -block_width, 0)) # Position it correctly
)


# 4. Combine operations
# Base block
part = base

# Subtract the large U-shape cutouts
# We need to shift the cutouts slightly in Y so they cut into the block 
# but leave the back wall.
# In the image, the cutout center seems aligned with the front face, making a semi-circle.
shift_y = -block_width/2 

cutout_tool = (
    cq.Workplane("XY")
    .workplane(offset=-block_height/2)
    .center(-cutout_spacing/2, shift_y)
    .circle(cutout_rad)
    .extrude(block_height)
    .center(cutout_spacing, 0) # Move to the other side
    .circle(cutout_rad)
    .extrude(block_height)
)

part = part.cut(cutout_tool)

# Subtract the central hole
# The hole is in the middle of the bridge.
part = part.faces(">Y").workplane().center(0,0).hole(center_hole_dia)


# 5. Add Fillets
# The back outer corners are rounded.
# Selecting vertical edges on the "back" (+Y) side.
part = part.edges("|Z and >Y").fillet(fillet_radius)

# The front corners of the clamp "arms" are often slightly rounded or sharp. 
# The image shows them fairly sharp, but let's add a tiny fillet for realism/safety if needed.
# Based on image, outer back corners have large radius. Front tips look sharp-ish.

# Assign to result
result = part