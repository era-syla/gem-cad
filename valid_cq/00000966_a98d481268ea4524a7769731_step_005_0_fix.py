import cadquery as cq

# Main base plate
base_length = 80
base_width = 12
base_height = 4

# Cylinder parameters
cyl_outer_r = 7
cyl_inner_r = 3.5
cyl_length = 40

# Create the base plate
base = (
    cq.Workplane("XY")
    .box(base_length, base_width, base_height)
)

# Add a thin flange/lip on bottom
flange = (
    cq.Workplane("XY")
    .box(base_length + 4, base_width + 4, 1.5)
    .translate((0, 0, -(base_height/2 + 1.5/2)))
)

base = base.union(flange)

# Create left cylinder (hollow tube) - positioned on top of base, left side
left_cyl_x = -20
cyl_y = 0
cyl_z = base_height / 2 + cyl_outer_r

left_outer = (
    cq.Workplane("YZ")
    .center(cyl_y, cyl_z)
    .circle(cyl_outer_r)
    .extrude(cyl_length)
    .translate((-cyl_length + left_cyl_x, 0, 0))
)

left_inner = (
    cq.Workplane("YZ")
    .center(cyl_y, cyl_z)
    .circle(cyl_inner_r)
    .extrude(cyl_length)
    .translate((-cyl_length + left_cyl_x, 0, 0))
)

# Create right cylinder (hollow tube) - positioned on top of base, right side
right_cyl_x = 20

right_outer = (
    cq.Workplane("YZ")
    .center(cyl_y, cyl_z)
    .circle(cyl_outer_r)
    .extrude(cyl_length)
    .translate((right_cyl_x, 0, 0))
)

right_inner = (
    cq.Workplane("YZ")
    .center(cyl_y, cyl_z)
    .circle(cyl_inner_r)
    .extrude(cyl_length)
    .translate((right_cyl_x, 0, 0))
)

# Combine: base + left tube + right tube, then subtract inner holes
result = (
    base
    .union(left_outer)
    .union(right_outer)
    .cut(left_inner)
    .cut(right_inner)
)

# Add small connector nubs between cylinders and base (optional detail)
# Small tab on top of base between the two cylinders
connector = (
    cq.Workplane("XY")
    .box(10, base_width, base_height * 0.5)
    .translate((0, 0, base_height / 2 + base_height * 0.25))
)

result = result.union(connector)