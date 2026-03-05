import cadquery as cq

# --- Parameter Definitions ---
# Overall dimensions
width = 60.0    # Width of the box (x-direction)
depth = 30.0    # Depth of the box (y-direction)
height = 80.0   # Total height including legs (z-direction)

# Leg details
leg_height = 10.0
leg_thickness = 4.0   # Thickness of the legs from the side walls
front_arch_height = 8.0 # Height of the cutout between front legs
side_arch_height = 5.0  # Height of the cutout on the sides

# Top slant details
slant_depth = 15.0  # How far back the slant goes
slant_height = 15.0 # How far down the slant goes

# --- Geometry Construction ---

# 1. Start with the main block
# We align the bottom center to z=0 for easier reference, or center everything.
# Let's align the bottom-left-front corner to (0,0,0) conceptually, but center the XY plane.
base = cq.Workplane("XY").box(width, depth, height, centered=(True, True, False))

# 2. Create the slanted top front
# We need to remove material from the top-front edge.
# We'll sketch on the side (YZ plane) and cut.
# Or simpler: select the top-front edge and chamfer it, but the chamfer might need asymmetric distances.
# A chamfer is easy if slant_depth == slant_height. If not, a cut is better.
# Let's assume a generic cut to be safe with parameters.
slant_cut_sketch = (
    cq.Workplane("YZ")
    .workplane(offset=width/2.0) # Move to the right side face
    .moveTo(depth/2.0, height)   # Top-front corner
    .lineTo(depth/2.0 - slant_depth, height) # Top point of slant
    .lineTo(depth/2.0, height - slant_height) # Front point of slant
    .close()
)
# Cut through all
result = base.cut(slant_cut_sketch.extrude(-width)) # Extrude negative to cut inwards

# 3. Create the legs (remove material from bottom)
# We need to cut out the "arches" between the legs.

# Cutout along the width (Front/Back arch)
# We want to keep legs at the corners.
front_cutout_width = width - (2 * leg_thickness)

result = (
    result.faces("<Z") # Select bottom face
    .workplane()
    .rect(front_cutout_width, depth + 1.0) # Rectangle for the central gap, slightly deeper to ensure clean cut
    .cutBlind(front_arch_height) # Cut up into the body
)

# Cutout along the depth (Side arches) - specifically the notch seen on the side
# The image shows a small notch on the side bottom.
side_cutout_depth = depth - (2 * leg_thickness) # Assuming legs are square-ish in profile or symmetric

# Looking at the image, there is a distinct notch on the side, but it seems to leave the front face flat?
# Actually, looking closely at the bottom-left corner of the image:
# There is a leg. Behind it, there is a cutout.
# Let's assume a standard enclosure "feet" design where the center is hollowed out from both axes.

result = (
    result.faces("<Z")
    .workplane()
    .rect(width + 1.0, side_cutout_depth) # Rectangle crossing the whole width
    .cutBlind(side_arch_height)
)

# 4. Final details from the image
# The image shows a specific notch profile on the side near the front leg.
# It looks like the side cut doesn't go all the way through or has a specific shape.
# Let's refine the side cut. The image shows the side notch is rectangular.
# Let's assume simple rectangular cutouts between legs on all sides for symmetry, 
# or specific side notches as seen.

# Re-evaluating the specific side notch at the bottom left of the image:
# It looks like a small rectangular bite taken out of the side wall bottom edge.
# The previous step .rect(width + 1.0, side_cutout_depth).cutBlind(side_arch_height) does this globally.
# This results in 4 legs at the corners.

result = result

# Optional: Fillets or chamfers?
# The image looks fairly sharp, maybe very small fillets, but standard CAD is sharp unless specified.

# Final Variable
result = result