import cadquery as cq

# Parametric dimensions for the ring
outer_diameter = 100.0
inner_diameter = 94.0  # Defines the wall thickness ( (100 - 94) / 2 = 3mm )
height = 3.0           # Thickness in the Z direction

# Create the ring geometry
# 1. Create a workplane
# 2. Sketch the outer circle
# 3. Sketch the inner circle
# 4. Extrude the area between them
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(height)
)