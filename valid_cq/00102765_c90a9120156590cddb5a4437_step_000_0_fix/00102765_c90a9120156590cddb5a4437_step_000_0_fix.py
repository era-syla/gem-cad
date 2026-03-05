import cadquery as cq

# Define parameters
thickness = 2

# Create basic shape
logo_shape = cq.Workplane("XY").text("x4", fontsize=20, distance=thickness, cut=False)

# Final solid
result = logo_shape
