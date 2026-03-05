import cadquery as cq

# Parametric dimensions
length = 50.0       # Total length of the spacer/tube
outer_diameter = 15.0  # Outer diameter of the cylinder
inner_diameter = 6.0   # Diameter of the through-hole

# Create the geometry
# Start with a workplane (XY plane)
# Draw the outer circle and extrude it to create the solid cylinder
# Then cut the inner hole through it
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .extrude(length)
    .faces(">Z")
    .workplane()
    .hole(inner_diameter)
)

# Alternatively, a more direct subtraction approach:
# result = (
#     cq.Workplane("XY")
#     .circle(outer_diameter / 2.0)
#     .circle(inner_diameter / 2.0)
#     .extrude(length)
# )

# The first method is often more robust for adding features later, 
# but for a simple tube, the second commented-out method works well too.
# I will use the first method as it creates a solid cylinder first then drills, 
# which mimics manufacturing.