import cadquery as cq

# Parameters for the model
base_length = 120.0
base_width = 35.0
base_thickness = 8.0
post_diameter = 18.0
post_height = 60.0

# The post appears to be centered within the square region at one end of the base plate
post_x_offset = -(base_length / 2.0) + (base_width / 2.0)

# Create the geometry
result = (
    cq.Workplane("XY")
    # Create the rectangular base plate
    .box(base_length, base_width, base_thickness)
    # Select the top face to draw the cylinder
    .faces(">Z")
    .workplane()
    # Move to the position for the cylindrical post
    .center(post_x_offset, 0)
    # Draw and extrude the cylinder
    .circle(post_diameter / 2.0)
    .extrude(post_height)
)