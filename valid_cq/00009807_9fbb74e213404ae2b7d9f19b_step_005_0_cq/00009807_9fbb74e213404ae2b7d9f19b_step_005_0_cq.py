import cadquery as cq

# Define parametric dimensions
outer_diameter = 50.0  # Diameter of the outer cylinder
inner_diameter = 25.0  # Diameter of the inner hole
thickness = 15.0       # Thickness of the washer/ring

# Create the washer geometry
# Method: Draw two concentric circles on the XY plane and extrude them
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(thickness)
)

# Alternative method (boolean subtraction):
# outer_cyl = cq.Workplane("XY").circle(outer_diameter / 2).extrude(thickness)
# inner_cyl = cq.Workplane("XY").circle(inner_diameter / 2).extrude(thickness)
# result = outer_cyl.cut(inner_cyl)