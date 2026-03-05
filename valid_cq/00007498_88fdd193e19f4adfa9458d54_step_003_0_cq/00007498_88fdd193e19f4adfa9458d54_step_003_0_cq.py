import cadquery as cq

# Parametric dimensions
outer_diameter = 20.0
inner_diameter = 12.0
length = 30.0
keyway_width = 3.0  # Width of the keyway slot
keyway_depth = 1.5  # Depth of the keyway from the inner surface

# Create the main cylinder
main_body = cq.Workplane("XY").circle(outer_diameter / 2).extrude(length)

# Create the inner bore
bore = cq.Workplane("XY").circle(inner_diameter / 2).extrude(length)

# Create the keyway profile
# We position a rectangle or circle to cut the keyway.
# Looking at the image, it seems to be a rounded keyway.
# Let's approximate it as a circular cutout offset from the center.
# A common keyway shape is rectangular, but this specific image looks like a simple 
# semi-circular groove or just a standard keyway with fillets. 
# Let's make a standard rectangular keyway with a rounded top which is common for shaft collars,
# or simply a circle if it looks like a pin channel.
# Looking closely at the image, the cutout inside the hole looks semi-circular.
# Let's model it as a circle swept along the length.

keyway_radius = keyway_width / 2
# The center of the keyway cutter needs to be positioned such that it cuts into the inner bore.
# Distance from center = (inner_diameter / 2) + keyway_depth - keyway_radius
keyway_center_offset = (inner_diameter / 2) 

keyway_cutter = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .moveTo(0, keyway_center_offset)
    .circle(keyway_radius)
    .extrude(length)
)

# Combine operations:
# 1. Start with main body
# 2. Cut the center bore
# 3. Cut the keyway
result = main_body.cut(bore).cut(keyway_cutter)

# Alternatively, a more robust way using a single 2D sketch and extruding:
# (This is often cleaner for simple profiles)
final_part = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)  # Outer circle
    .circle(inner_diameter / 2)  # Inner circle to be subtracted (hole)
    .extrude(length)
)

# Now adding the keyway as a separate cut operation to ensure correct geometry
# The keyway in the image looks like a half-circle notch on the inner circumference.
keyway_cut = (
    cq.Workplane("XY")
    .moveTo(0, inner_diameter/2) # Move to the top of the inner hole
    .circle(keyway_width/2)      # Create the profile for the keyway
    .extrude(length)
)

# Final boolean operation
result = final_part.cut(keyway_cut)