import cadquery as cq

# Parametric dimensions
base_width = 40.0
base_length = 40.0
base_height = 20.0
fillet_radius = 25.0  # Radius for the top curved surface

cylinder_diam = 20.0
cylinder_height = 30.0  # Height extending upwards from within the base
hole_diam = 8.0

pocket_width = 25.0
pocket_height = 12.0
pocket_depth = 35.0   # How deep the rectangular cutout goes

# 1. Create the base block
base = cq.Workplane("XY").box(base_length, base_width, base_height)

# 2. Create the curved top surface
# We can achieve this by creating a large cylinder and cutting it away from the top.
# The axis of the cutting cylinder needs to be horizontal (e.g., along Y or X) and positioned above.
# Looking at the image, the curve dips in the middle. This suggests a cut subtraction.
# Let's try positioning a cylinder with its axis along Y, shifted up in Z.
cut_radius = 60.0
cut_center_z = base_height/2 + cut_radius - 5.0 # Fine tune depth of the dip
cutter = (
    cq.Workplane("XZ")
    .workplane(offset=-base_width/2 - 5) # Start outside
    .circle(cut_radius)
    .extrude(base_width + 10) # Extrude along Y
    .translate((0, 0, cut_center_z))
)

# Apply the cut
base_curved = base.cut(cutter)

# 3. Create the central vertical cylinder
# It sits on top of the base (or emerges from it).
# We need to find the top surface to extrude from, or just union a cylinder.
# Unioning is safer to ensure valid geometry regardless of the curve.
# The cylinder looks like it starts slightly embedded or from the "floor" of the curve.
cylinder_z_offset = base_height / 2 - 5.0 # Start slightly inside the block
main_cylinder = (
    cq.Workplane("XY")
    .circle(cylinder_diam / 2)
    .extrude(cylinder_height)
    .translate((0, 0, cylinder_z_offset))
)

# 4. Create the through-hole in the cylinder
# This goes through the cylinder.
hole_cylinder = (
    cq.Workplane("XY")
    .circle(hole_diam / 2)
    .extrude(cylinder_height + 20) # Make it long enough to cut through
    .translate((0, 0, cylinder_z_offset - 5))
)

# 5. Create the rectangular pocket/cutout on the side face
# The pocket is on one of the vertical faces (let's say the front face, XZ plane, negative Y direction)
pocket = (
    cq.Workplane("XZ")
    .workplane(offset=base_width/2) # Move to the front face
    .rect(pocket_width, pocket_height)
    .extrude(-pocket_depth) # Cut inwards (negative direction)
)

# 6. Combine all operations
result = (
    base_curved
    .union(main_cylinder)
    .cut(hole_cylinder)
    .cut(pocket)
)