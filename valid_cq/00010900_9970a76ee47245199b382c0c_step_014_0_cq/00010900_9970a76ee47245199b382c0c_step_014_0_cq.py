import cadquery as cq

# Parametric dimensions
cylinder_radius = 5.0
cylinder_hole_radius = 2.5
cylinder_length = 20.0
cylinder_spacing = 9.0  # Slightly less than 2*radius to ensure overlap/fusion
num_horizontal_cylinders = 3
vertical_cylinder_height = 30.0

# Create the base shape (horizontal connected cylinders)
horizontal_cylinders = cq.Workplane("YZ")

for i in range(num_horizontal_cylinders):
    # Calculate center position for each cylinder
    y_pos = i * cylinder_spacing
    
    # Create a cylinder
    cyl = (
        cq.Workplane("YZ")
        .center(y_pos, 0)
        .circle(cylinder_radius)
        .extrude(cylinder_length)
    )
    
    # Create the hole
    hole = (
        cq.Workplane("YZ")
        .center(y_pos, 0)
        .circle(cylinder_hole_radius)
        .extrude(cylinder_length)
    )
    
    # Combine or cut
    part = cyl.cut(hole)
    
    if i == 0:
        horizontal_cylinders = part
    else:
        horizontal_cylinders = horizontal_cylinders.union(part)

# Create the vertical cylinder at the end
# Position it at the end of the last horizontal cylinder
last_cyl_y = (num_horizontal_cylinders - 1) * cylinder_spacing

# The vertical cylinder seems to be tangent or merged at the end of the horizontal row.
# Based on the image, it looks centered on the axis of a potential "4th" cylinder 
# or slightly offset. Let's position it relative to the last horizontal one.
vertical_cyl_y_pos = last_cyl_y + cylinder_spacing
# The vertical cylinder sits on the ground plane (Z= -cylinder_radius) relative to the horizontal centers?
# Looking at the image, the horizontal cylinders are floating or centered. 
# Let's assume the horizontal cylinders are centered at Z=0.
# The vertical cylinder goes up. Its bottom seems to align with the bottom of the horizontal ones.
vertical_cyl_bottom_z = -cylinder_radius

vertical_cylinder = (
    cq.Workplane("XY")
    .center(0, vertical_cyl_y_pos)  # Align with the row in Y, but shifted
    .workplane(offset=vertical_cyl_bottom_z) # Start from bottom
    .circle(cylinder_radius)
    .extrude(vertical_cylinder_height)
)

vertical_hole = (
    cq.Workplane("XY")
    .center(0, vertical_cyl_y_pos)
    .workplane(offset=vertical_cyl_bottom_z)
    .circle(cylinder_hole_radius)
    .extrude(vertical_cylinder_height)
)

vertical_part = vertical_cylinder.cut(vertical_hole)

# Combine horizontal part and vertical part
# The horizontal part was extruded along X, centered at YZ plane.
# So its length is split -10 to +10 if centered, or 0 to 20. 
# The code above `.extrude(cylinder_length)` defaults to normal direction.
# Let's ensure alignment. The horizontal cylinders are extruded in X.
# We need to shift the horizontal assembly to align with the vertical one if needed.
# Let's recenter the horizontal part to make logic easier.
# Actually, the loop created them in place. The vertical one is offset in Y.
# We need to rotate the horizontal assembly or change the workplane of the vertical one 
# to match the image orientation (Horizontal along X, Row along Y).
# The current code:
# Horizontal: Circles on YZ plane, extruded along X. (Row grows along Y).
# Vertical: Circle on XY plane, extruded along Z. (Positioned at higher Y).

# Union the parts
result = horizontal_cylinders.union(vertical_part)