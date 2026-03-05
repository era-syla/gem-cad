import cadquery as cq

# Create the U-channel profile
channel = (
    cq.Workplane("XY")
    .vLine(10)
    .hLine(20)
    .vLine(-10)
    .close()
    .extrude(100)
)

# Add holes to the top
channel = (
    channel.faces(">Z")
    .workplane()
    .rarray(20, 20, 5, 2)
    .circle(3)
    .cutThruAll()
)

result = channel