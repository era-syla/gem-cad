import cadquery as cq

# -- Parameters --
# Main shaft dimensions
shaft_diameter = 10.0
shaft_length = 100.0

# Tip dimensions (the smaller cylinder on top)
tip_diameter = 6.0
tip_length = 5.0

# -- Modeling --

# Create the main shaft cylinder
main_shaft = cq.Workplane("XY").circle(shaft_diameter / 2.0).extrude(shaft_length)

# Create the tip on top of the main shaft
# We select the top face (>Z) of the main shaft, draw the smaller circle, and extrude
result = (
    main_shaft
    .faces(">Z")
    .workplane()
    .circle(tip_diameter / 2.0)
    .extrude(tip_length)
)

# Alternatively, one could union two simple cylinders, but the stack-and-extrude
# method above is very idiomatic for CadQuery.