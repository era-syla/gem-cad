import cadquery as cq

# Parameters
base_length = 64
base_width = 20
base_thickness = 4
cyl_radius = 5
cyl_length = base_width
cyl_offset = 20
hole_radius = 2.5

# Base plate
base = cq.Workplane("XY").rect(base_length, base_width).extrude(base_thickness)

# Cylindrical bosses
boss1 = cq.Workplane("ZX", origin=(-cyl_offset, 0, base_thickness)).circle(cyl_radius).extrude(cyl_length)
boss2 = cq.Workplane("ZX", origin=( cyl_offset, 0, base_thickness)).circle(cyl_radius).extrude(cyl_length)

# Combine base and bosses
part = base.union(boss1).union(boss2)

# Through-holes in bosses
hole1 = cq.Workplane("ZX", origin=(-cyl_offset, 0, base_thickness)).circle(hole_radius).extrude(cyl_length)
hole2 = cq.Workplane("ZX", origin=( cyl_offset, 0, base_thickness)).circle(hole_radius).extrude(cyl_length)

# Subtract holes
result = part.cut(hole1).cut(hole2)