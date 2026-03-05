import cadquery as cq

# Dimensions
plate_width = 100
plate_height = 140
thickness = 5

# Window dimensions and positions
# Top Left (Horizontal Rectangle)
tl_width = 35
tl_height = 30
tl_x = -25
tl_y = 40

# Top Right (Vertical Rectangle)
tr_width = 25
tr_height = 50
tr_x = 25
tr_y = 30

# Bottom Left (Tall Vertical Rectangle)
bl_width = 25
bl_height = 60
bl_x = -25
bl_y = -30

# Bottom Right 1 (Inner/Lower Rectangle)
br1_width = 10
br1_height = 25
br1_x = 15
br1_y = -45

# Bottom Right 2 (Outer/Higher Rectangle)
br2_width = 10
br2_height = 25
br2_x = 35
br2_y = -30

# Create base plate
result = cq.Workplane("XY").box(plate_width, plate_height, thickness)

# Create cutouts
result = (
    result.faces(">Z")
    .workplane()
    # Top Left
    .moveTo(tl_x, tl_y)
    .rect(tl_width, tl_height)
    # Top Right
    .moveTo(tr_x, tr_y)
    .rect(tr_width, tr_height)
    # Bottom Left
    .moveTo(bl_x, bl_y)
    .rect(bl_width, bl_height)
    # Bottom Right - Inner
    .moveTo(br1_x, br1_y)
    .rect(br1_width, br1_height)
    # Bottom Right - Outer
    .moveTo(br2_x, br2_y)
    .rect(br2_width, br2_height)
    # Cut through the plate
    .cutThruAll()
)