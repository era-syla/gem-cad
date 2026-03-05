import cadquery as cq

# Parameters
length = 60
width = 30
height = 15
radius = width / 2  # semicircular ends
hole_diameter = 12
hole_offset_x = 20  # offset from center toward right end

# Create the oblong/stadium shape (rectangle with semicircular ends)
result = (
    cq.Workplane("XY")
    .moveTo(-length/2 + radius, 0)
    .lineTo(length/2 - radius, 0)
    .threePointArc((length/2, radius, 0), (length/2 - radius, 2*radius, 0))
    .lineTo(-length/2 + radius, 2*radius)
    .threePointArc((-length/2, radius, 0), (-length/2 + radius, 0, 0))
    .close()
    .extrude(height)
)

# Add hole on the right side
result = (
    result
    .faces(">Z")
    .workplane()
    .center(length/2 - radius, radius)
    .circle(hole_diameter / 2)
    .cutThruAll()
)