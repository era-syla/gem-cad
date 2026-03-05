import cadquery as cq

# Create the main frame
top_tube = cq.Workplane("XY").workplane(offset=50).lineTo(250, 0).center(0, 0).circle(15).extrude(450)

down_tube = cq.Workplane("XY").workplane(offset=50).lineTo(150, -50).center(0, 0).circle(20).extrude(500)

seat_tube = cq.Workplane("XY").workplane(offset=400).circle(20).extrude(250)

head_tube = cq.Workplane("YZ").workplane(offset=-250).circle(22).extrude(100)

# Add the connections (gussets)
gusset = (
    cq.Workplane("XY")
    .box(60, 10, 5)
    .translate((200, 30, 100))
    .union(cq.Workplane("XY").box(50, 10, 5).translate((100, 30, 50)))
)

# Combine all parts
result = top_tube.union(down_tube).union(seat_tube).union(head_tube).union(gusset)