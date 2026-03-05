import cadquery as cq

# Define parametric dimensions based on visual estimation
# The object appears to be a DC motor or a solenoid
body_large_diameter = 25.0
body_large_length = 30.0

body_small_diameter = 20.0
body_small_length = 25.0

# Rear feature (hexagonal shaft or terminal block)
rear_hex_width = 6.0  # approximate distance across flats
rear_hex_length = 8.0

# Front shaft
shaft_diameter = 5.0
shaft_length = 6.0 # protruding length

# Create the main body
# Start with the larger cylinder
main_body = cq.Workplane("XY").circle(body_large_diameter / 2.0).extrude(body_large_length)

# Add the smaller cylinder on one end (let's say the -Z direction for "rear" relative to the large part)
rear_body = (
    cq.Workplane("XY")
    .workplane(offset=-body_small_length)
    .circle(body_small_diameter / 2.0)
    .extrude(body_small_length)
)

# Combine the two cylindrical body parts
motor_body = main_body.union(rear_body)

# Add the front shaft (on top of the large cylinder, +Z direction)
front_shaft = (
    motor_body.faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(shaft_length)
)

# Add the rear feature (on the back of the small cylinder, -Z direction)
# The image shows a hexagonal prism shape
rear_feature = (
    motor_body.faces("<Z")
    .workplane()
    .polygon(6, rear_hex_width * 1.15) # 1.15 factor converts flat-to-flat to corner-to-corner roughly
    .extrude(-rear_hex_length) # Extrude downwards
)

# Combine everything into the final result
result = front_shaft.union(rear_feature)

# Ensure the final object is centered nicely (optional but good practice)
result = result.translate((0, 0, (body_small_length + rear_hex_length) / 2))