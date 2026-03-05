import cadquery as cq

# Parametric dimensions
base_width = 20.0
base_height = 40.0
base_thickness = 15.0

arm_length = 50.0  # From the back of the base to the center of the rounded end
arm_thickness = 10.0
arm_height = 40.0  # Same as base height initially

# Hole dimensions
base_hole_diameter = 5.0
base_hole_spacing = 20.0  # Distance between the two holes on the base
arm_hole_diameter = 6.0

# Create the base block
# We will center the design roughly around the origin for easier manipulation
base = cq.Workplane("XY").box(base_width, base_height, base_thickness)

# Create the arm
# The arm extends from the side of the base.
# It has a rounded end.
arm_center_dist = arm_length  # Distance to center of the arc
total_arm_len = arm_length + (arm_height / 2.0)

# We create the arm profile on the side of the base and extrude it
# The arm seems to be flush with one side of the base (the "back") but thinner
arm = (
    cq.Workplane("XY")
    .workplane(offset=-base_thickness / 2.0)  # Start from the bottom face (relative to original box)
    .center(base_width / 2.0, 0) # Move to the right edge of the base
    .transformed(rotate=(0, 90, 0)) # Rotate to draw on the YZ plane effectively
    .workplane(offset=0) # Reset workplane orientation after transform
    # The arm is thinner, let's assume it's flush with the "back" face (top in XY view usually, or aligned)
    # Looking at the image, the arm is flush with the top face and bottom face of the base in terms of height?
    # No, looking closely, the arm is the full height of the base.
    # The thickness is the difference. The base is thicker.
    # Let's re-orient. Let's build it flat on XY.
)

# Alternative approach: Build the 2D profile and extrude
# 1. Base Rectangle
# 2. Arm extending from it with rounded cap
# 3. Extrude everything to arm_thickness
# 4. Add the extra thickness to the base part

# Let's go with the additive approach
# 1. Create the main L-shape body with the thickness of the arm
# The full height is base_height. The length is base_width + arm_length.
# The end is rounded.

# Create the main flat shape (the arm and part of the base)
# Orientation: Length along X, Height along Y, Thickness along Z
main_body = (
    cq.Workplane("XY")
    .moveTo(-base_width, -base_height/2)
    .lineTo(arm_length, -base_height/2)
    .threePointArc((arm_length + base_height/2, 0), (arm_length, base_height/2)) # Rounded end
    .lineTo(-base_width, base_height/2)
    .close()
    .extrude(arm_thickness)
)

# Add the thicker block for the base
# The base is thicker than the arm. The image shows a step.
# Let's assume the extra thickness is added on one side (the "front" in the image).
extra_base_thickness = base_thickness - arm_thickness

base_block = (
    cq.Workplane("XY")
    .workplane(offset=arm_thickness) # Start on top of the existing shape
    .moveTo(-base_width, -base_height/2)
    .rect(base_width, base_height, centered=False) # Rectangle for the base part
    .extrude(extra_base_thickness)
)

# Combine the shapes
result = main_body.union(base_block)

# Add holes
# 1. Hole in the rounded arm
result = (
    result.faces(">Z") # Select the top face (could be the arm or the base, need to be careful)
    .workplane()
    .moveTo(arm_length, 0) # Center of the arc
    .hole(arm_hole_diameter)
)

# 2. Holes in the base
# These are on the side face (the thick face at the end)
# Based on the image, looking at the block from the left (-X direction)
result = (
    result.faces("<X") # Select the face at -X
    .workplane()
    .moveTo(0, base_hole_spacing/2)
    .hole(base_hole_diameter)
    .moveTo(0, -base_hole_spacing) # Move relative to previous hole or absolute? moveTo is absolute on the plane
    .moveTo(0, -base_hole_spacing/2) # Absolute position
    .hole(base_hole_diameter)
)

# Refinement: In the image, the step between arm and base is sharp.
# The holes on the base seem to be centered on the thickness of the base.
# Our construction ensures the base block is added on top, so the base is thicker.
# The holes are on the "end" face of the base.

# Verify coordinates for holes on the base face
# The face is Y-Z plane essentially.
# Z goes from 0 to base_thickness. Y goes from -20 to 20.
# Center of the face is roughly Z=base_thickness/2, Y=0.
# The default workplane on <X centers the origin on the face center.
# So (0, base_hole_spacing/2) refers to (Y, Z) or (Z, Y)?
# Standard CadQuery face workplane orientation: X is local horizontal, Y is local vertical.
# On <X face:
# Normal is -X.
# Local X is likely +Y? or -Y?
# Local Y is likely +Z.
# Let's adjust hole positions relative to the face center.

result = (
    result.faces("<X")
    .workplane()
    # Create two holes
    .pushPoints([(0, base_hole_spacing/2), (0, -base_hole_spacing/2)])
    .hole(base_hole_diameter)
)

# Final check of the geometry
# The arm connects to the side of the base.
# The image shows the arm surface is flush with the "back" of the base.
# In my code:
# main_body starts at Z=0, goes to Z=arm_thickness.
# base_block starts at Z=arm_thickness, goes to Z=base_thickness.
# This creates a step on the +Z side.
# The -Z side is flush (Z=0).
# This matches the "flush back" appearance if we consider -Z the back.
# The holes on the base are centered on the base face.

# Re-orient for better viewing if exported (optional, but good practice)
# No specific orientation requested, leaving as is.