import cadquery as cq

# Parametric dimensions
height = 50.0      # Total height of the tube
outer_diameter = 50.0 # Outside diameter of the tube
wall_thickness = 5.0  # Thickness of the tube wall

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the hollow cylinder
# Method: Sketch two circles and extrude
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(height)
)

# Alternative method (often cleaner for simple tubes):
# result = cq.Workplane("XY").tube(outer_radius, inner_radius, height)