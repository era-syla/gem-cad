import cadquery as cq

# Parametric dimensions
# Based on the image, the object is a simple long, thin cylinder (a rod or shaft).
# Dimensions are estimated to be proportional.
diameter = 5.0
length = 80.0

# Create the cylinder
# We create a circle on the XY plane and extrude it along the Z axis
result = cq.Workplane("XY").circle(diameter / 2.0).extrude(length)

# Alternatively, we could specific the cylinder directly, which is often cleaner:
# result = cq.Workplane("XY").cylinder(length, diameter / 2.0)
# But extruding a circle is the most fundamental constructive geometry approach.