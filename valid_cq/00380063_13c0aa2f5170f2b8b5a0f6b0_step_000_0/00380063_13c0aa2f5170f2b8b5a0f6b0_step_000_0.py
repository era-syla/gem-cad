import cadquery as cq

# Dimensions estimated from the image
plate_thickness = 10.0
circle_diameter = 60.0
rect_width = 35.0
rect_height = 110.0

# Create the central circular section
# We create a workplane on the XY plane, draw a circle, and extrude it
disk = cq.Workplane("XY").circle(circle_diameter / 2.0).extrude(plate_thickness)

# Create the vertical rectangular section
# We draw a rectangle centered at the origin and extrude it
bar = cq.Workplane("XY").rect(rect_width, rect_height).extrude(plate_thickness)

# Union the two solids to create the final geometry
# This merges the disk and the bar into a single object
result = disk.union(bar)