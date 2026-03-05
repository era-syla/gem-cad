import cadquery as cq

# Parametric dimensions
height = 200.0       # Total length of the tube
outer_diameter = 10.0 # Outside diameter of the tube
wall_thickness = 1.0  # Thickness of the tube wall

# Calculate inner diameter based on wall thickness
inner_diameter = outer_diameter - (2 * wall_thickness)

# Create the tube
# We create a solid cylinder first
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(height)
)

# Alternative method using cylinder and cut:
# outer_cyl = cq.Workplane("XY").cylinder(height, outer_diameter / 2)
# inner_cyl = cq.Workplane("XY").cylinder(height, inner_diameter / 2)
# result = outer_cyl.cut(inner_cyl)