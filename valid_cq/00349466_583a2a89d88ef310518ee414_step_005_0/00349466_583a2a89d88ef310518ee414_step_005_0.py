import cadquery as cq

# --- Parameters ---
length = 220.0          # Distance between hole centers
small_boss_od = 34.0    # Outer diameter of the smaller (left) boss
small_boss_h = 24.0     # Height of the smaller boss
large_boss_od = 44.0    # Outer diameter of the larger (right) boss
large_boss_h = 50.0     # Height of the larger boss
beam_h = 16.0           # Thickness of the connecting beam
wall_t = 4.0            # Thickness of the flange/rim
web_t = 6.0             # Thickness of the central web
hole_dia = 16.0         # Diameter of the through holes
gusset_l = 45.0         # Length of the reinforcement rib on the right

# --- 1. Create the Main Beam (Arm) ---
# Define the outer shape using the hull of two circles
arm_sketch = (
    cq.Sketch()
    .circle(small_boss_od / 2.0)
    .moved(cq.Location(cq.Vector(length, 0, 0)))
    .circle(large_boss_od / 2.0)
    .hull()
)

# Extrude the solid arm block
arm = cq.Workplane("XY").placeSketch(arm_sketch).extrude(beam_h)

# --- 2. Create the Recess (Pocket) ---
# Create a smaller inner shape to cut away material, leaving a rim and web
pocket_sketch = (
    cq.Sketch()
    .circle((small_boss_od / 2.0) - wall_t)
    .moved(cq.Location(cq.Vector(length, 0, 0)))
    .circle((large_boss_od / 2.0) - wall_t)
    .hull()
)

# Cut the pocket from the top face downwards
# Depth is calculated to leave 'web_t' material at the bottom
pocket_depth = beam_h - web_t
arm_pocketed = arm.cut(
    cq.Workplane("XY")
    .workplane(offset=beam_h)
    .placeSketch(pocket_sketch)
    .extrude(-pocket_depth)
)

# --- 3. Create the Bosses ---
# Create the cylindrical ends. Adding these after the cut fills the pocket at the ends.
left_boss = cq.Workplane("XY").circle(small_boss_od / 2.0).extrude(small_boss_h)
right_boss = cq.Workplane("XY").center(length, 0).circle(large_boss_od / 2.0).extrude(large_boss_h)

# Apply a chamfer to the top of the tall boss to match the image style
right_boss = right_boss.edges(">Z").chamfer(3.0)

# Union the parts
result = arm_pocketed.union(left_boss).union(right_boss)

# --- 4. Create the Reinforcement Gusset ---
# A triangular rib connecting the beam web to the tall boss
gusset = (
    cq.Workplane("XZ")
    .center(length, 0)
    .polyline([
        (-large_boss_od/2.0, beam_h),                      # Start at beam/boss junction
        (-large_boss_od/2.0 - gusset_l, beam_h),           # Point along the beam
        (-large_boss_od/2.0, large_boss_h - 10.0),         # Point up the boss
        (-large_boss_od/2.0, beam_h)                       # Close loop
    ])
    .close()
    .extrude(web_t / 2.0, both=True)  # Symmetric extrusion
)

result = result.union(gusset)

# --- 5. Cut Holes ---
result = (
    result.faces(">Z").workplane()
    .circle(hole_dia / 2.0)
    .moveTo(length, 0)
    .circle(hole_dia / 2.0)
    .cutThruAll()
)

# --- 6. Fillets ---
# Add fillets to the vertical intersections for a realistic cast look
# Selecting edges that are approximately vertical and near the boss connections
try:
    result = result.edges("|Z").filterByPosition(lambda p: p.z < beam_h + 1).fillet(2.0)
except Exception:
    # Fallback if geometry is too complex for automatic filleting
    pass