import cadquery as cq

# Parameters for dimensions based on visual estimation
# The aspect ratio suggests a length roughly 3-4 times the diameter
length = 40.0
diameter = 10.0

# Generate the cylindrical geometry
result = (
    cq.Workplane("XY")
    .circle(diameter / 2.0)
    .extrude(length)
)