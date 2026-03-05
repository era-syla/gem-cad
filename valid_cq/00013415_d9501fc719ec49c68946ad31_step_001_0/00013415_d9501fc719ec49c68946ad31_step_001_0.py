import cadquery as cq

# Parameters for the model
width = 10.0
depth = 10.0
height = 40.0
notch_width = 3.0  # Along Y axis
notch_depth = 2.0  # Into the X face
notch_height = 8.0 # Height of the notch feature
bottom_angle_rise = 3.0 # How much the bottom rises from the corner

# 1. Create the main rectangular prism
# Centered on XY, extending from Z = -20 to Z = 20
result = cq.Workplane("XY").box(width, depth, height)

# 2. Define geometry for the bottom angled cut
# The lowest point is assumed to be the Front-Right corner (in standard view context),
# which we map to (width/2, -depth/2).
# The plane rises towards the back and left.
# Points defining the plane (relative to the bottom face at Z = -height/2):
p1 = (width/2, -depth/2, -height/2)                 # Lowest point (Corner)
p2 = (-width/2, -depth/2, -height/2 + bottom_angle_rise) # Back along X
p3 = (width/2, depth/2, -height/2 + bottom_angle_rise)   # Back along Y

# Create a cutting tool for the bottom
# We calculate the normal of the plane defined by p1, p2, p3 to orient a cutter
# Vector 1: p2 - p1 = (-10, 0, 3)
# Vector 2: p3 - p1 = (0, 10, 3)
# Normal = V1 x V2 = (-30, 30, -100) -> (-0.3, 0.3, -1)
# Use a large box oriented to this plane to cut everything below it
bottom_cutter_plane = cq.Plane(origin=p1, normal=(-0.3, 0.3, -1))
bottom_cutter = (
    cq.Workplane(bottom_cutter_plane)
    .rect(50, 50) # Large rectangle
    .extrude(20)  # Extrude 'up' (relative to normal, so away from part) or 'down'?
                  # Normal points down, so extrude + direction goes down.
                  # We want to remove the material *below* the plane.
                  # Since the normal is pointing roughly down (-Z), extruding +20 removes the bottom.
)

# 3. Define the side notch (relief cut)
# Located at the same corner (width/2, -depth/2) on the X face.
# It should have vertical walls but a top "roof" parallel to the bottom cut.

# First, create a vertical block representing the notch footprint
# Center of the notch block:
# X: From width/2 inwards by notch_depth. Center = width/2 - notch_depth/2
# Y: From -depth/2 inwards by notch_width. Center = -depth/2 + notch_width/2
notch_center_x = width/2 - notch_depth/2
notch_center_y = -depth/2 + notch_width/2
notch_tool = (
    cq.Workplane("XY")
    .workplane(offset=-height/2) # Start at bottom
    .center(notch_center_x, notch_center_y)
    .box(notch_depth, notch_width, height) # Infinite height for now
)

# Create a cutter for the "roof" of the notch
# It is the same as the bottom cutter, but shifted up by notch_height
notch_roof_plane = cq.Plane(
    origin=(p1[0], p1[1], p1[2] + notch_height), 
    normal=(-0.3, 0.3, -1)
)
notch_roof_cutter = (
    cq.Workplane(notch_roof_plane)
    .rect(50, 50)
    .extrude(-50) # Extrude upwards (opposite to normal) to remove the top part of the notch tool
)

# Trim the notch tool so it has a slanted roof
# We cut the 'notch_tool' with the 'notch_roof_cutter'
# Since notch_roof_cutter is the volume *above* the roof plane, intersecting or cutting?
# We want to keep the bottom part of the notch tool.
# notch_roof_cutter defined above extrudes "Up" (-normal).
# So cutting notch_tool with it removes the top.
notch_tool = notch_tool.cut(notch_roof_cutter)

# 4. Apply cuts to the main result
# First, cut the notch from the body
result = result.cut(notch_tool)

# Then, cut the bottom of the entire body
result = result.cut(bottom_cutter)