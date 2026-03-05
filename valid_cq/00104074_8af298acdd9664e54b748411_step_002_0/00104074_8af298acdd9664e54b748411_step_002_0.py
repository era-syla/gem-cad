import cadquery as cq

# Parameters defining the geometry
box_width = 40.0       # Dimension along X axis
box_depth = 20.0       # Dimension along Y axis
box_height = 60.0      # Dimension along Z axis
wall_thickness = 1.5   # Thickness of the top rim
recess_depth = 2.0     # Depth of the top pocket

cyl_base_dia = 12.0    # Diameter of the cylinder base flange
cyl_base_height = 1.5  # Height/Thickness of the base flange
post_dia = 6.0         # Diameter of the vertical post
post_height = 35.0     # Height of the post (extending from the flange)
cyl_offset_x = -10.0   # Offset of the cylinder from the center along X

# 1. Create the main rectangular body centered at origin
main_body = cq.Workplane("XY").box(box_width, box_depth, box_height)

# 2. Create the recessed top (pocket)
# Select the top face (+Z), create a workplane, draw the inner rectangle, and cut
main_body = (
    main_body
    .faces(">Z")
    .workplane()
    .rect(box_width - 2 * wall_thickness, box_depth - 2 * wall_thickness)
    .cutBlind(-recess_depth)
)

# 3. Create the cylinder assembly (Base Flange + Post)
# Calculate the Z-level of the pocket floor to place the cylinder correctly
pocket_floor_z = (box_height / 2.0) - recess_depth

cylinder_assembly = (
    cq.Workplane("XY")
    .workplane(offset=pocket_floor_z)
    .center(cyl_offset_x, 0)
    .circle(cyl_base_dia / 2.0)
    .extrude(cyl_base_height)
    .faces(">Z").workplane()  # Select the top face of the newly created base disk
    .circle(post_dia / 2.0)
    .extrude(post_height)
)

# 4. Combine the main body with the cylinder assembly
result = main_body.union(cylinder_assembly)