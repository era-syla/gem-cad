import cadquery as cq

# Parametric dimensions
width = 80.0          # Total width of the base
length = 120.0        # Total length of the base
base_height = 5.0     # Height of the bottom flange part
wall_height = 10.0    # Height of the vertical walls above the base
wall_thickness = 2.0  # Thickness of the walls
base_fillet = 5.0     # Fillet radius for the base corners
top_fillet = 5.0      # Fillet radius for the top wall corners
inset = 3.0           # How much the wall is inset from the base edge

# Derived calculations
# The wall section is smaller than the base
wall_outer_width = width - (2 * inset)
wall_outer_length = length - (2 * inset)

# 1. Create the base plate (the wider bottom part)
base = (
    cq.Workplane("XY")
    .box(length, width, base_height)
    .edges("|Z")
    .fillet(base_fillet)
)

# 2. Create the wall section (solid block first) sitting on top of the base
# We align it so its bottom face matches the top face of the base
upper_block = (
    cq.Workplane("XY")
    .workplane(offset=base_height/2 + wall_height/2) # Move center up
    .box(wall_outer_length, wall_outer_width, wall_height)
    .edges("|Z")
    .fillet(top_fillet)
)

# 3. Combine base and upper block
solid = base.union(upper_block)

# 4. Hollow out the top to create the tray/lid shape
# We select the top face and shell inwards with a negative thickness
result = (
    solid
    .faces(">Z")
    .shell(-wall_thickness)
)