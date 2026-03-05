import cadquery as cq

# --- Parameter Definitions ---
# Main body dimensions
outer_diameter = 100.0
total_thickness = 15.0
wall_thickness = 3.0  # Approximate wall thickness for the rim

# Top rim details
rim_height = 2.0
rim_width = 4.0
fillet_radius = 1.5

# Cutout details (the notch at the top)
cutout_width = 25.0
cutout_depth = 8.0  # Depth into the circle from the edge
cutout_height = 8.0 # How far down from the top face

# Screw hole details
hole_pitch_diameter = 60.0  # Distance between centers seems roughly 60% of OD
hole_diameter = 4.5
cbore_diameter = 8.5
cbore_depth = 3.0
hole_angle = 45.0 # Angle of hole placement relative to vertical axis

# --- Modeling Process ---

# 1. Base Disk
# Create the main cylinder
base = cq.Workplane("XY").circle(outer_diameter / 2.0).extrude(total_thickness)

# 2. Create the Rim / Recess
# We'll cut a recess into the top face to leave a rim
# The recess depth is rim_height, diameter is OD - 2*rim_width
recess_diameter = outer_diameter - (2 * rim_width)
base = base.faces(">Z").workplane().circle(recess_diameter / 2.0).cutBlind(-rim_height)

# 3. Add Fillet to the Rim
# Select the top outer edge and fillet it
base = base.edges(">Z and %Circle").fillet(fillet_radius)

# 4. Create the Notch/Cutout
# Create a shape to subtract from the top edge
# We position a rectangle at the top edge (12 o'clock position)
cutout_shape = (
    cq.Workplane("XY")
    .workplane(offset=total_thickness) # Start at top face
    .moveTo(0, outer_diameter/2.0)     # Move to outer edge
    .rect(cutout_width, cutout_depth * 2) # Rectangle centered on the edge
    .extrude(-cutout_height)           # Cut downwards
)
result = base.cut(cutout_shape)

# 5. Create Countersunk Holes
# We need two holes on a pitch circle diameter.
# Based on the image, they are roughly at 45 and 225 degrees, or -45 and 135.
# Looking at the image, if the notch is at 12 o'clock (90 deg), the holes are roughly at 8 o'clock and 4 o'clock? 
# No, let's look closer. The notch is at the top. The holes are aligned horizontally-ish but tilted.
# Actually, looking at the perspective, the notch is top-left. Let's assume standard alignment:
# Notch at 12 o'clock (Y+). Holes appear symmetric. Let's place them at -45 and -135 relative to X axis?
# Or simply +/- X distance. They look symmetric across the vertical axis defined by the notch.
# Let's assume they are on the X axis or slightly rotated. In the image, the notch is up. The holes are left and right.
# Let's place them at +/- X offsets.

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints([(hole_pitch_diameter/2.0, 0), (-hole_pitch_diameter/2.0, 0)]) # Place on X axis centered
    .cboreHole(hole_diameter, cbore_diameter, cbore_depth)
)

# 6. Apply fillet to bottom edge (optional but looks good/realistic)
result = result.edges("<Z").fillet(1.0)

# Export or visualize
if 'show_object' in globals():
    show_object(result)