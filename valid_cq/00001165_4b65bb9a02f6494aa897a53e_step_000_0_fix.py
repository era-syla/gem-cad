import cadquery as cq

# Parameters
cyl_r = 20
cyl_h = 35
wall = 3

trough_w = 80
trough_d = 25
trough_h = 20
trough_angle = 30  # degrees tilt from horizontal

# Build the cylindrical base
base = (
    cq.Workplane("XY")
    .circle(cyl_r)
    .extrude(cyl_h)
)

# Build the trough body - a hollow rectangular box tilted at an angle
# The trough sits on top of the cylinder, tilted

# Outer trough shell
trough_outer = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, cyl_h), rotate=(trough_angle, 0, 0))
    .rect(trough_w, trough_d)
    .extrude(trough_h)
)

# Inner cavity of trough (hollow inside)
trough_inner = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, cyl_h + wall), rotate=(trough_angle, 0, 0))
    .rect(trough_w - 2*wall, trough_d - 2*wall)
    .extrude(trough_h)
)

# Combine base and trough outer
combined = base.union(trough_outer)

# Subtract inner trough cavity - open top trough
# The trough is open on the top face (the face away from cylinder)
# We cut a slightly taller inner to open the top
trough_inner_cut = (
    cq.Workplane("XY")
    .transformed(offset=(0, 0, cyl_h + wall), rotate=(trough_angle, 0, 0))
    .rect(trough_w - 2*wall, trough_d - 2*wall)
    .extrude(trough_h + 1)
)

result = combined.cut(trough_inner_cut)

# Also cut the cylindrical hole through the base partially
# to show the interior connects - cut a cylinder hole partway
inner_cyl = (
    cq.Workplane("XY")
    .circle(cyl_r - wall)
    .extrude(cyl_h - wall)
)

result = result.cut(inner_cyl)