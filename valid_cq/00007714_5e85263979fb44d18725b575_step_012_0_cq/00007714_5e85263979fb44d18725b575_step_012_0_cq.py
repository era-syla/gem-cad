import cadquery as cq

# --- Parameter Definitions ---
# Overall dimensions
wall_height = 100.0
long_wall_length = 150.0
short_wall_length = 80.0
wall_thickness = 10.0

# "Room" or Shaft dimensions (the hollow rectangular part)
shaft_width = 40.0   # Dimension along the short wall direction
shaft_depth = 60.0   # Dimension along the long wall direction
shaft_wall_thickness = 5.0 # Slightly thinner walls for the internal feature

# Doorway dimensions
door_width = 25.0
door_height = 50.0
door_offset = 20.0 # From the corner

# Top notch/cutout dimensions on the far end of the long wall
notch_width = 15.0
notch_depth = 5.0

# --- Geometry Construction ---

# 1. Create the main L-shaped wall structure
# We'll build this by creating two rectangular prisms and uniting them.

# Long wall
long_wall = cq.Workplane("XY").box(long_wall_length, wall_thickness, wall_height, centered=(False, True, False))

# Short wall (attached at the origin corner)
# We rotate or position it to form the corner. 
# Let's align the corner at (0,0).
short_wall = (
    cq.Workplane("XY")
    .box(wall_thickness, short_wall_length, wall_height, centered=(True, False, False))
    .translate((-wall_thickness/2, -short_wall_length, 0)) # Move so the corner aligns with the start of long wall
    .translate((wall_thickness/2, short_wall_length, 0)) # Actually, easier to just build it in place
)

# Let's rebuild for cleaner coordinates:
# Let the outer corner be at (0,0).
# Long wall extends along +X.
# Short wall extends along +Y.

long_wall = (
    cq.Workplane("XY")
    .box(long_wall_length, wall_thickness, wall_height, centered=(False, False, False))
    .translate((0, -wall_thickness, 0)) # Move so inner face is on X axis
)

short_wall = (
    cq.Workplane("XY")
    .box(wall_thickness, short_wall_length, wall_height, centered=(False, False, False))
    .translate((-wall_thickness, 0, 0)) # Move so inner face is on Y axis
)

walls = long_wall.union(short_wall)


# 2. Create the enclosed shaft/room
# This is attached to the inner corner.
# Dimensions: shaft_depth along X, shaft_width along Y.

shaft_outer = (
    cq.Workplane("XY")
    .box(shaft_depth, shaft_width, wall_height, centered=(False, False, False))
)

shaft_inner = (
    cq.Workplane("XY")
    .box(shaft_depth - shaft_wall_thickness, 
         shaft_width - shaft_wall_thickness, 
         wall_height, 
         centered=(False, False, False))
    .translate((shaft_wall_thickness, shaft_wall_thickness, 0)) # Offset to create wall thickness
)

shaft = shaft_outer.cut(shaft_inner)

# Combine main walls with the shaft
structure = walls.union(shaft)


# 3. Create the Doorway
# Located on the long wall face.
door_cutout = (
    cq.Workplane("XY")
    .box(door_width, wall_thickness * 3, door_height, centered=(False, True, False))
    .translate((door_offset, -wall_thickness/2, 0))
)

structure = structure.cut(door_cutout)


# 4. Create the Notch at the end of the long wall
# Located at the top, far end of the long wall.
notch_cutout = (
    cq.Workplane("XY")
    .workplane(offset=wall_height) # Move to top
    .box(notch_width, notch_depth, wall_height, centered=(False, False, False)) # Height doesn't matter much as long as it cuts down
    .translate((long_wall_length - notch_width - 15, -wall_thickness, -5)) # Position: near end, on the edge, slightly down
)
# Re-adjusting notch logic based on visual:
# It looks like a cutout on the top edge of the long wall.
notch_cutout = (
    cq.Workplane("XZ") # Work on the side profile
    .box(notch_width, notch_depth, wall_thickness*2, centered=(True, True, True))
    .translate((long_wall_length - notch_width, wall_height, -wall_thickness/2))
)

structure = structure.cut(notch_cutout)

# Assign to result
result = structure