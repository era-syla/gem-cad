import cadquery as cq

# --- Parametric Dimensions ---
# Box dimensions
length = 80.0
width = 40.0
height = 40.0
wall_thickness = 3.0

# Lid dimensions
lid_top_thickness = 2.0
lid_insert_depth = 2.0
tolerance = 0.5  # Clearance for the lid to fit inside the box

# --- Geometry Construction ---

# 1. Create the Box (Container)
# Start with a solid block centered at the origin
box_base = cq.Workplane("XY").box(length, width, height)

# Create the hollow container by shelling the solid.
# Selecting the "+Z" (top) face and applying a negative shell thickness
# removes the top face and hollows the interior.
container = box_base.faces("+Z").shell(-wall_thickness)

# 2. Create the Lid
# Create the top plate of the lid
lid_plate = cq.Workplane("XY").box(length, width, lid_top_thickness)

# Create the insert/step that fits into the box
# Dimensions are reduced by the wall thickness and tolerance
insert_length = length - (2 * wall_thickness) - tolerance
insert_width = width - (2 * wall_thickness) - tolerance

# Create the insert block
lid_insert = cq.Workplane("XY").box(insert_length, insert_width, lid_insert_depth)

# Position the insert below the top plate
# Calculate the Z offset to align the top of the insert with the bottom of the plate
# Plate bottom is at -lid_top_thickness/2
# Insert top is at +lid_insert_depth/2 (before move)
z_shift = -(lid_top_thickness + lid_insert_depth) / 2
lid_insert = lid_insert.translate((0, 0, z_shift))

# Combine plate and insert to form the full lid object
lid = lid_plate.union(lid_insert)

# --- Assembly and Positioning ---

# Position the Container to the right
# Translate Z by height/2 so the bottom rests on the Z=0 plane
container_positioned = container.translate((length * 0.6, 0, height / 2))

# Position the Lid to the left
# Translate Z so the bottom of the insert rests on the Z=0 plane
lid_bottom_z_local = -(lid_top_thickness / 2 + lid_insert_depth)
lid_z_correction = -lid_bottom_z_local
lid_positioned = lid.translate((-length * 0.6, 0, lid_z_correction))

# Combine into the final result
result = container_positioned.union(lid_positioned)