import cadquery as cq

# Define parameters for the cylindrical pin
# These dimensions are estimates based on visual proportions
pin_diameter = 5.0
pin_length = 50.0
chamfer_size = 0.25

# Create the main cylinder
result = (
    cq.Workplane("XY")
    .circle(pin_diameter / 2)
    .extrude(pin_length)
)

# Apply chamfers to both ends for a realistic look
# Selecting edges at the top (Z=length) and bottom (Z=0)
result = (
    result.faces(">Z or <Z")
    .edges()
    .chamfer(chamfer_size)
)