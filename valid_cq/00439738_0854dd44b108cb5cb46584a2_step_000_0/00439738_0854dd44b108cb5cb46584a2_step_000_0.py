import cadquery as cq

# Geometric parameters estimated from the image
main_diameter = 25.0
main_length = 100.0
pin_diameter = 6.0
pin_length_from_center = 50.0

# Create the main horizontal cylinder
# Oriented along the X-axis (extruding from YZ plane)
# Centered at the origin using both=True
main_body = (
    cq.Workplane("YZ")
    .circle(main_diameter / 2.0)
    .extrude(main_length / 2.0, both=True)
)

# Create the perpendicular pin
# Oriented along the Y-axis (extruding from XZ plane)
# Starts from the center and extends outwards
pin = (
    cq.Workplane("XZ")
    .circle(pin_diameter / 2.0)
    .extrude(pin_length_from_center)
)

# Combine the two solids
result = main_body.union(pin)