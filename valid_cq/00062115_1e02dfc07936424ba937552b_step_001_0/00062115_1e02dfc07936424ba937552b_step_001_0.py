import cadquery as cq
import math
import numpy as np

# --- Parameters ---
# Main Dimensions
width = 180.0          # Center-to-center distance
cyl_height = 60.0      # Height of the mounting cylinders
cyl_od = 36.0          # Outer diameter of cylinders
cyl_id = 26.0          # Inner diameter (hollow)
beam_thickness = 18.0  # Thickness of the bridge beam (Y-axis depth)
beam_height = 22.0     # Vertical thickness of the bridge profile
arch_rise = 35.0       # Height of the arch center relative to ends
flat_span = 50.0       # Width of the flat top section
fillet_radius = 20.0   # Radius of the bends in the bridge
hole_diameter = 12.0   # Diameter of lightening holes

# Clamp Details
slit_width = 2.0
boss_width = 18.0
boss_depth = 10.0
boss_height = 44.0
bolt_dia = 6.0
cbore_dia = 10.0
bolt_spacing = 26.0

# --- Geometry Construction ---

# 1. Create the Connecting Bridge
# We draw the profile on the XZ plane and extrude symmetrically in Y.
# Calculate key points for the trapezoidal profile
half_w = width / 2.0
x_knee = flat_span / 2.0
y_base = cyl_height * 0.60  # Connection height on cylinder
y_peak = y_base + arch_rise

# Define the outer path of the bridge
def bridge_profile():
    pts = [
        (-half_w, y_base),                  # Bottom Left
        (-x_knee, y_peak),                  # Bottom Knee Left
        (x_knee, y_peak),                   # Bottom Knee Right
        (half_w, y_base),                   # Bottom Right
        (half_w, y_base + beam_height),     # Top Right
        (x_knee, y_peak + beam_height),     # Top Knee Right
        (-x_knee, y_peak + beam_height),    # Top Knee Left
        (-half_w, y_base + beam_height),    # Top Left
    ]
    return cq.Workplane("XZ").polyline(pts).close()

bridge = (
    bridge_profile()
    .extrude(beam_thickness / 2.0, both=True)
)

# Apply fillets to the bridge bends
# Selecting edges parallel to Y axis that are within the span
bridge = (
    bridge.edges("|Y")
    .filter(lambda e: abs(e.Center().x) < half_w - 5)
    .fillet(fillet_radius)
)

# 2. Create End Cylinders
cylinders = (
    cq.Workplane("XY")
    .pushPoints([(-half_w, 0), (half_w, 0)])
    .circle(cyl_od / 2.0)
    .extrude(cyl_height)
)

# 3. Create Clamp Bosses (Lugs)
# These are blocks on the front of the cylinders for the bolts
boss_offset_y = -cyl_od / 2.0 - boss_depth / 2.0 + 1.0 # Slight overlap
bosses = (
    cq.Workplane("XY")
    .pushPoints([(-half_w, boss_offset_y), (half_w, boss_offset_y)])
    .box(boss_width, boss_depth, boss_height)
    .translate((0, 0, cyl_height / 2.0)) # Move Z center to mid-height
)

# 4. Union Main Bodies
result = bridge.union(cylinders).union(bosses)

# 5. Hollow out Cylinders (Main Bore)
result = (
    result.faces("<Z").workplane()
    .pushPoints([(-half_w, 0), (half_w, 0)])
    .circle(cyl_id / 2.0)
    .cutBlind(cyl_height)
)

# 6. Cut Clamp Slits
# Vertical slit cutting through the boss and cylinder wall at the front
result = result.cut(
    cq.Workplane("XY")
    .pushPoints([(-half_w, -cyl_od/2), (half_w, -cyl_od/2)])
    .box(slit_width, cyl_od, cyl_height + 10.0) # Box centered on point
)

# 7. Bolt Holes and Counterbores
# Bolts run X-axis through the bosses
bolt_z_pts = [cyl_height/2 - bolt_spacing/2, cyl_height/2 + bolt_spacing/2]
bolt_y = boss_offset_y

for z in bolt_z_pts:
    # Points for left and right cylinder bolts
    pts = [(-half_w, bolt_y, z), (half_w, bolt_y, z)]
    
    for p in pts:
        # Through hole
        result = result.cut(
            cq.Workplane("YZ").center(p[1], p[2])
            .workplane(offset=p[0] - boss_width)
            .circle(bolt_dia/2)
            .extrude(boss_width * 2.5)
        )
        
        # Counterbore (on the outer faces)
        # Determine offset direction based on cylinder side (Left or Right)
        is_left_cyl = p[0] < 0
        cb_offset = p[0] - boss_width/2.0 if is_left_cyl else p[0] + boss_width/2.0
        extrude_dir = 1 if is_left_cyl else -1
        
        result = result.cut(
            cq.Workplane("YZ").center(p[1], p[2])
            .workplane(offset=cb_offset)
            .circle(cbore_dia/2)
            .extrude(boss_width/2.0 * extrude_dir) # Cut halfway into boss
        )

# 8. Lightening Holes in Bridge Legs
# Calculate positions along the angled legs
# Start and End points of the straight section of the leg (approx)
leg_start = np.array([-half_w + cyl_od/2 + 8.0, y_base + beam_height/2.0])
leg_end = np.array([-x_knee - fillet_radius/2.0, y_peak + beam_height/2.0])
leg_vec = leg_end - leg_start

hole_locs = []
# Create 3 holes along the vector
for t in [0.2, 0.5, 0.8]:
    pt = leg_start + leg_vec * t
    hole_locs.append((pt[0], pt[1]))    # Left Leg
    hole_locs.append((-pt[0], pt[1]))   # Right Leg (Mirror X)

# Cut holes through the bridge (Y-axis)
# Select the front face of the bridge to start the cut
result = (
    result.faces(">Y").workplane()
    .pushPoints(hole_locs)
    .circle(hole_diameter / 2.0)
    .cutBlind(-beam_thickness * 2.0)
)

# 9. Final Fillet at Cylinder Junction (Optional cosmetic)
# Adding a small fillet where the bridge meets the cylinder for smooth transition
try:
    result = result.edges(cq.selectors.NearestToPointSelector((-half_w + cyl_od/2, y_base + beam_height/2, beam_thickness/2))).fillet(2.0)
    result = result.edges(cq.selectors.NearestToPointSelector((half_w - cyl_od/2, y_base + beam_height/2, beam_thickness/2))).fillet(2.0)
except:
    pass # Skip if selection fails to avoid breakage

# Export or Render
# show_object(result) 