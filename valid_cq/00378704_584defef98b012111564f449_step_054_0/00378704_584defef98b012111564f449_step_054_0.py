import cadquery as cq

# Parametric dimensions for the model
base_diameter = 12.0
base_height = 10.0
shaft_diameter = 7.0
long_shaft_height = 45.0
short_shaft_height = 20.0
offset_distance = 25.0  # Spacing between the two objects

# Create the first object (Tall Pin)
# Start with the cylindrical base on the XY plane
long_pin = (
    cq.Workplane("XY")
    .circle(base_diameter / 2.0)
    .extrude(base_height)
    # Select the top face of the base to draw the shaft
    .faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(long_shaft_height)
)

# Create the second object (Short Pin)
# Similar construction, but with shorter shaft height and translated position
short_pin = (
    cq.Workplane("XY")
    .circle(base_diameter / 2.0)
    .extrude(base_height)
    .faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2.0)
    .extrude(short_shaft_height)
    # Move the short pin to the right along the X axis
    .translate((offset_distance, 0, 0))
)

# Combine both separate solids into a single compound object
result = long_pin.union(short_pin)