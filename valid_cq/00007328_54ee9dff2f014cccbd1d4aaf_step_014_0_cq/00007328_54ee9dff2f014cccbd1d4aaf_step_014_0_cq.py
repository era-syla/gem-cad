import cadquery as cq

# Parametric dimensions
height = 100.0       # Total height of the tube
outer_diameter = 10.0 # Outer diameter of the tube
wall_thickness = 1.0 # Thickness of the tube wall

# Derived dimensions
outer_radius = outer_diameter / 2.0
inner_radius = outer_radius - wall_thickness

# Create the hollow tube
# Method 1: Create a cylinder and subtract a smaller cylinder
# result = cq.Workplane("XY").cylinder(height, outer_radius).faces(">Z").hole(inner_radius * 2)

# Method 2: Create a circle, extrude it, and then shell it (or use a tube function if available in some libraries, but core CQ is simple enough)
# result = cq.Workplane("XY").circle(outer_radius).extrude(height).faces(">Z").shell(-wall_thickness)

# Method 3: 2D sketch subtraction then extrude (often robust)
result = (
    cq.Workplane("XY")
    .circle(outer_radius)       # Outer circle
    .circle(inner_radius)       # Inner circle to be subtracted
    .extrude(height)            # Extrude the resulting ring
)

# Alternative simplified method using the tube method if specifically aiming for a pipe shape
# result = cq.Workplane("XY").tube(outer_radius, inner_radius, height) # Not a standard method, stick to extrude

# Final check: The image shows a simple pipe. Method 3 is very clean.
# Let's verify the "result" variable is set.