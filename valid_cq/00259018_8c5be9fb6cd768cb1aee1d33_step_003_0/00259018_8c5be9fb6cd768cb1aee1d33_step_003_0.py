import cadquery as cq

# Parametric dimensions
body_diameter = 12.0  # Diameter of the upper, thicker section
body_length = 35.0    # Length of the upper section
pin_diameter = 6.0    # Diameter of the lower, thinner section
pin_length = 15.0     # Length of the lower section
fillet_radius = 1.5   # Radius of the fillet on the top edge

# Create the model
result = (
    cq.Workplane("XY")
    # Create the bottom pin section
    .circle(pin_diameter / 2.0)
    .extrude(pin_length)
    # Select the top face of the pin to start the body
    .faces(">Z")
    .workplane()
    # Create the main body section
    .circle(body_diameter / 2.0)
    .extrude(body_length)
    # Select the top edge and apply fillet
    .edges(">Z")
    .fillet(fillet_radius)
)