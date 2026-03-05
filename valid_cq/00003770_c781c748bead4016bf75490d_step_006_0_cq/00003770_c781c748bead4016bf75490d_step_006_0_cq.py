import cadquery as cq

# Parametric dimensions
wheel_outer_radius = 50.0
wheel_inner_radius = 40.0
wheel_thickness = 10.0
spoke_width = 8.0
spoke_thickness = 10.0  # Matches wheel thickness
hub_box_width = 60.0    # Width of the square protrusion
hub_box_height = 60.0   # Height of the square protrusion
hub_box_length = 80.0   # Length of the protrusion from the wheel face

# Create the main ring (wheel rim)
# We extrude a ring shape
rim = (
    cq.Workplane("XY")
    .circle(wheel_outer_radius)
    .circle(wheel_inner_radius)
    .extrude(wheel_thickness)
)

# Create the cross spokes
# Vertical spoke
vertical_spoke = (
    cq.Workplane("XY")
    .rect(spoke_width, wheel_outer_radius * 2)
    .extrude(spoke_thickness)
)

# Horizontal spoke
horizontal_spoke = (
    cq.Workplane("XY")
    .rect(wheel_outer_radius * 2, spoke_width)
    .extrude(spoke_thickness)
)

# Combine the rim and spokes to form the base wheel
# Using intersect to trim the spokes to the outer radius of the wheel
wheel_assembly = rim.union(vertical_spoke).union(horizontal_spoke)
wheel_assembly = wheel_assembly.intersect(
    cq.Workplane("XY").circle(wheel_outer_radius).extrude(wheel_thickness)
)

# Create the central square hub protrusion
# This is a simple box located at the center, protruding outwards
hub_box = (
    cq.Workplane("XY")
    .rect(hub_box_width, hub_box_height)
    .extrude(hub_box_length)
)

# Combine everything
result = wheel_assembly.union(hub_box)