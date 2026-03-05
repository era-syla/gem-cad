import cadquery as cq

# Parametric dimensions
diameter = 50.0  # Diameter of the disc
thickness = 5.0  # Thickness (height) of the disc

# Create the disc geometry
# We sketch a circle on the XY plane and extrude it
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(thickness)
)

# Alternatively, a more direct method for a cylinder exists, 
# but the sketch approach is good practice.
# result = cq.Workplane("XY").cylinder(thickness, diameter / 2.0)