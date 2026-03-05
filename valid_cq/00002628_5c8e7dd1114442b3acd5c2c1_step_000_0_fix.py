import cadquery as cq

# Build a surveying/drafting instrument - looks like a compass/alidade with a blade

# Main horizontal bar/rule
bar = (
    cq.Workplane("XY")
    .box(120, 8, 3)
)

# Pointed blade extending from left side
blade = (
    cq.Workplane("XY")
    .move(-60, 0)
    .polyline([(-60, 0), (-20, -3), (-20, 3)])
    .close()
    .extrude(3)
)

# Small block on right end of bar
right_block = (
    cq.Workplane("XY")
    .box(10, 10, 6)
    .translate((55, 0, 3))
)

# Center mounting base - left foot
left_foot = (
    cq.Workplane("XY")
    .box(18, 18, 4)
    .translate((-15, 0, -2))
)

# Center mounting base - right foot
right_foot = (
    cq.Workplane("XY")
    .box(18, 18, 4)
    .translate((15, 0, -2))
)

# Vertical sight/alidade plate
sight_plate = (
    cq.Workplane("XY")
    .box(4, 20, 25)
    .translate((0, 0, 12))
)

# Horizontal cylinder/barrel on sight
barrel = (
    cq.Workplane("YZ")
    .circle(4)
    .extrude(22)
    .translate((-11, 0, 22))
)

# Left cylinder end cap
left_cap = (
    cq.Workplane("YZ")
    .circle(5)
    .extrude(3)
    .translate((-11, 0, 22))
)

# Right cylinder end cap
right_cap = (
    cq.Workplane("YZ")
    .circle(5)
    .extrude(3)
    .translate((8, 0, 22))
)

# Small pegs/pins on sight plate
peg_left = (
    cq.Workplane("XY")
    .circle(2.5)
    .extrude(8)
    .translate((-12, 0, 18))
)

peg_right = (
    cq.Workplane("XY")
    .circle(2.5)
    .extrude(8)
    .translate((12, 0, 18))
)

# Combine all parts
result = (
    bar
    .union(left_foot)
    .union(right_foot)
    .union(sight_plate)
    .union(barrel)
    .union(left_cap)
    .union(right_cap)
    .union(peg_left)
    .union(peg_right)
    .union(right_block)
)

# Add the blade (pointed end) using a wedge shape
blade_shape = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(-60, 0, 0))
    .box(50, 6, 3)
)

# Create actual pointed blade
pts = [(-85, 0), (-60, -3), (-60, 3)]
blade2 = (
    cq.Workplane("XY")
    .polyline([(-85, 0, 1.5), (-60, -3, 1.5), (-60, 3, 1.5)])
    .close()
    .workplane(offset=3)
    .polyline([(-85, 0, 1.5), (-60, -3, 1.5), (-60, 3, 1.5)])
    .close()
    .loft()
)

# Use a wedge for the blade
blade_final = (
    cq.Workplane("XY")
    .wedge(50, 3, 6, 0, 0, 6, 6)
    .rotate((0, 0, 0), (0, 0, 1), 180)
    .translate((-60, 0, 1.5))
)

result = result.union(blade_final)

# Rotate entire assembly for isometric-like view presentation
result = result.rotate((0, 0, 0), (0, 0, 1), -35)