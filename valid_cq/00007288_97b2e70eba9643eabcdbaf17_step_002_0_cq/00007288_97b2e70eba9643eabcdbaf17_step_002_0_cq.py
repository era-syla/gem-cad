import cadquery as cq

# --- Parameters ---
# Standard bearing dimensions (approximate for a common size like 608 or similar)
outer_diameter = 22.0
inner_diameter = 8.0
width = 7.0

# Detail dimensions
outer_race_thickness = 2.5
inner_race_thickness = 2.5
seal_recess_depth = 0.5  # How far down the seal sits
seal_groove_width = 1.0  # Width of the gap for the seal
chamfer_size = 0.4       # Edge chamfer

# Calculated internal values
radius_outer = outer_diameter / 2.0
radius_inner = inner_diameter / 2.0
radius_mid = (radius_outer + radius_inner) / 2.0

# --- Construction ---

# 1. Outer Race
# Cylinder for outer boundary
outer_race = cq.Workplane("XY").circle(radius_outer).extrude(width)
# Cut the center hole for the "guts" of the bearing
outer_race_id = radius_outer - outer_race_thickness
outer_race = outer_race.cut(
    cq.Workplane("XY").circle(outer_race_id).extrude(width)
)

# 2. Inner Race
# Cylinder for inner race body
inner_race_od = radius_inner + inner_race_thickness
inner_race = cq.Workplane("XY").circle(inner_race_od).extrude(width)
# Cut the actual bore hole
inner_race = inner_race.cut(
    cq.Workplane("XY").circle(radius_inner).extrude(width)
)

# 3. Seal / Shield
# The seal sits between the races, slightly recessed.
# It usually doesn't touch the inner race in the simplified CAD representation of a shielded bearing, 
# or touches lightly. We'll make a solid ring.
seal_outer_r = outer_race_id - 0.1 # Slight tolerance gap visually
seal_inner_r = inner_race_od + 0.1 # Slight tolerance gap visually
seal_thickness = 0.5 # Thickness of the seal plate itself

# Create one seal plate
seal = cq.Workplane("XY") \
    .workplane(offset=width - seal_recess_depth - seal_thickness) \
    .circle(seal_outer_r) \
    .circle(seal_inner_r) \
    .extrude(seal_thickness)

# Create the bottom seal (mirror or new extrusion)
seal_bottom = cq.Workplane("XY") \
    .workplane(offset=seal_recess_depth) \
    .circle(seal_outer_r) \
    .circle(seal_inner_r) \
    .extrude(seal_thickness)

# 4. Assembly & Finishing
# Combine the parts
bearing = outer_race.union(inner_race).union(seal).union(seal_bottom)

# Apply Chamfers to the outer edges of the races (standard bearing feature)
# Outer race outer edges
bearing = bearing.edges(
    cq.selectors.RadiusNthSelector(0) # Select outer cylinder edges
).chamfer(chamfer_size)

# Inner race inner edges (the bore)
# We need to be careful selecting edges. Let's select edges at the Z min/max faces 
# that have the specific inner radius.
bearing = bearing.edges(
    cq.selectors.RadiusNthSelector(-1) # Select the smallest radius cylinder (the bore)
).chamfer(chamfer_size)


# Optional: Add the small characteristic grooves often seen on the seal/race interface
# This is purely aesthetic to match the image's "stepped" look on the inner race lip
inner_lip_cut = cq.Workplane("XY") \
    .workplane(offset=width - seal_recess_depth + 0.1) \
    .circle(inner_race_od + 0.2) \
    .circle(inner_race_od - 0.5) \
    .extrude(-1.0) # Cut downwards a bit

bearing = bearing.cut(inner_lip_cut)

# Do the same for bottom
inner_lip_cut_bottom = cq.Workplane("XY") \
    .workplane(offset=seal_recess_depth - 0.1) \
    .circle(inner_race_od + 0.2) \
    .circle(inner_race_od - 0.5) \
    .extrude(1.0) 

bearing = bearing.cut(inner_lip_cut_bottom)

result = bearing