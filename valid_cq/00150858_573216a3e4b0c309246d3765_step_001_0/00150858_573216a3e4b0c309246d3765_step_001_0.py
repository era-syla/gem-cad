import cadquery as cq

# --- Parametric Dimensions ---
# Shaft
shaft_diameter = 25.0
shaft_length = 90.0
bore_diameter = 15.0

# Stepped End
step_diameter = 20.0
step_length = 25.0

# Flange
flange_diameter = 55.0
flange_thickness = 10.0
recess_diameter = 38.0
recess_depth = 2.0
flange_cutout_radius = 12.0

# Mounting Holes
pcd = 42.0  # Pitch Circle Diameter
hole_diameter = 4.5
num_holes = 3  # Based on image visibility/pattern

# Boss Feature (Side Block)
boss_width = 8.0
boss_length = 15.0
boss_height = 6.0

# Internal Keyway
keyway_width = 5.0
keyway_depth = 2.5
keyway_length = 30.0

# --- Modeling ---

# 1. Base Geometry: Stacked Cylinders (Flange -> Shaft -> Step)
# Created along the Z-axis
flange = cq.Workplane("XY").circle(flange_diameter / 2.0).extrude(flange_thickness)

shaft = flange.faces(">Z").workplane().circle(shaft_diameter / 2.0).extrude(shaft_length)

stepped_end = shaft.faces(">Z").workplane().circle(step_diameter / 2.0).extrude(step_length)

# Combine into base body
body = stepped_end

# 2. Central Bore (Through All)
body = body.faces("<Z").workplane().circle(bore_diameter / 2.0).cutThruAll()

# 3. Flange Details
# A. Front Recess (Counterbore)
body = body.faces("<Z").workplane().circle(recess_diameter / 2.0).cutBlind(-recess_depth)

# B. Perimeter Cutout (The semi-circular bite)
# Placed at -X direction
body = body.faces("<Z").workplane().moveTo(-flange_diameter / 2.0, 0).circle(flange_cutout_radius).cutBlind(-flange_thickness)

# C. Mounting Holes
# Creating a pattern of 3 holes at 0, 90, 270 degrees (avoiding the cutout at 180/-X)
hole_locations = [
    (pcd / 2.0, 0),       # 0 degrees
    (0, pcd / 2.0),       # 90 degrees
    (0, -pcd / 2.0)       # 270 degrees
]
body = body.faces("<Z").workplane() \
    .pushPoints(hole_locations) \
    .circle(hole_diameter / 2.0) \
    .cutBlind(-flange_thickness)

# 4. Boss Feature
# A rectangular block protruding from the shaft near the step
# Position logic: Z = near end of main shaft, Y = extending from shaft surface
boss_z_pos = flange_thickness + shaft_length - boss_length
overlap = 1.0 # Material overlap to ensure valid union
boss_y_pos = (shaft_diameter / 2.0) + (boss_height / 2.0) - overlap

boss = cq.Workplane("XY").box(boss_width, boss_height + overlap, boss_length) \
    .translate((0, boss_y_pos, boss_z_pos + boss_length / 2.0))

result = body.union(boss)

# 5. Internal Keyway
# A rectangular slot cut into the bore wall
# Centered on Y axis, cutting radially outward
result = result.faces("<Z").workplane() \
    .moveTo(0, bore_diameter / 2.0) \
    .rect(keyway_width, keyway_depth * 2) \
    .cutBlind(keyway_length)

# Final Result
if 'show_object' in globals():
    show_object(result)