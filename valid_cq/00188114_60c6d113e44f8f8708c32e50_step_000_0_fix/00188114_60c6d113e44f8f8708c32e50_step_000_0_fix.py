import cadquery as cq

# Define the 2D path for the tube centerline
start = (50, 0)
path_points = [(15, 40), (-30, 20), (-25, -30), (40, -20)]
path = cq.Workplane("XY")\
    .moveTo(start[0], start[1])\
    .spline(path_points)\
    .val()

# Parameters for tube
outer_radius = 5
wall_thickness = 1
inner_radius = outer_radius - wall_thickness

# Sweep an outer circle along the path
outer_tube = cq.Workplane("XY")\
    .transformed(offset=(start[0], start[1], 0))\
    .circle(outer_radius)\
    .sweep(path, isFrenet=True)

# Sweep an inner circle along the same path to hollow out
inner_tube = cq.Workplane("XY")\
    .transformed(offset=(start[0], start[1], 0))\
    .circle(inner_radius)\
    .sweep(path, isFrenet=True)

# Subtract inner from outer to get a hollow tube
result = outer_tube.cut(inner_tube)