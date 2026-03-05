import cadquery as cq

# 1. Sphere (Top Left)
# Positioned at (-25, 50, 0)
sphere = cq.Workplane("XY").sphere(10).translate((-25, 50, 0))

# 2. Torus (Middle Left)
# Positioned at (-25, 15, 0)
# Using kernel primitive wrapped in Workplane
torus_solid = cq.Solid.makeTorus(9, 2.5)
torus = cq.Workplane("XY").newObject([torus_solid]).translate((-25, 15, 0))

# 3. Cylinder (Bottom Left)
# Positioned at (-25, -25, 0)
cylinder = cq.Workplane("XY").cylinder(12, 10).translate((-25, -25, 0))

# 4. Rounded Box (Middle Right)
# Positioned at (25, 20, 0)
# Create a box and fillet the end facing the center (-X)
box_len, box_width, box_height = 35, 18, 15
rounded_box = (
    cq.Workplane("XY")
    .box(box_len, box_width, box_height)
    .edges("|Z and <X")
    .fillet(box_width / 2 - 0.01)
    .translate((25, 20, 0))
)

# 5. Twisted Loft (Bottom Right)
# Positioned at (25, -20, 0)
# Loft from a horizontal rectangle to a narrower, rotated rectangle/line
twist = (
    cq.Workplane("XY")
    .translate((25, -20, 0))
    .rect(20, 12)
    .workplane(offset=20)
    .rect(2, 12)  # Tapering to a thin profile to create a wedge/chisel shape
    .loft(combine=True)
)

# Combine all independent solids into a single result
result = sphere.union(torus).union(cylinder).union(rounded_box).union(twist)