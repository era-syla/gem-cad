import cadquery as cq

# --- Parameters ---
# Dimensions are estimated based on visual proportions
post_height = 200.0    # Total height of the vertical posts
post_width = 10.0      # Width of the square post
post_depth = 10.0      # Depth of the square post
post_spacing = 150.0   # Center-to-center distance between the two posts

rail_diameter = 3.0    # Diameter of the horizontal rails
rail_count = 14        # Number of horizontal rails
rail_gap = 12.0        # Vertical center-to-center spacing between rails

# Calculate offsets to center the rail assembly vertically relative to the posts
rail_assembly_height = (rail_count - 1) * rail_gap
rail_start_height = (post_height - rail_assembly_height) / 2.0

# Middle support rod parameters (the thin vertical line in the center)
support_rod_dia = 2.0

# --- Modeling ---

# 1. Create the Left Post
# We create a box centered on XY, sitting on Z=0, then move it to the left
left_post = (
    cq.Workplane("XY")
    .box(post_width, post_depth, post_height, centered=(True, True, False))
    .translate((-post_spacing / 2, 0, 0))
)

# 2. Create the Right Post
# Similar to the left post, moved to the right
right_post = (
    cq.Workplane("XY")
    .box(post_width, post_depth, post_height, centered=(True, True, False))
    .translate((post_spacing / 2, 0, 0))
)

# 3. Create the Horizontal Rails
# We will create one cylinder and then use a loop to unite them
# Alternatively, we can use points to place them all at once.

# Generate the center points for the rails on the YZ plane (relative to a side view)
# But creating cylinders along X is easier.
rail_points = []
for i in range(rail_count):
    z_pos = rail_start_height + (i * rail_gap)
    # Points are (x, y, z). We want them centered on X=0, Y=0
    rail_points.append((0, 0, z_pos))

# Create the rails
# Use a cylinder along the X-axis. Length is post_spacing minus a bit to sit inside, 
# or just full post_spacing and let boolean union handle overlap.
# Let's make them span exactly between the centers of the posts for simplicity, 
# or slightly longer to ensure full intersection.
rail_length = post_spacing 

rails = (
    cq.Workplane("YZ")
    .pushPoints([(0, z) for x, y, z in rail_points]) # Use 2D points on YZ plane
    .circle(rail_diameter / 2)
    .extrude(rail_length, both=True) # Extrude along X from center
)

# 4. Create the Vertical Support Rod (Middle)
# This is the thin vertical line seen intersecting the rails in the middle
support_rod = (
    cq.Workplane("XY")
    .circle(support_rod_dia / 2)
    .extrude(post_height - (rail_start_height/2)) # Height roughly matching top rail area
    .translate((0, 0, rail_start_height/2)) # Lift it up slightly
)

# 5. Combine everything
result = left_post.union(right_post).union(rails).union(support_rod)

# Optional: If you want to export or visualize
if 'show_object' in globals():
    show_object(result)