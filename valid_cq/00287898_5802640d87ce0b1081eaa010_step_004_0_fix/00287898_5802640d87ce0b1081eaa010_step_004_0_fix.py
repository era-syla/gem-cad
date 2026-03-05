import cadquery as cq

# Central block
block = cq.Workplane("XY").box(8, 4, 4)

# Rod profile (1×1 square in YZ plane)
profile = cq.Workplane("YZ").rect(1, 1)

# Rod path in XY plane, with a slight bend
path = cq.Workplane("XY").polyline([
    (-40, 0),
    (0,   0),
    (10,  0),
    (20,  2),
    (60,  2),
]).wire()

# Sweep the profile along the path to create the rod
rod = profile.sweep(path)

# Separate block on the right
separate_block = cq.Workplane("XY").box(4, 4, 4).translate((80, 0, 0))

# Combine all parts into the final result
result = block.union(rod).union(separate_block)