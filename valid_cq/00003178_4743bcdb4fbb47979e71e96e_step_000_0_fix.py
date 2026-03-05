import cadquery as cq

# Create a D-shaped profile (rectangle with one semicircular end)
# The shape is a rectangle with a semicircle on one end, extruded to a height

width = 60   # full width
length = 80  # total length
height = 15  # extrusion height
radius = width / 2  # semicircle radius = half of width

# Build the 2D profile using a wire
# The flat end is on the right, the semicircular end is on the left
result = (
    cq.Workplane("XY")
    .moveTo(0, -width/2)
    .lineTo(length - radius, -width/2)
    .threePointArc((length - radius + radius, 0), (length - radius, width/2))
    .lineTo(0, width/2)
    .close()
    .extrude(height)
)