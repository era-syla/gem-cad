import cadquery as cq

# Parametric dimensions
height = 50.0          # Total length of the tube
outer_diameter = 10.0  # Outer diameter
wall_thickness = 1.5   # Thickness of the tube wall

# Calculate inner diameter
inner_diameter = outer_diameter - (2 * wall_thickness)

# Generate the hollow cylinder geometry
# 1. Create a workplane on XY
# 2. Draw the outer circle
# 3. Draw the inner circle
# 4. Extrude the region between the two circles to create a tube
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(height)
)