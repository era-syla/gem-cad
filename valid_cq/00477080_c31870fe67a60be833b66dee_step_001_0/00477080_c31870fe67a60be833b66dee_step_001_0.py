import cadquery as cq

# Parametric dimensions
outer_diameter = 100.0  # Diameter of the outer circle
inner_diameter = 90.0   # Diameter of the inner hole
thickness = 5.0         # Height/thickness of the ring

# Create the ring geometry
# 1. Start a workplane
# 2. Draw the outer circle
# 3. Draw the inner circle to create the hole
# 4. Extrude the resulting 2D shape to create the 3D solid
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(thickness)
)