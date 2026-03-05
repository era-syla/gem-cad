import cadquery as cq

# Parameters for the cylinder
radius = 5.0  # Radius of the cylinder base
height = 100.0 # Height/Length of the cylinder

# Create the cylindrical rod
# We align it along the Z-axis by extruding a circle
result = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(height)
)

# Alternatively, a simpler direct primitive can be used:
# result = cq.Solid.makeCylinder(radius, height)