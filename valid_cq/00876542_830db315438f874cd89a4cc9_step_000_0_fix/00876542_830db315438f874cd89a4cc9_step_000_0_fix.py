import cadquery as cq

# Parameters
base_x = 20
base_y = 30
base_z = 40

flange_thickness = 5
flange_height = 10

slab_x = 20
slab_y = 20
slab_z = 5

cyl1_r = 4
cyl1_h = 5
cyl2_r = 3
cyl2_h = 5

handle_width = 2
handle_length = 20
handle_thickness = 2

# Build base
result = cq.Workplane("XY").box(base_x, base_y, base_z)

# Add side flanges
for s in [1, -1]:
    result = result.union(
        cq.Workplane("XY")
        .transformed(offset=(s * (base_x/2 + flange_thickness/2), 0, flange_height/2))
        .box(flange_thickness, base_y, flange_height)
    )

# Cut U-shaped slots in flanges (half through)
for s in [1, -1]:
    result = result.cut(
        cq.Workplane("XY")
        .transformed(offset=(s * (base_x/2 + flange_thickness/2), 0, flange_height/2))
        .circle(2.5)
        .extrude(flange_thickness + 1)
    )

# Top slab
result = result.union(
    cq.Workplane("XY")
    .transformed(offset=(0, 0, base_z + slab_z/2))
    .box(slab_x, slab_y, slab_z)
)

# Front cylinder posts
front_y = slab_y / 2
cyl1 = (
    cq.Workplane("XY")
    .transformed(offset=(0, front_y, base_z + slab_z))
    .circle(cyl1_r)
    .extrude(cyl1_h)
)
cyl2 = (
    cq.Workplane("XY")
    .transformed(offset=(0, front_y, base_z + slab_z + cyl1_h))
    .circle(cyl2_r)
    .extrude(cyl2_h)
)
result = result.union(cyl1).union(cyl2)

# Handle on top
handle = (
    cq.Workplane("XY")
    .transformed(
        offset=(0, front_y + handle_length/2, base_z + slab_z + cyl1_h + cyl2_h)
    )
    .ellipse(handle_width/2, handle_length/2)
    .extrude(handle_thickness)
)
result = result.union(handle)