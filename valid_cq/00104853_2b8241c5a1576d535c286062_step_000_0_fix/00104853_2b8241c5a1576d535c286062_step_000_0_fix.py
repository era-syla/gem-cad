import cadquery as cq

# Define 2D profiles
outer = [(-40, 40), (40, 40), (40, 20), (20, 20), (0, -40), (-20, 20), (-40, 20)]
triangle = [(-8, 16), (8, 16), (0, -20)]

# Base plate
base = cq.Workplane("XY").polyline(outer).close().extrude(1)

# Middle border (outer shape minus central triangle)
middle_full = cq.Workplane("XY").polyline(outer).close().extrude(4).translate((0, 0, 1))
cut_tri = cq.Workplane("XY").polyline(triangle).close().extrude(4).translate((0, 0, 1))
middle = middle_full.cut(cut_tri)

# Top plate
top = cq.Workplane("XY").polyline(outer).close().extrude(1).translate((0, 0, 5))

# Combine into final result
result = base.union(middle).union(top)