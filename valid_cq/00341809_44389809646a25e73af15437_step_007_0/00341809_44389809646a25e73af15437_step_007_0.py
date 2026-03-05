import math
import cadquery as cq

# --- Parameters ---
chord = 100.0             # Length of the airfoil chord
span = 300.0              # Length of the extrusion
thickness_ratio = 0.18    # NACA 0018 (18% thickness)
wall_thickness = 2.0      # Thickness of the hollow shell
groove_depth = 0.5        # Depth of the surface cuts
groove_width = 2.0        # Width of the groove lines
groove_gap = 5.0          # Spacing between the pair of grooves
margin_end = 30.0         # Distance from ends to the first groove

# --- Helper Function: NACA 4-Digit Series Generator ---
def naca4_symmetric_points(c, t, n=100):
    """
    Generate points for a symmetric NACA 4-digit airfoil.
    c: Chord length
    t: Thickness-to-chord ratio (e.g., 0.12 for NACA 0012)
    n: Number of points per side
    """
    points = []
    
    # Upper surface (Leading Edge to Trailing Edge)
    for i in range(n + 1):
        x = (i / n) * c
        # Avoid sqrt(0) error, though math.sqrt(0) is 0
        if x < 0: x = 0
        xc = x / c
        yt = 5 * t * c * (
            0.2969 * math.sqrt(xc) -
            0.1260 * xc -
            0.3516 * xc**2 +
            0.2843 * xc**3 -
            0.1015 * xc**4
        )
        points.append((x, yt))
        
    # Lower surface (Trailing Edge back to Leading Edge)
    for i in range(n - 1, -1, -1):
        x = (i / n) * c
        xc = x / c
        yt = 5 * t * c * (
            0.2969 * math.sqrt(xc) -
            0.1260 * xc -
            0.3516 * xc**2 +
            0.2843 * xc**3 -
            0.1015 * xc**4
        )
        points.append((x, -yt))
        
    return points

# --- Geometry Construction ---

# 1. Create Base Profile
pts = naca4_symmetric_points(chord, thickness_ratio)
# Create the outer wire on the XY plane
outer_wire = cq.Workplane("XY").polyline(pts).close()

# 2. Main Extrusion
# Extrude the full solid airfoil
main_body = outer_wire.extrude(span)

# 3. Create Hollow Shell
# Generate an inner profile by offsetting the outer wire inwards
# offset2D handles the complex curvature
inner_wire_wp = outer_wire.wires().toPending().offset2D(-wall_thickness)
inner_solid = inner_wire_wp.extrude(span)

# Cut the inner solid from the main body to create the tube
hollow_body = main_body.cut(inner_solid)

# 4. Create Surface Grooves
# We simulate constant depth grooves by creating a thin skin and intersecting with rings
groove_ref_wire_wp = outer_wire.wires().toPending().offset2D(-groove_depth)
groove_inner_cut = groove_ref_wire_wp.extrude(span)

# 'skin' represents the volume of material on the surface up to groove_depth
skin = main_body.cut(groove_inner_cut)

# Define the regions along the Z-axis where grooves should exist
cutter_mask = cq.Workplane("XY")
cut_locations = [
    margin_end, 
    margin_end + groove_width + groove_gap,
    span - (margin_end + groove_width + groove_gap + groove_width),
    span - (margin_end + groove_width)
]

# Create a union of boxes at the specific Z locations
large_dim = chord * 2.0  # Ensure box covers the whole cross-section
for z in cut_locations:
    # Create a slab at height Z
    slab = cq.Workplane("XY").workplane(offset=z).rect(large_dim, large_dim).extrude(groove_width)
    cutter_mask = cutter_mask.union(slab)

# Intersect the skin with the mask to get ring-shaped cutters that match the airfoil surface
groove_rings = skin.intersect(cutter_mask)

# Cut the grooves from the body
body_with_grooves = hollow_body.cut(groove_rings)

# 5. Internal Spar
# Create a vertical web inside the hollow section for structure
# Positioned roughly at max thickness (approx 30% chord for NACA 00xx)
spar_pos_x = chord * 0.3
spar_thk = wall_thickness

# Create a block representing the spar plane
spar_block = cq.Workplane("XY").workplane(offset=0)\
    .center(spar_pos_x, 0)\
    .rect(spar_thk, chord * 2)\
    .extrude(span)

# Intersect the block with the 'inner_solid' (the void) to perfectly trim the spar to the inner walls
spar_final = spar_block.intersect(inner_solid)

# Union the spar with the main shell
result = body_with_grooves.union(spar_final)

# Export or Render
# show_object(result) # Uncomment if running in CQ-Editor