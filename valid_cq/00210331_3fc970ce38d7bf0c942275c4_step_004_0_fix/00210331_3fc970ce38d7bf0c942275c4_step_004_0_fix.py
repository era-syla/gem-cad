import cadquery as cq

# Parameters
t = 2              # material thickness
back_width = 40    # width of back plate
back_height = 50   # height of back plate
shelf_depth = 30   # depth of shelf

# Back plate
back = cq.Workplane("XZ").rect(back_width, back_height).extrude(t)

# Shelf plate
shelf = cq.Workplane("XY") \
    .box(back_width, shelf_depth, t) \
    .translate((0, t + shelf_depth/2, back_height + t/2))

# Front guard plate at shelf outer end
guard = cq.Workplane("XY") \
    .box(t, shelf_depth, back_height) \
    .translate((-back_width/2 + t/2, t + shelf_depth/2, back_height/2))

# Triangular gusset on the right side
gusset = (
    cq.Workplane("YZ")
    .transformed(offset=(back_width/2 - t, 0, 0))
    .polyline([
        (t, 0),
        (t, back_height),
        (t + shelf_depth, back_height)
    ])
    .close()
    .extrude(t)
)

# Combine all parts
result = back.union(shelf).union(guard).union(gusset)