import cadquery as cq

# Parameters
bar_length = 100.0
bar_width = 5.0
bar_thickness = 5.0

support_width = 20.0
support_depth = 10.0
support_height = 25.0
wall_thickness = 2.0

# Offset for supports along Y
y_offset = bar_length/2 - support_depth/2

# Base beam
base = cq.Workplane("XY").box(bar_width, bar_length, bar_thickness)

# Solid supports
support1 = (
    cq.Workplane("XY")
    .transformed(offset=(0, y_offset, bar_thickness/2 + support_height/2))
    .box(support_width, support_depth, support_height)
)
support2 = (
    cq.Workplane("XY")
    .transformed(offset=(0, -y_offset, bar_thickness/2 + support_height/2))
    .box(support_width, support_depth, support_height)
)

# Merge base and supports
result = base.union(support1).union(support2)

# Inner cavity dimensions (creates U-shaped channel)
cavity_width = support_width - 2*wall_thickness
cavity_depth = support_depth - wall_thickness

# Cavity for support1 (cuts from the front toward the beam center)
yfront1 = y_offset + support_depth/2
ycut1 = yfront1 - cavity_depth/2
cut1 = (
    cq.Workplane("XY")
    .transformed(offset=(0, ycut1, bar_thickness/2 + support_height/2))
    .box(cavity_width, cavity_depth, support_height)
)

# Cavity for support2 (mirrored)
yfront2 = -y_offset - support_depth/2
ycut2 = yfront2 + cavity_depth/2
cut2 = (
    cq.Workplane("XY")
    .transformed(offset=(0, ycut2, bar_thickness/2 + support_height/2))
    .box(cavity_width, cavity_depth, support_height)
)

# Subtract cavities to form U-channels
result = result.cut(cut1).cut(cut2)