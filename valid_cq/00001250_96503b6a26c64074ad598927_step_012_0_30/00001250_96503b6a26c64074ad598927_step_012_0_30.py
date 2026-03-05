import cadquery as cq

# -----------------------------------------------------------------------------
# Parameters & Dimensions
# -----------------------------------------------------------------------------
plate_thk = 2.5
fillet_radius = 3.0

# Main central hole
main_hole_dia = 38.0

# Mounting tabs (ears)
ear_radius = 5.0
mtg_hole_dia = 4.2

# Boss details
boss_loc = (-45, 20)
boss_od = 14.0
boss_id = 8.0
boss_height = 6.0

# Rib details
rib_width = 3.0
rib_height = 4.0

# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------
def create_lobe(loc):
    """Creates a circular lobe (ear) at a specific location."""
    return (
        cq.Workplane("XY")
        .center(loc[0], loc[1])
        .circle(ear_radius)
        .extrude(plate_thk)
    )

# -----------------------------------------------------------------------------
# Geometry Construction
# -----------------------------------------------------------------------------

# 1. Define Key Locations (approximate based on image)
# Center is at (0,0)
pt_ears = {
    'tl': (-95, 15),   # Top Left
    'tm': (-45, 20),   # Top Mid (Boss location)
    'tr': (45, 20),    # Top Right
    'fr': (110, 0),    # Far Right Tip
    'br': (60, -20),   # Bottom Right
    'bm': (-10, -28),  # Bottom Mid
    'bl': (-95, -15)   # Bottom Left
}

# 2. Construct Base Plate Sections
# We split the plate into overlapping hulls to achieve the organic concave shape

# Center Disk (Hub)
center_hub = cq.Workplane("XY").circle(main_hole_dia/2 + 6).extrude(plate_thk)

# Left Arm: Hull of Left Ears, Mid Ears, and Center
left_features = (
    create_lobe(pt_ears['tl'])
    .union(create_lobe(pt_ears['bl']))
    .union(create_lobe(pt_ears['tm']))
    .union(create_lobe(pt_ears['bm']))
    .union(center_hub)
)
left_arm = left_features

# Right Arm: Hull of Center, Right Ears, and Far Tip
right_features = (
    center_hub
    .union(create_lobe(pt_ears['tr']))
    .union(create_lobe(pt_ears['br']))
    .union(create_lobe(pt_ears['fr']))
)
right_arm = right_features

# Combine Sections
base = left_arm.union(right_arm)

# 3. Refine Base Edges
# Fillet the vertical edges to blend the hulls smoothly
base = base.edges("|Z").fillet(fillet_radius)

# 4. Cuts (Holes and Slots)

# Main Central Hole
base = base.faces(">Z").workplane().circle(main_hole_dia/2).cutThruAll()

# Mounting Holes at all ear locations
for key, pt in pt_ears.items():
    base = base.faces(">Z").workplane().center(pt[0], pt[1]).circle(mtg_hole_dia/2).cutThruAll()

# Right side rectangular slot
base = base.faces(">Z").workplane().center(80, 0).rect(12, 6).cutThruAll()

# "Hook" / Flexure feature near center (modelled as a curved slot)
base = (
    base.faces(">Z")
    .workplane()
    .center(22, 12)
    .slot2D(12, 2.5, 45) # Length, Width, Angle
    .cutThruAll()
)

# 5. Add Raised Features

# Boss (Cylinder)
boss = (
    cq.Workplane("XY")
    .center(*boss_loc)
    .circle(boss_od/2)
    .extrude(plate_thk + boss_height)
)
# Boss Counterbore/Hole
boss = boss.faces(">Z").workplane().circle(boss_id/2).cutThruAll()

# Diagonal Rib
# Calculating a simple path from boss area to lower left area
rib_sketch = (
    cq.Workplane("XY")
    .moveTo(boss_loc[0], boss_loc[1])
    .lineTo(-90, -5)       # End point near bottom left
    .lineTo(-90, -5 + rib_width)
    .lineTo(boss_loc[0], boss_loc[1] + rib_width)
    .close()
    .extrude(plate_thk + rib_height * 0.6) # Rib height relative to plate
)

# Union features to base
result = base.union(boss).union(rib_sketch)

# Final edge refinement (optional chamfer/fillet on top edges)
# result = result.edges(">Z").fillet(0.5)