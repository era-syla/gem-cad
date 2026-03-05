import cadquery as cq

# Main base plate
base_length = 60
base_width = 45
base_height = 10

# Cylindrical boss dimensions
boss_radius = 18
boss_height = 22
boss_inner_radius = 8

# Mounting hole
mount_hole_radius = 4
mount_hole_x = -22
mount_hole_y = 5

# Create the base plate
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_height)
)

# Add the cylindrical boss on top, offset toward one side
boss = (
    cq.Workplane("XY")
    .transformed(offset=(8, 0, 0))
    .circle(boss_radius)
    .extrude(base_height + boss_height)
)

# Union base and boss
result = base.union(boss)

# Add chamfer/fillet to base edges - select top edges of base only
# Cut the hollow through the boss
result = (
    result
    .cut(
        cq.Workplane("XY")
        .transformed(offset=(8, 0, 0))
        .circle(boss_inner_radius)
        .extrude(base_height + boss_height + 5)
    )
)

# Cut mounting hole through the base plate
result = (
    result
    .cut(
        cq.Workplane("XY")
        .transformed(offset=(mount_hole_x, mount_hole_y, 0))
        .circle(mount_hole_radius)
        .extrude(base_height)
    )
)

# Add triangular gusset/rib on the side connecting base to boss
# Create a wedge shape as gusset
gusset = (
    cq.Workplane("XZ")
    .transformed(offset=(0, base_width/2 - 2, 0))
    .moveTo(-14, base_height)
    .lineTo(8 - boss_radius + 2, base_height)
    .lineTo(8, base_height + boss_height - 2)
    .lineTo(8, base_height)
    .lineTo(-14, base_height)
    .close()
    .extrude(4)
    .translate((0, -2, 0))
)

# Don't add gusset for simplicity - it complicates the geometry
# Instead add a simple fillet on the base

# Fillet the bottom edges of base
try:
    result = result.edges("|Z").fillet(3)
except:
    pass

# Try to fillet top edges of base (not boss)
try:
    result = (
        result
        .faces(">Z[0]")
        .edges()
        .fillet(1.5)
    )
except:
    pass