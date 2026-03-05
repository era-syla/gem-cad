import cadquery as cq

# Parameters
big_r = 10       # Radius of the large end
small_len = 80   # Length from circle center to tip
thickness = 4    # Thickness in Z
hole_r = 4       # Radius of the pivot hole

# Create the large circular end
circular_end = cq.Workplane("XY").circle(big_r).extrude(thickness)

# Create the tapering triangular tail
triangle_wire = [(0, big_r), (small_len, 0), (0, -big_r), (0, big_r)]
triangular_tail = cq.Workplane("XY").polyline(triangle_wire).close().extrude(thickness)

# Combine both solids
combined = circular_end.union(triangular_tail)

# Drill the pivot hole through the large end
result = combined.faces(">Z").workplane().hole(2 * hole_r)