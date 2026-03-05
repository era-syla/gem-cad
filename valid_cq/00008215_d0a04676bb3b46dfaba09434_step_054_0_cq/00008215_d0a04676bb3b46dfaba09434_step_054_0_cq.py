import cadquery as cq

# Parameters for the washer
outer_diameter = 30.0  # Diameter of the washer
inner_diameter = 13.0  # Diameter of the hole
thickness = 3.0        # Thickness of the washer

# Create the washer geometry
# 1. Start with a sketch on the XY plane
# 2. Draw the outer circle
# 3. Draw the inner circle to create the hole
# 4. Extrude to the desired thickness
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(thickness)
)

# Alternatively, using cylinder and hole operations:
# result = (
#     cq.Workplane("XY")
#     .cylinder(thickness, outer_diameter / 2)
#     .faces(">Z")
#     .hole(inner_diameter)
# )