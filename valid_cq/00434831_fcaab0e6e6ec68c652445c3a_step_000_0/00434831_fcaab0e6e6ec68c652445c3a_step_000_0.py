import cadquery as cq

# Parameters definition
width = 60.0       # X dimension (Length of the front face)
depth = 25.0       # Y dimension (Width of the side face)
height = 70.0      # Z dimension (Height of the box)
thickness = 2.0    # Material thickness
slot_width = 20.0  # Width of the front cutout
slot_depth = 45.0  # Depth of the front cutout from top
flap_height = 25.0 # Height of the top flaps
flap_angle = 30.0  # Angle of flaps (degrees)

# 1. Base Box Body
# Create the main rectangular prism centered on XY plane, base at Z=0
box = cq.Workplane("XY").box(width, depth, height, centered=(True, True, False))

# Shell the box to create walls with thickness, removing the top face (+Z)
# shell(-thickness) creates walls inward
main_body = box.faces(">Z").shell(-thickness)

# 2. Front Cutout
# Define the cutout shape (U-slot). 
# We position it on the Front face (assumed at Y = -depth/2 based on proportions).
# The cutter is a box that intersects the front wall.
slot_cutter = (cq.Workplane("XY")
               .box(slot_width, thickness * 4, slot_depth, centered=(True, True, True))
               .translate((0, -depth/2, height - slot_depth/2))
              )

# Apply the cut
main_body = main_body.cut(slot_cutter)

# 3. Flaps
# We construct flaps as separate solids and union them to the body.
# Flaps are attached to the top edges of the Left, Right, and Back walls.
# Front wall has the cutout and we omit the flap for visual accuracy with the provided image.

# Left Flap (Attached to face at X = -width/2)
# Dimensions: thickness x depth x flap_height
left_flap = (cq.Workplane("XY")
             .box(thickness, depth, flap_height, centered=(True, True, False))
             # Shift so the outer face is at X=0 (Pivot alignment)
             .translate((thickness/2, 0, 0))
             # Rotate outwards (Z tilts towards -X)
             .rotate((0, 0, 0), (0, 1, 0), -flap_angle)
             # Move to position at the top of the left wall
             .translate((-width/2, 0, height))
            )

# Right Flap (Attached to face at X = width/2)
right_flap = (cq.Workplane("XY")
              .box(thickness, depth, flap_height, centered=(True, True, False))
              # Shift so the outer face is at X=0
              .translate((-thickness/2, 0, 0))
              # Rotate outwards (Z tilts towards +X)
              .rotate((0, 0, 0), (0, 1, 0), flap_angle)
              # Move to position
              .translate((width/2, 0, height))
             )

# Back Flap (Attached to face at Y = depth/2)
# Dimensions: width x thickness x flap_height
back_flap = (cq.Workplane("XY")
             .box(width, thickness, flap_height, centered=(True, True, False))
             # Shift so the outer face is at Y=0
             .translate((0, -thickness/2, 0))
             # Rotate outwards (Z tilts towards +Y)
             # Rotation around X-axis: + is Y->Z. We want Z->Y, so negative angle.
             .rotate((0, 0, 0), (1, 0, 0), -flap_angle)
             # Move to position
             .translate((0, depth/2, height))
            )

# 4. Combine all parts
result = main_body.union(left_flap).union(right_flap).union(back_flap)