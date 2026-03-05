import cadquery as cq

# Parameters
taper_length = 80
small_width = 2
big_width = 10
thickness = 3
hole_size = 4
radius = big_width / 2

# Build the profile and extrude
result = (
    cq.Workplane("XY")
    .moveTo(0, small_width/2)
    .lineTo(taper_length, big_width/2)
    .radiusArc((taper_length, -big_width/2), radius)
    .lineTo(0, -small_width/2)
    .close()
    .extrude(thickness)
    # Cut the square hole at the rounded end
    .faces(">Z")
    .workplane()
    .center(taper_length + radius, 0)
    .rect(hole_size, hole_size)
    .cutThruAll()
)