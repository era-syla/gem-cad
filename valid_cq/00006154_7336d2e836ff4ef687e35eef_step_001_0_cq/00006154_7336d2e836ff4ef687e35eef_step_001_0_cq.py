import cadquery as cq

# Parameters
plate_width = 100.0   # Width of the square plate
plate_length = 100.0  # Length of the square plate
plate_thickness = 10.0 # Thickness of the plate
pin_diameter = 10.0   # Diameter of the protruding pin
pin_length = 20.0     # Length of the pin protrusion

# Create the main plate
# We center the plate on X and Y, but sit it on the Z=0 plane (or centered on Z depending on preference)
# Let's center it on all axes for simplicity of calculating the pin position.
plate = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# Create the pin
# The pin protrudes from one of the side faces.
# Let's place it on the face at +X.
# Center of that face is (plate_length/2, 0, 0)
# Normal is along +X axis.
pin = (
    cq.Workplane("YZ")
    .workplane(offset=plate_length / 2) # Move workplane to the +X face
    .circle(pin_diameter / 2)
    .extrude(pin_length)
)

# Combine the plate and the pin
result = plate.union(pin)

# Export or visualize (optional but good practice in context)
# show_object(result)