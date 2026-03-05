import cadquery as cq

# Parametric dimensions
head_diameter = 20.0  # Diameter of the top flat section
head_height = 5.0     # Thickness of the head
shaft_diameter = 12.0 # Diameter of the main cylindrical body
shaft_length = 25.0   # Length of the shaft below the head

# Create the model
# We start by drawing the shaft on the XY plane and extruding it up.
# Then we select the top face of the shaft and draw/extrude the head on top of it.
# Alternatively, we can just union two cylinders. Here is the union approach for clarity.

# Create the shaft
shaft = cq.Workplane("XY").circle(shaft_diameter / 2).extrude(shaft_length)

# Create the head. 
# We offset the workplane to the top of the shaft to start the head.
head = (
    cq.Workplane("XY")
    .workplane(offset=shaft_length)
    .circle(head_diameter / 2)
    .extrude(head_height)
)

# Combine them into a single object
result = shaft.union(head)

# Alternatively, a more compact single-chain approach:
# result = (
#     cq.Workplane("XY")
#     .circle(shaft_diameter / 2).extrude(shaft_length)
#     .faces(">Z").workplane()
#     .circle(head_diameter / 2).extrude(head_height)
# )