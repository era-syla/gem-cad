import cadquery as cq

# Parameters
length = 200.0
bottom_width = 20.0
top_width = 30.0
height = 20.0
wall_thickness = 2.0

# Outer trapezoidal prism
outer = (
    cq.Workplane("XZ")
    .polyline([
        (-bottom_width/2, 0),
        ( bottom_width/2, 0),
        ( top_width/2, height),
        (-top_width/2, height),
    ])
    .close()
    .extrude(length)
)

# Inner cutout to form the channel
inner = (
    cq.Workplane("XZ")
    .polyline([
        (-(bottom_width/2 - wall_thickness), wall_thickness),
        ( (bottom_width/2 - wall_thickness), wall_thickness),
        ( (top_width/2 - wall_thickness), height),
        (-(top_width/2 - wall_thickness), height),
    ])
    .close()
    .extrude(length)
)

# Subtract inner from outer to create hollow channel
result = outer.cut(inner)