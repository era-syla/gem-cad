import cadquery as cq

# Parameters
blade_thickness = 8
blade_width = 20
blade_height = 80
base_depth = blade_thickness + 8   # X dimension of base
base_width = blade_width + 8       # Y dimension of base
base_height = 10

# Base block
base = cq.Workplane("XY").box(base_depth, base_width, base_height)

# Front and back shelves on base
shelf_front = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .center(0, base_width/2 - 2)
    .box(base_depth, 4, 6)
)
shelf_back = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .center(0, -base_width/2 + 2)
    .box(base_depth, 4, 4)
)

# Vertical blade
blade = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .rect(blade_thickness, blade_width)
    .extrude(blade_height)
)

# Combine base, shelves, and blade
result = base.union(shelf_front).union(shelf_back).union(blade)

# Cut a semi-cylindrical groove along the top of the blade
groove_radius = blade_thickness / 2
groove_height = blade_width + 4
groove_offset_z = base_height + blade_height - groove_radius

groove = (
    cq.Workplane("XZ")
    .workplane(offset=groove_offset_z)
    .cylinder(groove_height, groove_radius)
)
result = result.cut(groove)