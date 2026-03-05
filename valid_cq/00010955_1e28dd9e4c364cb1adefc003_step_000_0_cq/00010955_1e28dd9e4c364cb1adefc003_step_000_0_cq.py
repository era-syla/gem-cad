import cadquery as cq

# Parametric dimensions
# Total length appears to be split by the collar
shaft_long_length = 40.0
shaft_long_diameter = 4.0

collar_length = 5.0
collar_diameter = 8.0

shaft_short_length = 25.0
shaft_short_diameter = 2.5  # Slightly thinner than the long shaft

# Create the long shaft section
long_shaft = cq.Workplane("XY").circle(shaft_long_diameter / 2).extrude(shaft_long_length)

# Create the collar section on top of the long shaft
# We select the top face (positive Z) of the current solid to continue drawing
collar = (
    long_shaft.faces(">Z")
    .workplane()
    .circle(collar_diameter / 2)
    .extrude(collar_length)
)

# Create the short/thin shaft section on top of the collar
result = (
    collar.faces(">Z")
    .workplane()
    .circle(shaft_short_diameter / 2)
    .extrude(shaft_short_length)
)

# Optional: Adding fillets if visible, though the image is quite simple.
# The image shows sharp transitions, but possibly a very small chamfer at the ends.
# Let's keep it simple as sharp edges for accuracy to the basic shape.

# Export or display the result (in a real environment this variable is used)
# show_object(result)