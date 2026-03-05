import cadquery as cq

# Parametric dimensions
diameter = 50.0  # Diameter of the cylinder
height = 20.0    # Thickness/Length of the cylinder

# Create the cylindrical geometry
# We can create a cylinder directly or by extruding a circle
# Using a sketch and extrude approach is often clearer for CAD workflows,
# but cq.Workplane().cylinder() is the most direct primitive operation.

# Method 1: Primitive
# result = cq.Workplane("XY").cylinder(height, diameter / 2.0)

# Method 2: Extrusion (often preferred for clarity in mechanical design)
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(height)
)

# If running in an environment that renders 'result' automatically, this is done.
# The variable 'result' contains the final geometry.