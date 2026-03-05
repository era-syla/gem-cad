import cadquery as cq
import math

# --- Parameters ---
height = 100.0        # Total height of the tube
radius = 40.0         # Outer radius of the tube
thickness = 2.0       # Wall thickness of the tube
cut_width = 5.0       # Width of the helical slot
pitch = 100.0         # Pitch of the helix (height for one full revolution)
revolutions = 0.5     # Number of revolutions for the cut

# --- Geometry Construction ---

# 1. Create the base tube
# We start with a solid cylinder and hollow it out.
tube = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(height)
    .faces(">Z")
    .hole(2 * (radius - thickness)) # hole takes diameter
)

# 2. Create the helix cutter
# CadQuery doesn't have a direct "helical cut" primitive for subtraction easily 
# accessible in this specific way without sweeping.
# We will create a helix path and sweep a rectangle along it to create a tool 
# for boolean subtraction.

# Calculate the height of the helix based on pitch and revolutions
helix_height = pitch * revolutions

# Create the helical path
helix_path = cq.Workplane("XY").parametricCurve(
    lambda t: (
        (radius + 5) * math.cos(t * revolutions * 2 * math.pi), # X, slightly larger radius for clean cut
        (radius + 5) * math.sin(t * revolutions * 2 * math.pi), # Y
        t * helix_height + (height/2 - helix_height/2)          # Z, centered vertically
    )
)

# Define the profile to sweep (the cross-section of the cut)
# It needs to be large enough to cut through the wall thickness
# We orient the profile plane perpendicular to the start of the helix
profile_plane = cq.Workplane("XZ", origin=(radius + 5, 0, (height/2 - helix_height/2)))
profile = (
    profile_plane
    .rect(20, cut_width) # Width (cutting depth), Height (slot width)
)

# Sweep the profile along the path to create the cutting solid
cutter = profile.sweep(helix_path, isFrenet=True)

# 3. Perform the Cut
# Subtract the helical solid from the tube
result = tube.cut(cutter)

# Export or visualization helper (not required by prompt but good practice)
# cq.exporters.export(result, "spiral_cut_tube.step")