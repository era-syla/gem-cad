import cadquery as cq

# Geometric parameters
plate_length = 180.0
plate_width = 35.0
plate_thickness = 2.0

num_posts = 8
post_diameter = 6.0
post_height = 8.0

# Calculate the spacing (pitch) between posts to distribute them evenly
# Using (N+1) divisions creates equal margins at the ends
post_pitch = plate_length / (num_posts + 1)

# Generate the 3D model
result = (
    cq.Workplane("XY")
    # Create the base rectangular plate
    .box(plate_length, plate_width, plate_thickness)
    # Select the top face to place the posts
    .faces(">Z")
    .workplane()
    # Create a linear array of points centered on the plate
    # rarray params: x_spacing, y_spacing, x_count, y_count
    .rarray(post_pitch, 1, num_posts, 1)
    # Draw the post cross-section (circles) at each point
    .circle(post_diameter / 2.0)
    # Extrude the posts upwards
    .extrude(post_height)
)