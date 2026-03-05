import cadquery as cq

# Parameters
R = 10          # cylinder radius
offset = 2*R    # center-to-center distance of the two cylinders
H1 = 80         # height of the long cylinder
H2 = 40         # height of the short cylinder
dz = (H1 - H2) / 2  # vertical offset of the short cylinder within the tall one

# Create the tall cylinder (left)
cyl1 = cq.Workplane("XY").circle(R).extrude(H1)

# Create the shorter, offset cylinder (right)
cyl2 = (
    cq.Workplane("XY")
    .transformed(offset=(offset, 0, dz))
    .circle(R)
    .extrude(H2)
)

# Combine the two cylinders
combined = cyl1.union(cyl2)

# Cut a vertical flat on the inner side of the short cylinder
cut_box = (
    cq.Workplane("XY")
    .transformed(offset=(R, 0, dz))
    .box(100, 2*R + 4, H2, centered=(False, True, False))
)

# Final result
result = combined.cut(cut_box)