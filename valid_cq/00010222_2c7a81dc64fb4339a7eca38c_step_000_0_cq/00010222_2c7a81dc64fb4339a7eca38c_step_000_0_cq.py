import cadquery as cq

# --- Parametric Dimensions ---
# Block dimensions
block_width = 30.0    # Width of the main face
block_height = 40.0   # Height of the main face
block_depth = 20.0    # Depth (thickness) of the block

# Main cylindrical hole dimensions
main_hole_radius = 12.0

# Top hexagonal holes dimensions
hex_hole_dist = 16.0  # Center-to-center distance between the two hex holes
hex_hole_size = 4.0   # Radius of the circumscribed circle of the hexagon (or similar sizing)
hex_hole_depth = 12.0 # Depth of the hex holes (needs to be deep enough to intersect the main hole)

# --- Geometry Construction ---

# 1. Create the main block
result = cq.Workplane("XY").box(block_width, block_height, block_depth)

# 2. Create the large cylindrical hole
# We cut through the largest face (XY plane equivalent in the box creation, which is front/back)
# The box method centers the object at (0,0,0).
# The hole goes through the "depth" dimension (Z-axis relative to the Workplane used for the hole).
result = result.faces(">Z").workplane().hole(main_hole_radius * 2)

# 3. Create the two hexagonal holes on top
# We select the top face (+Y face relative to the initial box orientation if width=X, height=Y, depth=Z)
# Wait, let's double check orientation.
# box(w, h, d) makes a box centered at origin.
# Width is usually X, Height usually Y, Depth usually Z.
# Let's align with the image:
# The large hole axis looks like it goes along the Z axis (depth).
# The hex holes are on the "Top" face. In standard CAD terms relative to a front view, this is usually +Y.

# Let's refine the orientation strategy:
# Let's say:
# X-axis: Left-Right
# Y-axis: Up-Down (Height)
# Z-axis: Front-Back (Depth)

# Re-creating with specific orientation logic to match visual
# 1. Base Block
result = cq.Workplane("XY").box(block_width, block_height, block_depth)

# 2. Main Hole (Front to Back, so along Z axis)
# The hole is centered on the face.
result = result.faces(">Z").workplane().hole(main_hole_radius * 2)

# 3. Hexagonal Holes (Top Face, so +Y face)
# We need to position two points on this face.
# The face is the XZ plane at Y = block_height/2.
top_face = result.faces(">Y").workplane()

# Calculate offsets for the two holes
offset_x = hex_hole_dist / 2

# Create the hex cuts
# polygon(n, d) creates a regular polygon with n sides and diameter d (circumscribed)
result = (
    top_face
    .pushPoints([(-offset_x, 0), (offset_x, 0)])
    .polygon(6, hex_hole_size * 2) # polygon takes diameter, not radius
    .cutBlind(-hex_hole_depth) # Cut downwards into the block
)

# If the hex holes need to go all the way to the center bore, 
# cutBlind needs to be deep enough. block_height/2 is the distance to center.
# From the image, they clearly intersect.
# We can just cut through everything downwards or to a specific depth.
# Let's ensure they intersect by cutting down by at least half the height.
# Re-applying the cut with a calculated depth to ensure intersection.
# The top face is at Y = +20. The hole center is at Y = 0.
# A cut of -10 would reach the center of the large hole.
# Let's use cutBlind(-block_height) to be safe and ensure full intersection.

result = (
    result.faces(">Y").workplane()
    .pushPoints([(-offset_x, 0), (offset_x, 0)])
    .polygon(6, hex_hole_size * 2)
    .cutBlind(-block_height / 1.5) # Cut deep enough to pierce the main bore
)