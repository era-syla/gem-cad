import cadquery as cq

# Parameters
L = 100            # total length
R_end = 10         # end circle radius
w_bar = 8          # width of connecting bar
thickness = 4      # thickness of part
hole_d = 5         # diameter of holes

shift = L/2 - R_end

# Create left end
left_end = cq.Workplane("XY").center(-shift, 0).circle(R_end).extrude(thickness)

# Create right end
right_end = cq.Workplane("XY").center(shift, 0).circle(R_end).extrude(thickness)

# Create central bar
bar = cq.Workplane("XY").rect(L - 2*R_end, w_bar).extrude(thickness)

# Combine all parts
combined = left_end.union(right_end).union(bar)

# Drill holes through ends
result = (
    combined
    .faces(">Z")
    .workplane()
    .pushPoints([(-shift, 0), (shift, 0)])
    .hole(hole_d)
)