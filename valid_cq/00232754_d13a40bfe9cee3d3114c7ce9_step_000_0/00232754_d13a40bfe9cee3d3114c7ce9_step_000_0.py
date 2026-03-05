import cadquery as cq

# Dimensions
length = 60.0           # Total length of the part
diameter = 20.0         # Diameter of the cylinder
radius = diameter / 2.0

head_length = 35.0      # Length of the machined section
groove_radius = 4.0     # Radius of the axial channel
notch_width = 5.0       # Width of the rectangular transverse cut
notch_offset = 2.0      # Distance from the shoulder to the notch

# 1. Base Geometry: Create the main cylinder
# Aligned along the X-axis
result = cq.Workplane("YZ").circle(radius).extrude(length)

# 2. Create the Flat Cut (Half-Cylinder Section)
# We remove the top half (Z > 0) of the cylinder for the length of the head.
# Using a box subtraction.
# Position X: Centered on the head section (head_length/2)
# Position Z: Base at 0, extruding upwards to clear the top.
flat_cutter = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .moveTo(head_length / 2.0, 0)
    .box(head_length, diameter * 2.0, radius, centered=(True, True, False))
)
result = result.cut(flat_cutter)

# 3. Create the Axial Groove
# A semi-circular channel running along the X-axis on the flat face.
# Created by subtracting a cylinder centered at the origin.
groove_cutter = (
    cq.Workplane("YZ")
    .circle(groove_radius)
    .extrude(head_length)
)
result = result.cut(groove_cutter)

# 4. Create the Transverse Notch
# A rectangular cutout on the side of the groove, near the shoulder.
# Position X: Near the end of the head section.
notch_center_x = head_length - notch_offset - (notch_width / 2.0)

# We define a cutting volume for the notch.
# It sits on the XY plane (Z=0) and cuts downwards to the depth of the groove.
# We position it to cut through one side wall (e.g., +Y side).
notch_cutter = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .moveTo(notch_center_x, radius) # Center Y offset to ensure it cuts the wall
    .rect(notch_width, radius * 2.0) # Large rectangle to clear the side
    .extrude(-groove_radius) # Cut down to groove bottom
)
result = result.cut(notch_cutter)