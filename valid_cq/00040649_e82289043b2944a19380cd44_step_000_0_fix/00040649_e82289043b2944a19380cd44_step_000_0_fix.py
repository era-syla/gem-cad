import cadquery as cq

# Parameters
length = 200
thickness = 5

# Create three orthogonal rods and union them
rod_z = cq.Workplane("XY").box(thickness, thickness, length)
rod_x = cq.Workplane("YZ").box(length, thickness, thickness)
rod_y = cq.Workplane("XZ").box(thickness, length, thickness)

result = rod_z.union(rod_x).union(rod_y)