import cadquery as cq

# Geometric parameters
length = 80.0       # Total length of the object
diameter = 30.0     # Outer diameter of the cylinder
fillet_radius = 8.0 # Radius for the rounded ends

# Create the model
# 1. Start with a cylinder centered at the origin
# 2. Select the edges at the top and bottom of the cylinder
# 3. Apply a fillet to round over the ends, leaving a flat circular face
result = (
    cq.Workplane("XY")
    .cylinder(length, diameter / 2.0)
    .edges()
    .fillet(fillet_radius)
)