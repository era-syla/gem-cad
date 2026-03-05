import cadquery as cq

# Define parametric dimensions for the plate
width = 100.0
height = 80.0
thickness = 5.0

# Create the 3D model
# The image depicts a simple rectangular prism (plate) oriented vertically.
# We use the box operation on the XY plane, mapping dimensions to axes:
# x=width, y=thickness, z=height to achieve the standing orientation.
result = cq.Workplane("XY").box(width, thickness, height)