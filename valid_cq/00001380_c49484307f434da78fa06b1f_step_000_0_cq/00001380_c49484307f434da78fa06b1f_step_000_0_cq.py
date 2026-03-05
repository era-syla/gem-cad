import cadquery as cq

# --- Parameters ---
plate_width = 80.0       # Width of the square plate
plate_thickness = 4.0    # Thickness of the base plate
corner_radius = 8.0      # Radius of the rounded corners

boss_height = 8.0        # Height of the mounting bosses (from bottom of plate)
boss_diameter = 10.0     # Outer diameter of the bosses
boss_hole_diameter = 5.0 # Inner diameter of the boss holes
boss_offset = 5.0        # Offset from the edge to the center of the boss (calculated below)

hex_hole_diameter = 35.0 # Diameter of the circumcircle of the hexagon

# Calculate boss position relative to center
# If plate is 80 wide, center to edge is 40.
# If boss is centered on the fillet radius or slightly inset, 
# let's assume boss centers are at the corners of a square pattern.
# Looking at the image, the boss center seems to align with the corner radius center.
boss_center_dist = (plate_width / 2) - corner_radius

# --- Geometry Construction ---

# 1. Base Plate with rounded corners
base_plate = (
    cq.Workplane("XY")
    .rect(plate_width, plate_width)
    .extrude(plate_thickness)
    .edges("|Z")
    .fillet(corner_radius)
)

# 2. Hexagonal Cutout
hex_cutout = (
    base_plate.faces(">Z")
    .workplane()
    .polygon(6, hex_hole_diameter)
    .cutThruAll()
)

# 3. Mounting Bosses (Cylinders)
# Define the locations for the 4 corners
boss_locations = [
    (boss_center_dist, boss_center_dist),
    (boss_center_dist, -boss_center_dist),
    (-boss_center_dist, boss_center_dist),
    (-boss_center_dist, -boss_center_dist),
]

# Add the bosses on top of the plate
plate_with_bosses = (
    hex_cutout.faces(">Z")
    .workplane()
    .pushPoints(boss_locations)
    .circle(boss_diameter / 2)
    .extrude(boss_height)
)

# 4. Boss Holes
# Cut holes through the bosses and the plate
result = (
    plate_with_bosses.faces(">Z")
    .workplane()
    .pushPoints(boss_locations)
    .circle(boss_hole_diameter / 2)
    .cutThruAll()
)

# If running in an environment that supports show_object (like CQ-Editor), display it
# show_object(result)