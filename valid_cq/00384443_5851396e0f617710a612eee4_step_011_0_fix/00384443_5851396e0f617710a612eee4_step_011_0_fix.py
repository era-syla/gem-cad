import cadquery as cq

# Parameters
base_width = 20
base_depth = 6
base_height = 30
platform_depth = 12
platform_thickness = 6
rod_diameter = 3
rod_height = 15
rod_spacing = 10
pocket_width = 4
pocket_height = 8
pocket_depth = 4
pocket_offset_z = -7

# Base block
base = cq.Workplane("XY").box(base_width, base_depth, base_height)

# Top platform
platform = (
    cq.Workplane("XY")
    .box(base_width, platform_depth, platform_thickness)
    .translate((0, 0, base_height/2 + platform_thickness/2))
)

# Cylindrical rods
platform_top_z = base_height/2 + platform_thickness
rod1 = (
    cq.Workplane("XY")
    .workplane(offset=platform_top_z)
    .center(-rod_spacing/2, 0)
    .circle(rod_diameter/2)
    .extrude(rod_height)
)
rod2 = (
    cq.Workplane("XY")
    .workplane(offset=platform_top_z)
    .center(rod_spacing/2, 0)
    .circle(rod_diameter/2)
    .extrude(rod_height)
)

# Combine solids
result = base.union(platform).union(rod1).union(rod2)

# Rectangular pockets on front face
result = (
    result.faces(">Y")
    .workplane()
    .pushPoints([(-rod_spacing/2, pocket_offset_z), (rod_spacing/2, pocket_offset_z)])
    .rect(pocket_width, pocket_height)
    .cutBlind(-pocket_depth)
)