import cadquery as cq
import math

# --- Parametric Dimensions ---
# Overall dimensions
height = 20.0
outer_diameter = 20.0  # Diameter at the tips of the 'teeth'
inner_diameter = 14.0  # Diameter at the base of the 'valleys'
num_teeth = 6
tooth_width_deg = 30.0 # Angular width of each tooth in degrees

# Internal features
hex_width_across_flats = 10.0 # Standard size for a hex key/nut
hex_depth = 12.0
through_hole_diameter = 5.0

# --- Geometry Construction ---

# 1. Create the base cylinder for the "valleys"
# This forms the core diameter of the part
core = cq.Workplane("XY").circle(inner_diameter / 2.0).extrude(height)

# 2. Create the "teeth" or lugs
# We'll create one tooth profile and polar array it
# The tooth is a sector of an annulus
tooth_thickness = (outer_diameter - inner_diameter) / 2.0
tooth_radius = outer_diameter / 2.0

# We sketch the tooth on the XY plane.
# It's an arc segment.
def create_tooth_sketch(radius, width_deg):
    angle_rad = math.radians(width_deg)
    # Calculate key points for the arc
    x_pos = radius * math.cos(angle_rad / 2)
    y_pos = radius * math.sin(angle_rad / 2)
    
    # We construct a closed profile: center -> arc -> center
    # But a simpler way in CQ is to make a wedge or use intersect.
    # Let's try extruding a rectangle and intersecting with a cylinder, 
    # or rotating a rectangle. 
    
    # Alternative approach: Sketch a trapezoid/wedge shape for the tooth
    # A cleaner way given the curved outer face is to use a polar array of a basic shape
    # and then cut or intersect, but let's build additively.
    
    # Let's make a wedge shape using a Workplane with a width
    return (
        cq.Workplane("XY")
        .polarArray(radius, 0, 360, 1) # Dummy for context, not strictly needed
        .moveTo(inner_diameter/2, 0)
        .rect((outer_diameter - inner_diameter)/2, 5) # Placeholder strategy
    )

# Better Strategy for Teeth:
# Create a large cylinder (outer diameter).
# Create "cutter" shapes to remove material to form the valleys.
# The valleys are gaps between the teeth.
total_angle = 360.0
gap_angle = (total_angle - (num_teeth * tooth_width_deg)) / num_teeth

# Start with the full outer cylinder
outer_body = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(height)

# Create a cutter for the gaps
# A gap is a segment of the annulus that needs to be removed.
# A simple way to cut the gaps is to use rectangular cuts rotated around the center
# or pie-wedge cuts.
# Let's use a "pie slice" cutter.
cutter_radius = outer_diameter / 2.0 + 1.0 # slightly larger to ensure clean cut
cutter_inner_radius = inner_diameter / 2.0

# To make a proper gap cutter that leaves a curved inner wall (the core),
# we can make a ring and cut slots, but let's stick to the additive + subtractive logic.

# Refined Strategy:
# 1. Base Cylinder (Outer Dia)
# 2. Cut "Slots" to create the teeth pattern.
#    A slot is defined by the space between teeth.
slot_width_deg = 360.0/num_teeth - tooth_width_deg

# We will create a sketch that represents the material to be REMOVED (the valleys).
# The shape to remove is an annular sector.
# However, CadQuery doesn't have a direct "annular sector extrude" primitive easily accessible
# without custom vertices.
# An easier geometric approach:
# 1. Create Cylinder(inner_diameter) -> The core.
# 2. Create Cylinder(outer_diameter) -> The outer ring.
# 3. Cut the outer ring with rectangular or wedge shapes to leave the teeth.
#    OR: Create rectangular blocks and intersect them with the outer cylinder.

# Let's go with: Core Cylinder + (Rectangular Blocks INTERSECT Outer Cylinder)
core = cq.Workplane("XY").circle(inner_diameter / 2.0).extrude(height)

# Create a block representing a tooth before it is curved
# The width of the block can be calculated from the chord length or just made wide enough.
# We want the side walls to be radial? The image shows radial side walls (pointing to center).
# If walls are radial, we need wedge shapes.

