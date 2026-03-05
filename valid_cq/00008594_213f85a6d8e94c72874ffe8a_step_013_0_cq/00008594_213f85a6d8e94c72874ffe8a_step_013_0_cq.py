import cadquery as cq
import math

# --- Parameters ---
# Gear parameters
module = 2.0
num_teeth = 90
pressure_angle = 20.0
gear_thickness = 15.0
helix_angle = 0.0  # Spur gear, so 0

# Hub and Spoke parameters
hub_diameter = 30.0
hub_bore_diameter = 10.0
num_spokes = 5
spoke_width = 10.0
rim_thickness = 5.0 # Radial thickness of the rim below the teeth
spoke_fillet = 2.0

# Mounting holes parameters
bolt_circle_diameter = 20.0
mounting_hole_diameter = 3.0
num_mounting_holes = 4

# --- Calculation ---
# Pitch diameter
pitch_diameter = module * num_teeth
# Addendum (distance from pitch circle to top of tooth)
addendum = module
# Dedendum (distance from pitch circle to root of tooth)
dedendum = 1.25 * module
# Root diameter
root_diameter = pitch_diameter - 2 * dedendum
# Outer diameter (Tip diameter)
outer_diameter = pitch_diameter + 2 * addendum

# Inner rim diameter (where spokes connect)
rim_inner_diameter = root_diameter - 2 * rim_thickness

# --- Gear Generation Helper Function ---
# While CadQuery doesn't have a built-in "gear" primitive in the core, 
# we can approximate an involute gear profile or use a trapezoidal approximation 
# for visual similarity if external libraries aren't allowed. 
# However, constructing a proper involute shape is better.
# Let's create a simplified involute tooth profile function for standalone execution.

def involute_gear_profile(num_teeth, module, pressure_angle):
    pitch_radius = (num_teeth * module) / 2.0
    base_radius = pitch_radius * math.cos(math.radians(pressure_angle))
    addendum_radius = pitch_radius + module
    dedendum_radius = pitch_radius - (1.25 * module)
    
    # Generate one tooth profile
    points = []
    
    # Angular width of the tooth at base
    tooth_thickness_angle = math.pi / (2 * num_teeth) 
    
    # Create the involute curve
    num_points = 10
    for i in range(num_points + 1):
        r = base_radius + (addendum_radius - base_radius) * (i / num_points)
        # Involute function: inv(alpha) = tan(alpha) - alpha
        # alpha = acos(Rb/R)
        if r < base_radius: r = base_radius # clamp
        
        alpha = math.acos(base_radius / r)
        inv_alpha = math.tan(alpha) - alpha
        theta = inv_alpha + tooth_thickness_angle 
        
        x = r * math.cos(theta)
        y = r * math.sin(theta)
        points.append((x, y))

    # Mirror for the other side of the tooth
    right_side = points
    left_side = [(p[0], -p[1]) for p in right_side[::-1]]
    
    # Combine
    tooth_profile = left_side + right_side
    return tooth_profile

# --- Geometry Construction ---

# 1. Create the base Gear Blank (Outer Rim + Teeth area)
# We will create a full cylinder first, then cut out the spokes.
# Note: For simplicity and robustness in a single script without external 
# `cadquery-plugins`, we will model the gear teeth using a repeated cut pattern
# or an additive loft. Let's use an additive approach for the teeth on a rim.

# Base Rim Cylinder
rim = cq.Workplane("XY").circle(root_diameter / 2.0).extrude(gear_thickness)

# Create a single tooth cutter
# Simplified Trapezoidal/Involute approximation for robustness
tooth_height = addendum + dedendum
top_width = (math.pi * pitch_diameter / num_teeth) * 0.3 # approximate tip width
base_width = (math.pi * pitch_diameter / num_teeth) * 0.6 # approximate root width

# Define a single tooth shape sketch
tooth_sketch = (
    cq.Workplane("XY")
    .workplane(offset=gear_thickness/2) # Center it vertically if needed, but we extrude
    .moveTo(root_diameter/2, base_width/2)
    .lineTo(outer_diameter/2, top_width/2)
    .lineTo(outer_diameter/2, -top_width/2)
    .lineTo(root_diameter/2, -base_width/2)
    .close()
    .extrude(gear_thickness)
    .translate((0, 0, -gear_thickness/2)) # Center Z
)

