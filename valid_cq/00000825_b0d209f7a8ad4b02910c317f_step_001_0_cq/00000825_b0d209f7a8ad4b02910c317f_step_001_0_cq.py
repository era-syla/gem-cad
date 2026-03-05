import cadquery as cq

# Parametric dimensions
# Bottom cylinder (base) dimensions
base_diameter = 10.0
base_height = 20.0

# Top cylinder (shaft) dimensions
shaft_diameter = 5.0
shaft_height = 30.0

# Create the base cylinder
# We start by drawing a circle on the XY plane and extruding it
base = cq.Workplane("XY").circle(base_diameter / 2).extrude(base_height)

# Create the shaft cylinder
# We select the top face of the base cylinder to start the next feature
# Then we draw a smaller circle and extrude it upwards
result = (
    base
    .faces(">Z")
    .workplane()
    .circle(shaft_diameter / 2)
    .extrude(shaft_height)
)

# Alternatively, using a single chain of operations:
# result = (
#     cq.Workplane("XY")
#     .circle(base_diameter / 2)
#     .extrude(base_height)
#     .faces(">Z")
#     .workplane()
#     .circle(shaft_diameter / 2)
#     .extrude(shaft_height)
# )