import cadquery as cq
import math

# --- Parametric Dimensions ---
# Base Plate
plate_width = 100.0
plate_height = 100.0
plate_thickness = 3.0

# Cone Feature
cone_center_x = -25.0
cone_center_y = 0.0
cone_base_dia = 45.0
cone_top_dia = 22.0
cone_height = 30.0
cone_wall_thickness = 3.0

# Boss Feature (Ring)
boss_center_x = 25.0
boss_center_y = -10.0
boss_outer_dia = 20.0
boss_inner_dia = 16.0
boss_height = 6.0
boss_through_hole_dia = 12.0

# Small Holes Pattern
pattern_radius = 20.0
pattern_hole_dia = 4.0
pattern_angles = [45, 90, 135]  # Degrees relative to the boss center

# --- Geometry Construction ---

# 1. Create Base Plate
result = cq.Workplane("XY").box(plate_width, plate_height, plate_thickness)

# 2. Create the Large Cone (Lofted Solid)
# Define the base and top wires for the outer shell
result = result.faces(">Z").workplane().center(cone_center_x, cone_center_y) \
    .circle(cone_base_dia / 2.0) \
    .workplane(offset=cone_height) \
    .circle(cone_top_dia / 2.0) \
    .loft(combine=True)

# Create the hollow interior (Lofted Cut)
result = result.faces(">Z").workplane().center(cone_center_x, cone_center_y) \
    .circle((cone_base_dia / 2.0) - cone_wall_thickness) \
    .workplane(offset=cone_height) \
    .circle((cone_top_dia / 2.0) - cone_wall_thickness) \
    .loft(combine="cut")

# Cut the hole through the plate at the base of the cone
result = result.faces(">Z").workplane().center(cone_center_x, cone_center_y) \
    .circle((cone_base_dia / 2.0) - cone_wall_thickness) \
    .cutBlind(-plate_thickness * 2)

# 3. Create the Cylindrical Boss (Ring)
# Move to boss location
boss_wp = result.faces(">Z").workplane().center(boss_center_x, boss_center_y)

# Create the ring by defining two circles and extruding the area between them
result = boss_wp.circle(boss_outer_dia / 2.0).circle(boss_inner_dia / 2.0).extrude(boss_height)

# Cut the through-hole inside the boss
result = result.faces(">Z").workplane().center(boss_center_x, boss_center_y) \
    .circle(boss_through_hole_dia / 2.0).cutBlind(-plate_thickness * 2)

# 4. Create the Pattern of Small Holes
# We iterate through the angles to place holes relative to the boss center
for angle in pattern_angles:
    rad = math.radians(angle)
    # Calculate offset from the boss center
    x_off = pattern_radius * math.cos(rad)
    y_off = pattern_radius * math.sin(rad)
    
    # Absolute coordinates on the plate
    hole_x = boss_center_x + x_off
    hole_y = boss_center_y + y_off
    
    result = result.faces(">Z").workplane().center(hole_x, hole_y) \
        .circle(pattern_hole_dia / 2.0).cutBlind(-plate_thickness * 2)

# result now contains the final geometry