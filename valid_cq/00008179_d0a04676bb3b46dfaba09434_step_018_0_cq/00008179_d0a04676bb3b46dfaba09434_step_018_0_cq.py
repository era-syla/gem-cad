import cadquery as cq
import math

# --- Parametric Dimensions ---
# Standard-ish GT2 pulley dimensions for example purposes
tooth_count = 36          # Number of teeth
pitch = 2.0               # Pitch of the belt (e.g., GT2 uses 2mm)
pulley_width = 7.0        # Width of the toothed section
flange_width = 1.0        # Thickness of the side flanges
flange_extra_radius = 2.0 # How much larger the flange is than the pulley
bore_diameter = 5.0       # Center hole diameter
tooth_depth = 0.75        # Depth of the cut for the tooth
tooth_ratio = 0.5         # Ratio of tooth cut width to pitch

# Calculations
# Pitch Diameter = (Tooth Count * Pitch) / PI
pitch_diameter = (tooth_count * pitch) / math.pi
outer_radius = (pitch_diameter / 2.0) - 0.254 # Approx offset for GT2 pitch line
flange_radius = outer_radius + flange_extra_radius
total_width = pulley_width + (2 * flange_width)

# --- Geometry Construction ---

# 1. Create the main toothed cylinder body
# We start with the full cylinder representing the outer diameter
pulley_body = cq.Workplane("XY").circle(outer_radius).extrude(pulley_width)

# 2. Create the cutter for the teeth
# The profile of a timing belt tooth cut is roughly trapezoidal or rounded.
# For simplicity and standard parametric modeling, we'll use a trapezoidal cut here.
tooth_angle_width = (360.0 / tooth_count) * tooth_ratio
cut_width = (2 * math.pi * outer_radius) / tooth_count * tooth_ratio

# Define a single tooth cutter shape
# We create a shape on the side and extrude it
tooth_cutter = (
    cq.Workplane("XY")
    .workplane(offset=pulley_width/2) # Center vertically relative to body
    .moveTo(outer_radius, 0)
    .rect(tooth_depth * 2, cut_width) # Create a rectangle to cut
    .extrude(pulley_width * 1.5, both=True) # Extrude enough to cut through
)

# 3. Create the pattern of teeth
# We use polarArray to replicate the cutter around the center
# Note: cut operations inside a polarArray context can be tricky in pure fluent API,
# often easier to subtract a union of cutters.
cutters = (
    cq.Workplane("XY")
    .polarArray(outer_radius, 0, 360, tooth_count)
    .rect(tooth_depth * 2, cut_width) # Simple rectangular cut profile
    .extrude(pulley_width)
)

# Apply the cut to the main body
toothed_core = pulley_body.cut(cutters)

# 4. Create the flanges
# Top flange
flange_top = (
    cq.Workplane("XY")
    .workplane(offset=pulley_width)
    .circle(flange_radius)
    .extrude(flange_width)
)

# Bottom flange
flange_bottom = (
    cq.Workplane("XY")
    .workplane(offset=-flange_width)
    .circle(flange_radius)
    .extrude(flange_width)
)

# 5. Assemble the parts
# Union the core and the flanges
assembly = toothed_core.union(flange_top).union(flange_bottom)

# 6. Create the central bore
# Cut the hole through the entire assembly
result = assembly.faces(">Z").workplane().circle(bore_diameter / 2.0).cutThruAll()

# 7. (Optional refinement) Chamfer the bore for easier insertion
# result = result.faces(">Z or <Z").edges(cq.selectors.RadiusNthSelector(0)).chamfer(0.5)

# Export or display
if "show_object" in locals():
    show_object(result)