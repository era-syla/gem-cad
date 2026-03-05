import cadquery as cq

# Parameters defining the shape
base_radius = 25.0       # Radius at the very bottom
max_radius = 35.0        # The bulge radius (widest point)
top_radius = 22.0        # Radius at the top rim
total_height = 50.0      # Total height of the object
bulge_height = 15.0      # Height at which the widest point occurs
wall_thickness = 3.0     # Thickness of the wall

# Create the profile for revolution
# We define points for the outer shell first
# Points: (radius, height)
p0 = (0, 0)
p1 = (base_radius, 0)
p2 = (max_radius, bulge_height) # Control point or intermediate vertex
p3 = (top_radius, total_height)
p4 = (top_radius - wall_thickness, total_height) # Inner top
p5 = (max_radius - wall_thickness, bulge_height) # Inner bulge
p6 = (base_radius - wall_thickness, wall_thickness) # Inner bottom (floor thickness)
p7 = (0, wall_thickness)

# Using a spline/loft approach is possible, but a revolution of a sketch is cleaner.
# Let's use a sketch with splines for the smooth curvature seen in the image.
# The image shows a smooth transition from base to bulge to top.

# Define the outer profile using a Spline
# We need a set of points for the outer wall and inner wall
outer_points = [
    (base_radius, 0),
    (max_radius, bulge_height),
    (top_radius, total_height)
]

inner_points = [
    (top_radius - wall_thickness, total_height),
    (max_radius - wall_thickness, bulge_height),
    (base_radius - wall_thickness, wall_thickness) # Keep floor thickness
]

# Create the solid using a sketch revolution
result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(base_radius, 0) # Bottom flat
    .spline(outer_points[1:], includeCurrent=True) # Outer curve
    .lineTo(top_radius - wall_thickness, total_height) # Top rim thickness
    .spline(inner_points[1:], includeCurrent=True) # Inner curve
    .lineTo(0, wall_thickness) # Inner floor
    .close()
    .revolve()
)