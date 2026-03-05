import cadquery as cq

# Parameter definitions for the extrusion profile (e.g., generic 2020 aluminum profile)
length = 500.0         # Total length of the bar
profile_size = 20.0    # Width and Height of the cross-section
slot_width = 6.0       # Width of the longitudinal slot
slot_depth = 5.5       # Depth of the longitudinal slot
center_hole_dia = 5.0  # Diameter of the central hole
corner_radius = 1.5    # Fillet radius for the outer corners

# 1. Create the base solid block centered at the origin
# The box is created centered on X, Y, and Z axes
base = cq.Workplane("XY").box(profile_size, profile_size, length)

# 2. Fillet the outer longitudinal edges
# Select edges parallel to the Z axis ("|Z") to apply rounded corners
base = base.edges("|Z").fillet(corner_radius)

# 3. Create the central hole running through the entire length
# We select the top face (positive Z), create a workplane, and drill the hole
result = base.faces(">Z").workplane().hole(center_hole_dia, length)

# 4. Create the longitudinal slots (grooves) on all four sides
# We create cutter objects (boxes) and subtract them from the main body.

# Vertical cutter geometry (for Top and Bottom faces)
# Height is set to slot_depth * 2 to ensure it overlaps the edge fully for a clean cut
cutter_v = cq.Workplane("XY").box(slot_width, slot_depth * 2, length)

# Horizontal cutter geometry (for Left and Right faces)
cutter_h = cq.Workplane("XY").box(slot_depth * 2, slot_width, length)

# Position the cutters at the four faces of the profile
cut_top    = cutter_v.translate((0, profile_size / 2, 0))
cut_bottom = cutter_v.translate((0, -profile_size / 2, 0))
cut_right  = cutter_h.translate((profile_size / 2, 0, 0))
cut_left   = cutter_h.translate((-profile_size / 2, 0, 0))

# Combine all cutters into a single object for an efficient boolean operation
all_slots = cut_top.union(cut_bottom).union(cut_right).union(cut_left)

# Subtract the slots from the main body
result = result.cut(all_slots)