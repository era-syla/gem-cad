import cadquery as cq

# --- Parameters ---
# Box dimensions
length = 160.0
width = 60.0
height = 30.0
wall_thickness = 2.0
floor_thickness = 2.0

# Mounting Boss dimensions
boss_diameter = 6.0
boss_hole_diameter = 2.6  # Sized for tapping (e.g., M3)
boss_height = 6.0         # Height of boss from the interior floor

# Boss positioning (centered pattern)
boss_spacing_x = 100.0    # Distance between bosses along length
boss_spacing_y = 30.0     # Distance between bosses along width

# --- Modeling ---

# 1. Create the Base Block
# Aligned so Z=0 is the bottom of the box
result = cq.Workplane("XY").box(length, width, height, centered=(True, True, False))

# 2. Shell/Hollow the Box
# Select the top face (Z=height) and cut downwards leaving wall/floor thickness
# The depth of the cut is total height minus the desired floor thickness
cut_depth = height - floor_thickness

result = (
    result
    .faces(">Z")                         # Select top face
    .workplane()                         # Create workplane on top face
    .rect(length - 2 * wall_thickness,   # Inner rectangle width
          width - 2 * wall_thickness)    # Inner rectangle height
    .cutBlind(-cut_depth)                # Cut down into the block
)

# 3. Add Mounting Bosses
# Define boss locations
boss_locations = [
    (boss_spacing_x / 2, boss_spacing_y / 2),
    (boss_spacing_x / 2, -boss_spacing_y / 2),
    (-boss_spacing_x / 2, boss_spacing_y / 2),
    (-boss_spacing_x / 2, -boss_spacing_y / 2)
]

# The current workplane is at the top of the box (Z=height).
# We move the workplane down to the interior floor level to start the bosses.
# Offset needs to be negative relative to the top face normal (+Z).
result = (
    result
    .workplane(offset=-cut_depth)        # Move plane to interior floor (Z=floor_thickness)
    .pushPoints(boss_locations)          # Place points
    .circle(boss_diameter / 2)           # Draw boss footprints
    .extrude(boss_height)                # Extrude upwards
)

# 4. Create Holes in Bosses
# Move workplane to the top of the bosses to cut holes
result = (
    result
    .workplane(offset=boss_height)       # Move plane to top of bosses
    .pushPoints(boss_locations)          # Use same locations
    .circle(boss_hole_diameter / 2)      # Draw hole profiles
    .cutBlind(-boss_height)              # Cut downwards through the boss
)