import cadquery as cq

# Define dimensions
length = 100
width = 20
thickness = 1.5
circle_dia = 5
hole_dia = 3
end_pad_dia = 15

# Create the main body
result = (cq.Workplane("XY")
    .rect(length, width)
    .extrude(thickness)
    # Add end pads
    .faces(">Z").workplane()
    .center(length/2, 0)
    .circle(end_pad_dia/2)
    .extrude(thickness)
    .center(-length, 0)
    .circle(end_pad_dia/2)
    .extrude(thickness)
    # Cut main holes
    .faces(">Z").workplane()
    .center(length/2, 0)
    .circle(circle_dia/2)
    .cutThruAll()
    .center(-length, 0)
    .circle(circle_dia/2)
    .cutThruAll()
    # Cut small holes
    .center(length/4, width/4)
    .circle(hole_dia/2)
    .cutThruAll()
    .center(0, -width/2)
    .circle(hole_dia/2)
    .cutThruAll()
    .center(-length/2, 0)
    .circle(hole_dia/2)
    .cutThruAll()
    .center(0, width/2)
    .circle(hole_dia/2)
    .cutThruAll()
)