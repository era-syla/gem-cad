import cadquery as cq

# Parametric dimensions
plate_width = 100.0  # Total width of the plate
plate_depth = 100.0  # Total depth of the plate
base_thickness = 10.0  # Thickness of the bottom plate
wall_height = 10.0    # Additional height of the side walls (total height = base + wall)
wall_width = 15.0     # Width of the side walls
corner_notch_size = 3.0 # Size of the cutout at the inner corner intersection

hole_diameter = 4.0   # Diameter of the screw holes
center_hole_dia = 6.0 # Diameter of the central hole

# Calculate derived dimensions
total_height = base_thickness + wall_height

# 1. Create the base block
result = cq.Workplane("XY").box(plate_width, plate_depth, base_thickness)

# 2. Add the walls
# We need an L-shaped wall. We can create this by adding two blocks.
# Left Wall
left_wall_center_x = -plate_width/2 + wall_width/2
result = result.faces(">Z").workplane().center(left_wall_center_x, 0) \
    .rect(wall_width, plate_depth).extrude(wall_height)

# Top Wall (adjusting width to avoid double overlapping the corner for cleaner boolean, though union handles it)
# We place it at the top edge
top_wall_center_y = plate_depth/2 - wall_width/2
result = result.faces(">Z").workplane().center(0, top_wall_center_y) \
    .rect(plate_width, wall_width).extrude(wall_height, combine=True)

# 3. Create the corner notch
# The walls meet at the top-left corner (-x, +y).
# The notch appears to be a small square or chamfer on the *inner* corner of the L-shape.
# The inner corner coordinate is roughly (-plate_width/2 + wall_width, plate_depth/2 - wall_width)
notch_x = -plate_width/2 + wall_width
notch_y = plate_depth/2 - wall_width

# We cut a small square profile at that intersection
result = result.faces(">Z").workplane().center(notch_x, notch_y) \
    .rect(corner_notch_size*2, corner_notch_size*2) \
    .cutBlind(-wall_height)

# 4. Add Holes
# Looking at the image:
# - There are 2 holes on the left wall.
# - There are 2 holes on the top wall.
# - There is 1 hole in the center of the plate.
# - There is 1 hole in the bottom-right corner of the base area.

# Wall Holes (Counterbored or just simple holes? Image shows simple holes)
# Left Wall Holes
result = result.faces(">Z").workplane().center(left_wall_center_x, 0) \
    .pushPoints([(0, -plate_depth/4), (0, plate_depth/6)]) \
    .hole(hole_diameter)

# Top Wall Holes
result = result.faces(">Z").workplane().center(0, top_wall_center_y) \
    .pushPoints([(plate_width/4, 0), (plate_width/2 - wall_width*1.5, 0)]) \
    .hole(hole_diameter)

# Center Hole
result = result.faces(">Z").workplane().center(0, 0).hole(center_hole_dia)

# Bottom Right Corner Hole
# This is in the flat area.
br_hole_x = plate_width/2 - wall_width
br_hole_y = -plate_depth/2 + wall_width
result = result.faces(">Z").workplane().center(br_hole_x, br_hole_y).hole(center_hole_dia)

# Optional: Add fillets to vertical edges for aesthetics (not strictly visible but good practice)
# result = result.edges("|Z").fillet(0.5) 

# Export/Show
# show_object(result)