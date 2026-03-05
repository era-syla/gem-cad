import cadquery as cq

# Create a cube with spherical cutouts on each face (like a dice with circular holes)
# and a sphere trapped inside

size = 40
hole_radius = 13
fillet_radius = 3

# Start with a box
box = cq.Workplane("XY").box(size, size, size)

# Subtract a sphere from the center (creates the hollow interior with the trapped sphere look)
sphere_radius = 17
box = box.cut(cq.Workplane("XY").sphere(sphere_radius))

# Cut circular holes through each face
# Top and bottom (Z axis)
box = box.cut(
    cq.Workplane("XY").workplane(offset=size/2 + 1).circle(hole_radius).extrude(size + 2, both=False)
    .translate((0, 0, -(size/2 + 1)))
)

# Actually let's redo with cylinders for each direction
box = cq.Workplane("XY").box(size, size, size)

# Subtract central sphere
inner_sphere = cq.Workplane("XY").sphere(sphere_radius)
box = box.cut(inner_sphere)

# Cut cylinders through each axis
cyl_z = cq.Workplane("XY").cylinder(size * 2, hole_radius)
cyl_x = cq.Workplane("YZ").cylinder(size * 2, hole_radius)
cyl_y = cq.Workplane("XZ").cylinder(size * 2, hole_radius)

box = box.cut(cyl_z)
box = box.cut(cyl_x)
box = box.cut(cyl_y)

# Apply fillets to the box edges
# We need to fillet the edges of the original box shape
# Create box with fillets first, then do cuts
box_filleted = cq.Workplane("XY").box(size, size, size)

# Fillet the edges
try:
    box_filleted = box_filleted.edges("|Z").fillet(fillet_radius)
    box_filleted = box_filleted.edges("#Z").fillet(fillet_radius)
except:
    pass

# Subtract central sphere
box_filleted = box_filleted.cut(inner_sphere)

# Cut cylinders through each axis
box_filleted = box_filleted.cut(cyl_z)
box_filleted = box_filleted.cut(cyl_x)
box_filleted = box_filleted.cut(cyl_y)

result = box_filleted