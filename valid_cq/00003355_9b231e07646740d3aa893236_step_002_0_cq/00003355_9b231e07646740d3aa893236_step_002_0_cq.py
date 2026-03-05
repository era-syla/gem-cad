import cadquery as cq
import math

# --- Parameters ---
outer_diameter = 100.0
total_height = 25.0
wall_thickness = 8.0
floor_thickness = 4.0

# Rim details
rim_inset = 4.0
rim_depth = 4.0  # Depth of the little step inside the rim

# Center boss details
center_boss_diameter = 30.0
center_boss_height = 12.0
boss_chamfer = 3.0  # The conical top section

# Internal lugs details
lug_count = 8
lug_width = 10.0
lug_depth = 8.0  # Radial depth
lug_height = 8.0  # Height from floor
lug_radial_position = (outer_diameter / 2) - wall_thickness  # Positioned against the inner wall

# --- Modeling ---

# 1. Create the main cylindrical cup
# Start with a solid cylinder
main_body = cq.Workplane("XY").circle(outer_diameter / 2).extrude(total_height)

# Create the inner cavity (leaving floor and walls)
inner_diameter = outer_diameter - (2 * wall_thickness)
main_body = main_body.faces(">Z").workplane().hole(inner_diameter, total_height - floor_thickness)

# 2. Create the Rim/Step Feature
# We need to cut a step into the top of the wall.
# Based on the image, there is an outer ring, then a step down, then the inner wall.
# Actually, looking closely, it looks like the wall thickness is constant, but there is a 
# groove or step cut into the top face.
# Let's cut a ring out of the top face.
cut_outer_r = (outer_diameter / 2) - 2.0 # Thin outer lip
cut_inner_r = (outer_diameter / 2) - rim_inset
main_body = (main_body.faces(">Z").workplane()
             .circle(cut_outer_r)
             .circle(cut_inner_r)
             .cutBlind(-rim_depth))

# 3. Create the Central Boss
# It's a cylinder with a chamfered top.
boss = (cq.Workplane("XY")
        .workplane(offset=floor_thickness) # Start on top of the floor
        .circle(center_boss_diameter / 2)
        .extrude(center_boss_height))

# Apply the heavy chamfer to the top edge of the boss
boss = boss.faces(">Z").edges().chamfer(boss_chamfer)

# Unite boss with main body
result = main_body.union(boss)

# 4. Create the Internal Lugs
# These are rectangular blocks arranged radially against the inner wall.
# We'll create one and polar array it.

# Define the single lug shape
lug = (cq.Workplane("XY")
       .workplane(offset=floor_thickness) # Start on the floor
       .box(lug_depth, lug_width, lug_height, centered=(True, True, False)))

# Move the lug to the correct radial position
# We want the outer face of the lug to touch the inner wall.
# Inner radius is inner_diameter / 2
# Lug center needs to be at (Inner Radius - Lug Depth / 2)
lug_r_center = (inner_diameter / 2) - (lug_depth / 2)
lug = lug.translate((lug_r_center, 0, 0))

# Create the pattern of lugs
lugs = (cq.Workplane("XY")
        .polarArray(lug_r_center, 0, 360, lug_count)
        .eachpoint(lambda loc: lug.val().located(loc)))

# Union the lugs to the main body
result = result.union(lugs)

# Optional: Add small fillets to the bottom floor edges for realism (not strictly visible but good practice)
# result = result.faces("<Z").edges().fillet(1.0) 

# Export/Return
if __name__ == "__main__":
    # If running in an environment that supports show_object (like CQ-editor)
    try:
        show_object(result)
    except NameError:
        pass