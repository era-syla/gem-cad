import cadquery as cq

# Parametric dimensions
plate_width = 50.0
plate_height = 90.0
plate_thickness = 4.0
post_height = 15.0
post_outer_diameter = 12.0
post_inner_diameter = 7.0

# The corner radius of the plate matches the outer radius of the posts
# to ensure the posts align flush with the rounded corners.
corner_radius = post_outer_diameter / 2.0

# Calculate offsets for the post centers relative to the origin
# Inset by the radius so the outer edge of the post touches the bounding box
x_offset = (plate_width / 2.0) - corner_radius
y_offset = (plate_height / 2.0) - corner_radius

post_centers = [
    (x_offset, y_offset),
    (x_offset, -y_offset),
    (-x_offset, y_offset),
    (-x_offset, -y_offset)
]

# 1. Create the Base Plate
# Start with a simple box centered on the XY plane
result = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# Fillet the four vertical corners
result = result.edges("|Z").fillet(corner_radius)

# 2. Add the Cylindrical Posts
# Select the top face of the plate to start the extrusion
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(post_centers)
    .circle(post_outer_diameter / 2.0)
    .extrude(post_height)
)

# 3. Create the Through Holes
# Select the top face of the new posts
# Create circles and cut through the entire part (posts and base)
result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(post_centers)
    .circle(post_inner_diameter / 2.0)
    .cutThruAll()
)