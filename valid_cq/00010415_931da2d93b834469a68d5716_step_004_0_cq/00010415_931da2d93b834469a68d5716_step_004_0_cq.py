import cadquery as cq

# Parametric dimensions
# Since the image is just a thin straight rod, we define reasonable defaults
# but keep them parametric for easy adjustment.
rod_length = 100.0  # Total length of the rod
rod_diameter = 1.0  # Diameter of the rod (thin compared to length)

# Create the rod using the Workplane and circle/extrude workflow
# Alternatively, cq.Solid.makeCylinder could be used, but Workplane is more idiomatic
result = (
    cq.Workplane("XY")
    .circle(rod_diameter / 2.0)
    .extrude(rod_length)
)

# Export or visualization would happen here in a real script
# The requirements ask for a 'result' variable containing the geometry