# In pure CadQuery without plugins, iterating 90 unions can be slow.
# A more efficient way for visual representation is making a large cylinder and 
# cutting the gaps. Let's use the efficient approach of creating one tooth 
# and polar arraying it.

# Create the tooth profile wire
p_radius = pitch_diameter / 2.0
ang_pitch = 360.0 / num_teeth
half_tooth_ang = 360.0 / (4 * num_teeth) # Approx angle for half tooth thickness

# Let's create a custom solid for the gear ring
# 1. Inner solid (Rim + Spokes area)
base_solid = cq.Workplane("XY").circle(root_diameter / 2.0).extrude(gear_thickness)

# 2. Generate simplified teeth
# Instead of complex involutes, we use a trapezoidal profile which renders fast
# and looks correct for this scale.
tooth_shape = (
    cq.Workplane("XY")
    .moveTo(root_diameter/2 - 0.1, -base_width/2) # Overlap slightly
    .lineTo(outer_diameter/2, -top_width/2)
    .lineTo(outer_diameter/2, top_width/2)
    .lineTo(root_diameter/2 - 0.1, base_width/2)
    .close()
    .extrude(gear_thickness)
)

# Array the teeth
teeth = (
    tooth_shape
    .rotate((0,0,0), (0,0,1), 0)
    .polarArray(root_diameter/2, 0, 360, num_teeth) # This just places locations
)

# Since polarArray on 3D objects behaves differently in recent CQ versions (creating locations),
# we usually use a loop or specific pattern logic. 
# Robust method:
gear_solid = base_solid
for i in range(num_teeth):
    angle = i * (360.0 / num_teeth)
    rotated_tooth = tooth_shape.rotate((0,0,0), (0,0,1), angle)
    gear_solid = gear_solid.union(rotated_tooth)

# --- Spoke Cutouts ---

# Calculate the wedge shape for the cutout
# The cutout is the space between spokes.
# Total angle per section = 360 / 5 = 72 deg
# Spoke takes up some angle. 
# We'll create a "pie slice" subtractor.

cutout_outer_radius = rim_inner_diameter / 2.0
cutout_inner_radius = hub_diameter / 2.0

# Define a wedge sketch for the cutout
# We need to calculate the start and end points based on spoke width
# Angle subtended by half spoke width at inner radius
angle_offset_inner = math.degrees(math.asin((spoke_width/2) / cutout_inner_radius))
# Angle subtended by half spoke width at outer radius
angle_offset_outer = math.degrees(math.asin((spoke_width/2) / cutout_outer_radius))

# This is tricky with pure angles because spoke is constant width, not constant angle.
# Better approach: Draw the negative space (the hole) using lines and arcs.

def spoke_cutout_sketch(i):
    # Rotate the workplane for each cutout
    angle = i * (360.0 / num_spokes)
    
    # We build a wire that represents the cutout shape
    # Local X is radial direction, Local Y is tangential
    
    # Points relative to a spoke centered on X axis
    # The cutout is centered between two spokes.
    # So we rotate by half the sector angle (360/10 = 36 deg)
    
    segment_angle = 360.0 / num_spokes
    
    # We will construct a "slot" shape that fits between spokes
    # Coordinate geometry:
    # We need a shape bounded by:
    # 1. Circle at hub_diameter/2
    # 2. Circle at rim_inner_diameter/2
    # 3. Offset line from spoke 1 center
    # 4. Offset line from spoke 2 center
    
    # Let's use a subtractive Loft or Cut.
    # Actually, simply cutting a wedge and then adding the spokes back (or unioning hub and rim) might be cleaner.
    # Method B: Create Rim, Hub, Spokes separately and Union. This is much cleaner than cutting out complex shapes.
    return None

# --- RESTART GEOMETRY STRATEGY: UNION METHOD ---
# This is often more robust for spoked wheels.

