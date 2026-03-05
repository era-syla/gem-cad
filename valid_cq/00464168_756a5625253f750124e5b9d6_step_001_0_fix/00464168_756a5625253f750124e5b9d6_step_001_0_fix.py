import cadquery as cq

# Parameters
handle_length = 80
blade_length = 40
thickness = 2
width = 8
radius = blade_length

# Build the rectangular handle
handle = cq.Workplane("YZ").box(handle_length, width, thickness)

# Build the full cylinder for the blade bottom
blade_cyl = (
    cq.Workplane("YZ")
    .transformed(offset=(handle_length/2, 0, 0))  # position at handle end
    .circle(radius)
    .extrude(blade_length)  # extrude along +X
)

# Union handle and blade cylinder
body = handle.union(blade_cyl)

# Cut away everything above the flat top plane at z = thickness
cut_top = (
    cq.Workplane("XY")
    .transformed(offset=( (handle_length/2 + blade_length/2), 0, thickness ))
    .rect(handle_length + blade_length, width)
    .extrude(radius + thickness)
)
body = body.cut(cut_top)

# Optionally, remove the rear half of the cylinder poking into the handle
# by intersecting with the handle block region (this cleans up internal faces)
body = body.intersect(
    cq.Workplane("YZ")
    .box(handle_length + blade_length, width, thickness)
)

result = body