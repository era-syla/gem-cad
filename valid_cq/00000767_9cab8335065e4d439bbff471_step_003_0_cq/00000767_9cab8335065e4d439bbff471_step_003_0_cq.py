import cadquery as cq

# Parametric dimensions
length = 200.0  # Length of the rod
diameter = 5.0  # Diameter of the rod
radius = diameter / 2.0

# Create the cylindrical rod
# We start with a workplane (usually XY) and draw a circle, then extrude it.
result = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(length)
)

# Alternatively, using the primitive cylinder method:
# result = cq.Workplane("XY").cylinder(height=length, radius=radius)