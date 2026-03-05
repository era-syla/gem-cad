import cadquery as cq

# Parametric dimensions
frame_width = 400.0  # Overall width of the structure
frame_height = 300.0 # Height of the vertical posts
base_depth = 200.0   # Depth of the triangular support at the base
profile_size = 20.0  # Size of the square tubing (width and height)

# Derived dimensions
inner_width = frame_width - 2 * profile_size

# 1. Create the Base Rails (Left and Right)
# These are the horizontal pieces at the bottom going "into" the page
base_rail = (
    cq.Workplane("XY")
    .box(profile_size, base_depth, profile_size)
    .translate((0, base_depth / 2 - profile_size, profile_size / 2))
)

left_base = base_rail.translate((-frame_width / 2 + profile_size / 2, 0, 0))
right_base = base_rail.translate((frame_width / 2 - profile_size / 2, 0, 0))

# 2. Create the Vertical Posts (Left and Right)
# These sit at the "back" corner of the L-shape
vertical_post = (
    cq.Workplane("XY")
    .box(profile_size, profile_size, frame_height)
    .translate((0, -profile_size / 2, frame_height / 2))
)

left_post = vertical_post.translate((-frame_width / 2 + profile_size / 2, 0, 0))
right_post = vertical_post.translate((frame_width / 2 - profile_size / 2, 0, 0))

# 3. Create the Top Crossbar
# Connecting the top of the two vertical posts
top_crossbar = (
    cq.Workplane("XY")
    .box(frame_width, profile_size, profile_size)
    .translate((0, -profile_size / 2, frame_height - profile_size / 2))
)

# 4. Create the Bottom Crossbar
# Connecting the front ends of the base rails
bottom_crossbar = (
    cq.Workplane("XY")
    .box(frame_width, profile_size, profile_size)
    .translate((0, base_depth - 1.5 * profile_size, profile_size / 2))
)

# 5. Create the Diagonal Braces
# These run from the top back corner to the front bottom corner
# Calculate geometry for the diagonal
p1 = (0, -profile_size, frame_height - profile_size) # Top-back connection point (relative to side plane)
p2 = (0, base_depth - profile_size, 0)               # Bottom-front connection point

# Create a single diagonal strut
# We sketch a path and sweep, or extrude along a vector.
# Easiest here is to loft or extrude a shape, but given the angles,
# creating a box and rotating it or defining points is robust.

# Let's use a construction based on points
pts = [
    (0, 0),
    (profile_size, 0),
    (profile_size, frame_height - profile_size), # Approximate height, will need trimming or exact calc
    (0, frame_height - profile_size)
]

# Alternative approach for diagonals: Define the path vector
diag_vec = cq.Vector(0, base_depth - profile_size, -frame_height + profile_size)
diag_len = diag_vec.Length
angle = -90 + (180/3.14159) *  cq.Vector(0, 1, 0).getAngle(diag_vec) 

# Create a generic bar of correct length centered at origin
diagonal = (
    cq.Workplane("YZ")
    .box(diag_len, profile_size, profile_size)
    .rotate((1,0,0), (0,0,0), angle) # Rotate to match slope
    # Translate to midpoint position between the top-back and bottom-front logic
    .translate((0, (base_depth - profile_size)/2 - profile_size/2, (frame_height)/2))
)

# Move diagonals to correct X positions
left_diag = diagonal.translate((-frame_width/2 + profile_size/2, 0, 0))
right_diag = diagonal.translate((frame_width/2 - profile_size/2, 0, 0))

# Combine all parts
structure = (
    left_base
    .union(right_base)
    .union(left_post)
    .union(right_post)
    .union(top_crossbar)
    .union(bottom_crossbar)
    .union(left_diag)
    .union(right_diag)
)

result = structure