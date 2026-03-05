import cadquery as cq

# --- Parameter Definitions ---
plate_width = 100.0       # Width of the square plate
plate_thickness = 2.0     # Thickness of the bottom face
wall_height = 8.0         # Total height of the outer rim
wall_thickness = 2.0      # Thickness of the outer rim
center_hole_dia = 40.0    # Diameter of the large center hole

boss_outer_dia = 10.0     # Outer diameter of the corner bosses
boss_inner_dia = 5.0      # Inner diameter (hole) of the bosses
boss_height = 6.0         # Height of the bosses (from the inner floor)
boss_offset = 6.0         # Offset of boss center from the inner walls

# Derived dimensions
inner_width = plate_width - (2 * wall_thickness)
# Boss center position relative to the center of the plate
# Distance from center = (Inner width / 2) - offset
boss_center_dist = (inner_width / 2.0) - boss_offset 

# --- Modeling ---

# 1. Base Plate with Rim (using a shell operation or simple cuts)
# Method: Create a solid box, then shell it to create the walls and floor.
# Note: Since shell opens a face, we need to pick the top face.
base = (
    cq.Workplane("XY")
    .box(plate_width, plate_width, wall_height)
    .faces(">Z")
    .shell(-wall_thickness) # Negative thickness shells inwards
)

# However, shelling a box gives a uniform thickness everywhere. 
# The floor thickness matches the wall thickness. If independent control is needed:
# Let's do it with a subtraction for more parametric flexibility.

base_solid = cq.Workplane("XY").box(plate_width, plate_width, wall_height)

cutout_pocket = (
    cq.Workplane("XY")
    .workplane(offset=plate_thickness) # Start cut above the floor thickness
    .rect(plate_width - 2*wall_thickness, plate_width - 2*wall_thickness)
    .extrude(wall_height, combine=False) # Extrude up through the top
)

main_body = base_solid.cut(cutout_pocket)

# 2. Central Hole
main_body = (
    main_body.faces("<Z") # Select bottom face
    .workplane()
    .circle(center_hole_dia / 2.0)
    .cutThruAll()
)

# 3. Corner Bosses
# We define the positions for the 4 bosses
boss_locations = [
    (boss_center_dist, boss_center_dist),
    (boss_center_dist, -boss_center_dist),
    (-boss_center_dist, boss_center_dist),
    (-boss_center_dist, -boss_center_dist)
]

# Create the bosses on the "floor" of the inside
bosses = (
    main_body.faces(">Z").workplane(offset=-wall_height + plate_thickness)
    .pushPoints(boss_locations)
    .circle(boss_outer_dia / 2.0)
    .extrude(boss_height)
)

# Cut the holes in the bosses
# Note: The image shows holes going through the bosses. 
# Usually these are through-holes or blind holes. 
# Assuming through-holes for mounting screws based on typical usage.
result = (
    bosses.faces(">Z").workplane(offset=-wall_height + plate_thickness) # Reset to internal floor
    .pushPoints(boss_locations)
    .circle(boss_inner_dia / 2.0)
    .cutThruAll()
)

# Optional: Add the small extra hole seen near one edge if strict adherence to image is required.
# Looking closely at the bottom left quadrant, there is a small additional hole.
extra_hole_dia = 3.0
# Position estimate: midway along one side, slightly offset from rim
extra_hole_pos = (0, -(inner_width/2.0) + 4.0) 

result = (
    result.faces("<Z").workplane()
    .pushPoints([extra_hole_pos])
    .circle(extra_hole_dia / 2.0)
    .cutThruAll()
)

# If you want to fillet the boss connections to the wall (optional refinement)
# result = result.edges("|Z").fillet(0.5) 

# Export or visualization
if 'show_object' in globals():
    show_object(result)