# Let's construct a custom profile for a single tooth and extrude it.
# Points for a single tooth sector:
# (r_in, -angle/2), (r_out, -angle/2), (r_out, +angle/2), (r_in, +angle/2)
pts = []
half_angle = math.radians(tooth_width_deg / 2.0)
r_in = inner_diameter / 2.0
r_out = outer_diameter / 2.0

# Define points in polar, convert to Cartesian
pts.append((r_in * math.cos(-half_angle), r_in * math.sin(-half_angle)))
pts.append((r_out * math.cos(-half_angle), r_out * math.sin(-half_angle)))
# We need an arc for the outer edge to match the image perfectly
# CQ polyline with arc support is best.
mid_angle = 0
p_mid_out = (r_out * math.cos(mid_angle), r_out * math.sin(mid_angle))
p_top_out = (r_out * math.cos(half_angle), r_out * math.sin(half_angle))
p_top_in = (r_in * math.cos(half_angle), r_in * math.sin(half_angle))
# Inner arc? The image shows the inner part connects to the core cylinder perfectly.
# So the inner edge of the tooth is just an arc matching the core.

# Single tooth profile
tooth_sketch = (
    cq.Workplane("XY")
    .moveTo(pts[0][0], pts[0][1])
    .lineTo(pts[1][0], pts[1][1])
    .threePointArc(p_mid_out, p_top_out)
    .lineTo(p_top_in[0], p_top_in[1])
    .close() # Close back to start, straight line (chord) is fine because it's buried in the core
)

# Extrude one tooth
single_tooth = tooth_sketch.extrude(height)

# Array the teeth
teeth = (
    single_tooth
    .rotate((0,0,0), (0,0,1), 360/num_teeth) # Offset to align if needed, but array handles it
    .rotate((0,0,0), (0,0,1), -360/num_teeth) # Reset
)

# Actually, simply using polarArray on the Workplane BEFORE extruding is much more efficient
teeth_compound = (
    cq.Workplane("XY")
    .moveTo(pts[0][0], pts[0][1])
    .lineTo(pts[1][0], pts[1][1])
    .threePointArc(p_mid_out, p_top_out)
    .lineTo(p_top_in[0], p_top_in[1])
    .close()
    .extrude(height)
)

# Now we pattern this solid
final_teeth = teeth_compound
for i in range(1, num_teeth):
    final_teeth = final_teeth.union(teeth_compound.rotate((0,0,0), (0,0,1), i * (360/num_teeth)))

# Combine core and teeth
body = core.union(final_teeth)

# 3. Create the Hexagonal Recess (Socket)
# Create a polygon and cut
hex_cut = (
    cq.Workplane("XY")
    .workplane(offset=height) # Work on top face
    .polygon(6, hex_width_across_flats / math.cos(math.radians(30)), circumscribed=False) 
    # Logic check: 'width across flats' usually determines size. 
    # circumscribed=True takes radius (center to corner).
    # circumscribed=False takes apothem (center to flat).
    # CQ polygon takes diameter/radius depending on implementation.
    # CQ documentation: polygon(nSides, diameter, circumscribed=False)
    # diameter means outer diameter usually? 
    # Actually for CQ, diameter implies the circle that defines the polygon.
    # If circumscribed=True (default), the polygon is inside the circle (diameter = corner-to-corner).
    # If circumscribed=False, the polygon surrounds the circle (diameter = flat-to-flat).
    # We want flat-to-flat = 10.0. So we use a circle of diameter 10.0 and circumscribed=True? 
    # Wait, if circumscribed=True, polygon is INSIDE circle. 
    # So circle dia = corner-to-corner distance.
    # We have flat-to-flat distance (W). 
    # W = 2 * r_inscribed. 
    # If circumscribed=False, diameter argument is the inscribed diameter (flat-to-flat).
    .polygon(6, hex_width_across_flats, circumscribed=False) 
    .extrude(-hex_depth)
)

# 4. Create Through Hole
# Centered hole through the bottom of the hex
hole_cut = (
    cq.Workplane("XY")
    .circle(through_hole_diameter / 2.0)
    .extrude(height) # Cut through everything
)

# Apply cuts
result = body.cut(hex_cut).cut(hole_cut)

# Clean up redundant variable for final output standard
result = result