import cadquery as cq

# Parametric dimensions
# Base block (middle section)
base_width = 50.0
base_length = 50.0
base_height = 30.0

# Top block (upper section)
top_width = 35.0
top_length = 35.0
top_height = 10.0

# Bottom pin (lower section)
pin_diameter = 5.0
pin_height = 10.0

# Create the main base block
base = cq.Workplane("XY").box(base_length, base_width, base_height)

# Create the top block on the top face of the base
# We select the top face (>Z), create a workplane, and extrude a centered rectangle
result = (
    base.faces(">Z")
    .workplane()
    .rect(top_length, top_width)
    .extrude(top_height)
)

# Create the pin on the bottom face of the base
# We select the bottom face (<Z), create a workplane, and extrude a circle
result = (
    result.faces("<Z")
    .workplane()
    .circle(pin_diameter / 2.0)
    .extrude(pin_height)
)