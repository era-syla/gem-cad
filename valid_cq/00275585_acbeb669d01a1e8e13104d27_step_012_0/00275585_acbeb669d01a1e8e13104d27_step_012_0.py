import cadquery as cq

# Parameters
body_width = 40.0
body_length = 60.0
straight_height = 20.0  # Height of the vertical straight sides
pin_diameter = 12.0
pin_length = 15.0

# Derived dimensions
radius = body_width / 2.0
total_height = straight_height + radius

# Generate the 3D model
result = (
    cq.Workplane("XZ")
    # Draw the base profile (U-shape / Tombstone shape)
    .moveTo(-body_width / 2.0, 0)
    .lineTo(body_width / 2.0, 0)
    .lineTo(body_width / 2.0, straight_height)
    # Create the top semi-circle
    # threePointArc args: (point_on_arc, end_point)
    .threePointArc((0, straight_height + radius), (-body_width / 2.0, straight_height))
    .close()
    .extrude(body_length)
    
    # Select the back face (minimum Y coordinate) to attach the pin
    .faces("<Y")
    .workplane(centerOption="ProjectedOrigin")
    
    # Move the center to the center of the arc (which is at Z = straight_height)
    .center(0, straight_height)
    
    # Create the pin
    .circle(pin_diameter / 2.0)
    .extrude(pin_length)
)