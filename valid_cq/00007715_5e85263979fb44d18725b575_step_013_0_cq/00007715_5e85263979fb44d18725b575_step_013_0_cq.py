import cadquery as cq

# -- Parametric Dimensions --
# Main walls
wall_height = 300.0
long_wall_length = 400.0
short_wall_length = 250.0
wall_thickness = 20.0

# Doorway
door_width = 80.0
door_height = 150.0  # Looks shorter than full height in the image
door_pos_from_corner = 50.0 # Distance from the outer corner edge

# Internal Shaft/Box
shaft_width = 100.0
shaft_depth = 80.0
shaft_wall_thickness = 10.0
shaft_height = wall_height # Same height as the walls

# Top Notch
notch_width = 30.0
notch_depth = 10.0
notch_pos = 280.0 # Distance along the long wall

# -- Construction --

# 1. Create the base L-shape walls
# We'll create the long wall first, aligned along X
long_wall = (
    cq.Workplane("XY")
    .box(long_wall_length, wall_thickness, wall_height)
    .translate((long_wall_length / 2, wall_thickness / 2, wall_height / 2))
)

# Create the short wall, aligned along Y, attached to the start of the long wall
short_wall = (
    cq.Workplane("XY")
    .box(wall_thickness, short_wall_length, wall_height)
    .translate((wall_thickness / 2, short_wall_length / 2, wall_height / 2))
    # Adjust position so the corner is flush on the outside
    .translate((-wall_thickness, 0, 0)) 
    # Move it back so it joins the long wall correctly at the corner
    .translate((wall_thickness, wall_thickness, 0)) 
    # Actually, simpler: origin at outer corner (0,0). 
    # Let's rebuild coordinate system logic for clarity.
)

# Re-approach: Define origin at the bottom-left outer corner.
# X-axis runs along the long wall, Y-axis runs along the short wall (backwards)
# Z-axis is up.

# Long Wall (along positive X)
long_wall = (
    cq.Workplane("XY")
    .box(long_wall_length, wall_thickness, wall_height, centered=(False, False, False))
    # Shift Y so the outer face is at Y=0 (assuming inside corner is positive Y relative to wall)
    # Actually, looking at the image, let's put the outer corner at (0,0,0).
    # Long wall goes +X. Short wall goes +Y.
    .translate((0, -wall_thickness, 0)) 
)

# Short Wall (along positive Y)
short_wall = (
    cq.Workplane("XY")
    .box(wall_thickness, short_wall_length, wall_height, centered=(False, False, False))
    .translate((-wall_thickness, 0, 0))
)

# Combine walls
walls = long_wall.union(short_wall)

# 2. Create the Doorway Cutout
# Located on the long wall.
door_cutout = (
    cq.Workplane("XY")
    .box(door_width, wall_thickness * 3, door_height, centered=(False, True, False))
    .translate((door_pos_from_corner, -wall_thickness/2, 0))
)

walls = walls.cut(door_cutout)

# 3. Create the Internal Shaft
# It sits in the "inside" corner (positive X, positive Y quadrant relative to the wall intersection)
# It appears to be a hollow rectangular prism attached to the walls.

# Outer shell of the shaft
shaft_outer = (
    cq.Workplane("XY")
    .box(shaft_width, shaft_depth, shaft_height, centered=(False, False, False))
    # Position it against the inside faces of the main walls
    .translate((0, 0, 0)) 
)

# Inner cutout of the shaft
shaft_inner = (
    cq.Workplane("XY")
    .box(shaft_width - shaft_wall_thickness, 
         shaft_depth - shaft_wall_thickness, 
         shaft_height, 
         centered=(False, False, False))
    # Offset to create wall thickness on the 'free' sides
    .translate((shaft_wall_thickness/2, shaft_wall_thickness/2, 0)) 
    # But wait, looking at the image, the shaft walls connect to the main walls.
    # The hollow part is inside.
    # Let's adjust:
    # The shaft is attached to the long wall (y=0 face) and somewhere along X.
    # Looking at the image, the shaft is centered roughly behind the "corner" area 
    # but actually it looks like it's attached to the long wall and extends inwards.
    # Let's re-examine image:
    # There is a distinct box attached to the INSIDE of the L-junction.
    # It shares the height of the walls.
)

# Let's refine the shaft position based on the image:
# It's tucked into the corner.
shaft_box_outer = (
    cq.Workplane("XY")
    .box(shaft_width, shaft_depth, shaft_height, centered=(False, False, False))
)

shaft_box_inner = (
    cq.Workplane("XY")
    .box(shaft_width - shaft_wall_thickness, 
         shaft_depth - shaft_wall_thickness, 
         shaft_height, centered=(False, False, False))
    .translate((shaft_wall_thickness, shaft_wall_thickness, 0)) 
    # Offset so walls exist on the "inner" sides away from the main walls
)

# The hollow shaft structure
shaft = shaft_box_outer.cut(shaft_box_inner)

# Combine shaft with main walls
result = walls.union(shaft)

# 4. Create the Top Notch
# There is a small notch on the top edge of the long wall, near the far end.
notch = (
    cq.Workplane("XY")
    .box(notch_width, wall_thickness * 2, notch_depth, centered=(False, True, False))
    .translate((notch_pos, -wall_thickness/2, wall_height - notch_depth))
)

result = result.cut(notch)

# Final Result
result = result