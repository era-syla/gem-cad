import cadquery as cq

# --- Parameters ---
# Overall dimensions
length = 150.0  # Total length of the plate
width = 40.0    # Total width of the plate
thickness_thick = 10.0 # Thickness at the back (thickest part)
thickness_thin = 0.5   # Thickness at the sharp edge (blade tip)
bevel_width = 15.0     # Width of the beveled section (cutting edge part)

# Hole Configuration
# There are two large counterbored holes and two smaller holes.
# Assuming symmetry.

large_hole_diam = 12.0
large_hole_cbore_diam = 18.0
large_hole_cbore_depth = 5.0
large_hole_spacing = 60.0  # Distance between large holes

small_hole_diam = 4.0
small_hole_spacing = 100.0 # Distance between small holes (outboard of large ones)

# Vertical position of holes (centered on the flat part of the width)
# We need to calculate how much flat area exists before the bevel starts.
flat_width = width - bevel_width
hole_y_pos = flat_width / 2.0  # Centered on the non-beveled section

# --- Modeling ---

# 1. Create the base profile (Cross-section)
# We will draw the side profile (trapezoidal/wedge shape) and extrude it.
# The profile is on the Y-Z plane, extruded along X.

# Points for the cross section:
# (0,0) -> (width, 0) -> (width, thickness_thick) -> (bevel_start, thickness_thick) -> (0, thickness_thin) -> close
# Note: The image shows the bevel on the 'front' edge. Let's orient it so width is along Y.

# Adjusting coordinate system for easier hole placement later:
# Let's extrude along X (Length).
# Profile on YZ plane.
# Y=0 is the sharp edge tip.
# Y=width is the back face.

pts = [
    (0, 0),                       # Bottom-left (sharp edge bottom)
    (width, 0),                   # Bottom-right
    (width, thickness_thick),     # Top-right
    (bevel_width, thickness_thick), # Top bevel start point
    (0, thickness_thin)           # Top-left (sharp edge top)
]

# Create the base extrusion centered on X
base = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(length)
)

# Rotate to align with the typical "top down" view (Length along X, Width along Y)
# Currently: Length is X extrusion. Width is Y profile. Thickness is Z profile.
# The extrusion went from Z=0 to Z=Length (default normal extrusion).
# Let's center it.
base = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(length/2.0, both=True) # Extrude symmetrically
)

# 2. Add Holes
# We need to identify the top flat face to drill into.
# The top face is parallel to the XY plane, located at Z = thickness_thick.
# However, the profile was drawn on YZ. So Y is width, Z is thickness.
# We want to drill along the Z axis (negative direction).

# Hole Locations (X, Y) relative to center.
# Y center of the holes is roughly the center of the flat section.
# The flat section starts at Y = bevel_width and ends at Y = width.
hole_y_center = bevel_width + (width - bevel_width) / 2.0

# Correcting coordinate system mental model based on the YZ sketch:
# X axis is Length. Y axis is Width. Z axis is Thickness.
# The holes go through the face at Z = thickness_thick.

# Large Counterbored Holes
base = (
    base.faces(">Z[1]") # Select the highest Z face (the flat top, excluding the angled bevel face)
    .workplane()
    .pushPoints([
        (-large_hole_spacing/2.0, hole_y_center),
        (large_hole_spacing/2.0, hole_y_center)
    ])
    .cboreHole(large_hole_diam, large_hole_cbore_diam, large_hole_cbore_depth)
)

# Small Holes
base = (
    base.faces(">Z[1]") # Reselect the top flat face
    .workplane()
    .pushPoints([
        (-small_hole_spacing/2.0, hole_y_center),
        (small_hole_spacing/2.0, hole_y_center)
    ])
    .hole(small_hole_diam)
)

# Orient for better view (Optional, matches image orientation roughly)
# The image shows the blade edge on the left/bottom.
# Our model has blade edge at Y=0.
result = base.rotate((0,0,0), (0,0,1), 180) # Just to align visually if needed, but geometry is solid.