import cadquery as cq

# Parameters for the dowel pin
pin_diameter = 6.0    # Diameter of the pin
pin_length = 40.0     # Total length of the pin
chamfer_size = 0.5    # Size of the chamfer on the ends

# Create the main cylinder
pin = cq.Workplane("XY").circle(pin_diameter / 2).extrude(pin_length)

# Apply chamfers to both ends
# We select the circular edges at Z=0 and Z=pin_length
result = pin.edges("%CIRCLE").chamfer(chamfer_size)