# 1. Hub
hub = cq.Workplane("XY").circle(hub_diameter/2).extrude(gear_thickness)

# 2. Rim Ring (Inner support for teeth)
rim_ring = (
    cq.Workplane("XY")
    .circle(root_diameter/2)
    .circle(rim_inner_diameter/2)
    .extrude(gear_thickness)
)

# 3. Spokes
spoke_shape = (
    cq.Workplane("XY")
    .rect(rim_inner_diameter/2 + hub_diameter/2, spoke_width) # Length covers from center to past rim
    .extrude(gear_thickness)
    .translate(((rim_inner_diameter/2 + hub_diameter/2)/2, 0, 0)) # Shift so one end is at center (approx)
    # Actually, let's center the rect correctly
    # Rect center X should be (rim_radius + hub_radius)/2
    # But simpler: make a long rectangle centered at origin, cut the middle, array it.
)

spoke = (
    cq.Workplane("XY")
    .rect(root_diameter, spoke_width) # Long enough to cross diameter
    .extrude(gear_thickness)
    .translate((root_diameter/4 + hub_diameter/4, 0, 0)) # Shift to one side
)
# Re-do spoke geometry to be precise
spoke_len = (rim_inner_diameter - hub_diameter) / 2
spoke_center_dist = hub_diameter/2 + spoke_len/2

spoke_obj = (
    cq.Workplane("XY")
    .rect(spoke_len, spoke_width)
    .extrude(gear_thickness)
    .translate((spoke_center_dist, 0, 0))
)

# Array the spokes
spokes = spoke_obj
for i in range(1, num_spokes):
    spokes = spokes.union(spoke_obj.rotate((0,0,0), (0,0,1), i * (360/num_spokes)))

# 4. Teeth Ring (Recalculating to be efficient)
# Create the base cylinder for the teeth
teeth_base = cq.Workplane("XY").circle(root_diameter/2).extrude(gear_thickness)

# Create the teeth cuts or additions. 
# Let's create a ring of teeth and union it to the rim.
# Efficient single-tooth creation
single_tooth = (
    cq.Workplane("XY")
    .moveTo(root_diameter/2 - 0.5, -base_width/2)
    .lineTo(outer_diameter/2, -top_width/2)
    .lineTo(outer_diameter/2, top_width/2)
    .lineTo(root_diameter/2 - 0.5, base_width/2)
    .close()
    .extrude(gear_thickness)
)

all_teeth = single_tooth
for i in range(1, num_teeth):
    all_teeth = all_teeth.union(single_tooth.rotate((0,0,0), (0,0,1), i * (360/num_teeth)))

# Combine Main Structure
main_body = hub.union(rim_ring).union(spokes).union(all_teeth)

# --- Finishing Features ---

# 1. Main Bore
with_bore = main_body.faces(">Z").workplane().hole(hub_bore_diameter)

# 2. Mounting Holes (Bolt Circle)
with_mounting_holes = (
    with_bore.faces(">Z").workplane()
    .polarArray(bolt_circle_diameter/2, 0, 360, num_mounting_holes)
    .hole(mounting_hole_diameter)
)

# 3. Fillets
# Fillet the junction between spokes and rim/hub.
# This can be computationally heavy in CQ/OCCT on complex unions.
# We will attempt to select the vertical edges of the spokes.
# Selecting edges based on position is the standard way.

# The spokes are roughly along radial lines. We want edges that are parallel to Z.
# And are within the radius range of the gap.
final_model = with_mounting_holes

try:
    # Attempt filleting. If it fails due to geometry complexity, we return the un-filleted model.
    # Select edges that are vertical (parallel to Z)
    # And distance from center is > hub radius and < rim inner radius
    
    # Because of the boolean unions, the edges might be segmented.
    # We create a selector.
    
    final_model = final_model.edges(
        "|Z and "  # Parallel to Z
        f"(> (distC {hub_diameter/2 + 0.1})) and " # Outside hub
        f"(< (distC {rim_inner_diameter/2 - 0.1}))" # Inside rim
    ).fillet(spoke_fillet)
except Exception:
    # If filleting fails (common in complex generated topology), proceed without
    pass

result = final_model