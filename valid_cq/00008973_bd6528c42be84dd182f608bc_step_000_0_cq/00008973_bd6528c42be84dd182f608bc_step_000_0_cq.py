import cadquery as cq

# Parametric dimensions
plate_length = 60.0
plate_width = 40.0
plate_thickness = 5.0

vertical_leg_width = 40.0
vertical_leg_height = 45.0  # From bottom of plate to bottom of leg
vertical_leg_thickness = 10.0

boss_diameter = 20.0
boss_length = 15.0
hole_diameter = 10.0
boss_offset_from_bottom = 15.0  # Center of boss from bottom of leg
boss_chamfer = 1.0

# 1. Create the top plate
# Centered on XY plane, extruded downwards (or upwards, but let's keep Z=0 as top surface)
plate = cq.Workplane("XY").box(plate_length, plate_width, plate_thickness)

# 2. Create the vertical leg
# This is attached to the bottom of the plate.
# Based on the image, it looks centered along the width (Y) but offset or centered along length (X).
# It appears to be an L-shape or T-shape bracket. Let's assume it's a T-bracket style where the leg is centered.
leg = (
    cq.Workplane("XY")
    .workplane(offset=-plate_thickness / 2) # Start from bottom of plate
    .transformed(offset=(0, 0, -vertical_leg_height / 2)) # Move down to center of extrusion
    .box(vertical_leg_thickness, vertical_leg_width, vertical_leg_height)
)

# 3. Create the triangular gusset/support
# The image shows a tapered section connecting the vertical leg to the plate.
# It looks like a wedge.
gusset_length = (plate_length - vertical_leg_thickness) / 2 # Extends to edge
gusset_height = vertical_leg_height
gusset_thickness = vertical_leg_width # Full width gusset based on the shading

# Let's draw the profile on the YZ plane (side view) and extrude.
# Actually, drawing on XZ plane is easier to visualize the slope.
gusset = (
    cq.Workplane("XZ")
    .workplane(offset= -vertical_leg_width / 2) # Move to the side
    .moveTo(-vertical_leg_thickness / 2, -plate_thickness / 2) # Top-inner corner
    .lineTo(-plate_length / 2, -plate_thickness / 2) # Top-outer corner
    .lineTo(-vertical_leg_thickness / 2, -plate_thickness / 2 - vertical_leg_height) # Bottom-inner corner
    .close()
    .extrude(vertical_leg_width)
)

# 4. Create the cylindrical boss
# It sticks out from the side of the vertical leg.
boss = (
    cq.Workplane("YZ")
    .workplane(offset=vertical_leg_thickness / 2) # Start at the face of the vertical leg
    .center(0, -plate_thickness/2 - vertical_leg_height + boss_offset_from_bottom) # Position vertically
    .circle(boss_diameter / 2)
    .extrude(boss_length)
)

# Add chamfer to the boss
boss = boss.faces(">X").edges().chamfer(boss_chamfer)

# 5. Create the through hole
hole = (
    cq.Workplane("YZ")
    .workplane(offset=vertical_leg_thickness / 2 + boss_length) # Start at the end of the boss
    .center(0, -plate_thickness/2 - vertical_leg_height + boss_offset_from_bottom)
    .circle(hole_diameter / 2)
    .extrude(-(boss_length + vertical_leg_thickness), combine=False) # Cut backwards through boss and leg
)

# Combine everything
result = plate.union(leg).union(gusset).union(boss).cut(hole)

# Export or display
if "show_object" in locals():
    show_object(result)