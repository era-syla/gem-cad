import cadquery as cq

# Define parametric dimensions for the washer
outer_diameter = 30.0  # Overall diameter of the washer
hole_diameter = 10.0   # Diameter of the central hole
thickness = 2.5        # Thickness of the washer

# Create the washer geometry
# 1. Start a workplane (XY plane is standard)
# 2. Draw the outer circle
# 3. Draw the inner circle (for the hole)
# 4. Extrude the sketch to create the 3D solid
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(hole_diameter / 2)
    .extrude(thickness)
)

# Alternatively, a more explicit subtraction method:
# result = (
#     cq.Workplane("XY")
#     .circle(outer_diameter / 2)
#     .extrude(thickness)
#     .faces(">Z")
#     .workplane()
#     .hole(hole_diameter)
# )