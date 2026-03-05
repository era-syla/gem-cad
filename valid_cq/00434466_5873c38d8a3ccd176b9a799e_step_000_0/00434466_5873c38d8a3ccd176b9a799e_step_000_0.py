import cadquery as cq

# --- Parameter Definitions ---
# Main Arm Dimensions
arm_length = 170.0      # Length of the straight horizontal section
arm_height = 34.0       # Height of the profile (side view)
curve_rise = 120.0      # Vertical height of the curve tip
curve_reach = 75.0      # Horizontal position of the curve tip relative to elbow
thickness_main = 14.0   # Thickness of the thinner web section
thickness_rib = 22.0    # Thickness of the reinforced rib section
rib_inset = 5.0         # Indentation of the rib from the edge profile
rib_start_x = -45.0     # X-coordinate where the rib reinforcement begins

# Boss/Pivot Dimensions
# Bottom Pivot (Junction)
boss_bot_od = 34.0
boss_bot_id = 24.0
boss_bot_width = 32.0

# Top Pivot (Tip)
boss_top_od = 28.0
boss_top_id = 18.0
boss_top_width = 32.0

# --- Geometry Construction ---

# 1. Main Beam Profile (The underlying web)
# Define points
p_tip = (-arm_length, 0)
p_elbow = (0, 0)
p_top = (curve_reach, curve_rise)

# Create the centerline path
path_main = (
    cq.Workplane("XY")
    .moveTo(*p_tip)
    .lineTo(*p_elbow)
    .tangentArcPoint(p_top, relative=False)
)

# Create the 2D profile with rounded ends (stadium shape) using offset
profile_main = path_main.toPending().offset2D(arm_height / 2.0, kind='arc')

# Extrude the main body centered on Z
body_main = profile_main.extrude(thickness_main).translate((0, 0, -thickness_main/2.0))

# 2. Reinforcement Rib (The raised central spine)
# The rib starts partway along the beam and follows the curve
path_rib = (
    cq.Workplane("XY")
    .moveTo(rib_start_x, 0)
    .lineTo(*p_elbow)
    .tangentArcPoint(p_top, relative=False)
)

# Create rib profile (inset from main profile)
profile_rib = path_rib.toPending().offset2D(arm_height / 2.0 - rib_inset, kind='arc')

# Extrude rib thicker than main body
body_rib = profile_rib.extrude(thickness_rib).translate((0, 0, -thickness_rib/2.0))

# 3. Bosses (Cylindrical Pivots)
# Bottom Boss at the elbow (0,0)
boss_bot = (
    cq.Workplane("XY")
    .circle(boss_bot_od / 2.0)
    .extrude(boss_bot_width)
    .translate((0, 0, -boss_bot_width / 2.0))
)

# Top Boss at the tip of the curve
# Modeled with a slight loft for a tapered/cast look
boss_top = (
    cq.Workplane("XY")
    .workplane(offset=-boss_top_width / 2.0)
    .center(*p_top)
    .circle(boss_top_od / 2.0 + 1.0)  # Slightly wider base
    .workplane(offset=boss_top_width)
    .circle(boss_top_od / 2.0)        # Normal top
    .loft()
)

# 4. Combine Shapes
# Union main body, rib, and bosses
result = body_main.union(body_rib).union(boss_bot).union(boss_top)

# 5. Machining / Detail Features
# Cut the through-holes for the pivots
result = (
    result
    .faces(">Z")
    .workplane()
    .moveTo(0, 0).circle(boss_bot_id / 2.0).cutThruAll()
    .moveTo(*p_top).circle(boss_top_id / 2.0).cutThruAll()
)

# 6. Fillets and Finishing
# Blend the start of the rib into the main beam smoothly
# Select vertical edges near the rib start position
try:
    rib_start_edges = result.edges(cq.selectors.BoxSelector(
        (rib_start_x - 1, -arm_height, -50), 
        (rib_start_x + 1, arm_height, 50)
    ))
    result = result.fillet(10.0, rib_start_edges)
except:
    pass # Skip if selection fails (robustness)

# Apply generic edge fillets to smooth the cast part
# Fillet vertical edges (Z-parallel)
result = result.edges("|Z").fillet(1.5)

# Fillet the edges where the boss meets the arm faces (approximate selection)
# This adds realism to the "welded" or "cast" intersections
result = result.edges(cq.selectors.NearestToPointSelector((0, 0, boss_bot_width/2))).fillet(2.0)