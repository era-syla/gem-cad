import cadquery as cq

# Parameters
base_r = 16.0
base_h = 6.0
rod_r = 1.0
rod_l = 150.0
sphere_r = 15.0
cyl_l = 20.0
angle = 50.0

# Create the base
base = cq.Workplane("XY").circle(base_r).extrude(base_h)

# Create the rod and its small base connector along the +Y axis
rod_connector = (
    cq.Workplane("XZ")
    .workplane(offset=base_r - 1)
    .center(0, base_h / 2)
    .circle(rod_r * 2.5)
    .extrude(3)
)
rod = (
    cq.Workplane("XZ")
    .workplane(offset=base_r)
    .center(0, base_h / 2)
    .circle(rod_r)
    .extrude(rod_l)
)
base = base.union(rod_connector).union(rod)

# Create the neck (pedestal) for the camera body
neck_h = 3.0
neck_r = 10.0
neck = cq.Workplane("XY").workplane(offset=base_h).circle(neck_r).extrude(neck_h)
base = base.union(neck)

# Create the camera body (sphere + cylinder)
body = cq.Workplane("XY").sphere(sphere_r)
body = body.union(cq.Workplane("XY").circle(sphere_r).extrude(cyl_l))

# Chamfer the front face of the camera
body = body.edges(">Z").chamfer(1.0)

# Add grooves to replicate the panel lines seen in the image
groove_front = (
    cq.Workplane("XY")
    .workplane(offset=cyl_l - 7)
    .circle(sphere_r + 1)
    .circle(sphere_r - 1)
    .extrude(0.5)
)
groove_mid = (
    cq.Workplane("XY")
    .workplane(offset=-0.25)
    .circle(sphere_r + 1)
    .circle(sphere_r - 1)
    .extrude(0.5)
)
body = body.cut(groove_front).cut(groove_mid)

# Rotate the camera body so it points upwards and opposite to the rod (-Y direction)
body = body.rotate((0, 0, 0), (1, 0, 0), angle)

# Translate the body to sit correctly on the neck
# Z offset is calculated to intersect the sphere nicely with the neck
z_offset = base_h + neck_h + 10.0
body = body.translate((0, 0, z_offset))

# Combine all parts into the final result
result = base.union(body)