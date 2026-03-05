import cadquery as cq

# Parameters for the 2080 Aluminum Extrusion profile
length = 400.0  # Length of the extrusion
width = 20.0    # Width of the profile
height = 80.0   # Height of the profile (4x 20mm units)
fillet_radius = 1.0 # External corner radius

# Derived parameters
w_half = width / 2.0
h_half = height / 2.0
# Y-coordinates for the centers of the four 20x20 sub-units
unit_centers = [-30.0, -10.0, 10.0, 30.0]
# Y-coordinates for the separator grooves between units
groove_centers = [-20.0, 0.0, 20.0]

# 1. Create the base solid block
# We create a box centered at the origin
base = cq.Workplane("XY").box(width, height, length)

# Round the vertical edges (which run along Z)
result = base.edges("|Z").fillet(fillet_radius)

# 2. Cut the center bores
# Standard 5mm holes (approx for tapping M5 or clearance) through the center of each unit
result = (
    result.faces(">Z").workplane()
    .pushPoints([(0, y) for y in unit_centers])
    .circle(2.5) # 5mm diameter
    .cutThruAll()
)

# 3. Define the T-Slot Cutter Geometry
# We define a generic T-slot profile 2D shape.
# Coordinates assume the slot opens at y=0 and extends into negative Y.
# Shape is a simplified V-slot/T-slot profile.
slot_pts = [
    (-3.0, 0.0),    # Top left opening
    (-3.0, -1.5),   # Neck down
    (-5.0, -2.5),   # Angled out
    (-5.0, -6.0),   # Bottom left
    (5.0, -6.0),    # Bottom right
    (5.0, -2.5),    # Angled in
    (3.0, -1.5),    # Neck up
    (3.0, 0.0),     # Top right opening
    (-3.0, 0.0)     # Close loop
]

# Create a long cutter solid for the slots
# Make it slightly longer than the main part to ensure clean cuts
cutter_len = length + 20.0
slot_wire = cq.Workplane("XY").polyline(slot_pts).close()
slot_cutter_base = slot_wire.extrude(cutter_len).translate((0, 0, -cutter_len/2))

# 4. Define Separator Groove Cutter Geometry
# Small V-grooves separating the 20mm sections visually
groove_pts = [(-0.6, 0.0), (0.0, -0.8), (0.6, 0.0), (-0.6, 0.0)]
groove_wire = cq.Workplane("XY").polyline(groove_pts).close()
groove_cutter_base = groove_wire.extrude(cutter_len).translate((0, 0, -cutter_len/2))

# 5. Position and Apply Cutters
cutters = []

# -- T-Slots on the Short Faces (Top and Bottom) --
# Top Face (Y = +40)
cutters.append(
    slot_cutter_base.translate((0, h_half, 0))
)
# Bottom Face (Y = -40) - Rotate 180 to point up
cutters.append(
    slot_cutter_base.rotate((0,0,0), (0,0,1), 180).translate((0, -h_half, 0))
)

# -- T-Slots on the Long Faces (Left and Right) --
# Right Face (X = +10) - Rotate -90 to point left (into -X)
cutter_right = slot_cutter_base.rotate((0,0,0), (0,0,1), -90)
for y in unit_centers:
    cutters.append(cutter_right.translate((w_half, y, 0)))

# Left Face (X = -10) - Rotate 90 to point right (into +X)
cutter_left = slot_cutter_base.rotate((0,0,0), (0,0,1), 90)
for y in unit_centers:
    cutters.append(cutter_left.translate((-w_half, y, 0)))

# -- Grooves on the Long Faces --
# Right Face Grooves
groove_right = groove_cutter_base.rotate((0,0,0), (0,0,1), -90)
for y in groove_centers:
    cutters.append(groove_right.translate((w_half, y, 0)))

# Left Face Grooves
groove_left = groove_cutter_base.rotate((0,0,0), (0,0,1), 90)
for y in groove_centers:
    cutters.append(groove_left.translate((-w_half, y, 0)))

# Apply all cuts to the main object
for cutter in cutters:
    result = result.cut(cutter)
