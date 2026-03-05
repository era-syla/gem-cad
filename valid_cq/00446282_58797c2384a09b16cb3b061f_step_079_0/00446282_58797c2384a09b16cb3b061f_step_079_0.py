import cadquery as cq

# Parameter definitions
length = 100.0        # Total length of the beam
profile_width = 30.0  # Overall width of the cross section
profile_height = 30.0 # Overall height of the cross section
thickness = 10.0      # Thickness of the cross arms

# Create the geometry by uniting two rectangular prisms (boxes)
# We align the beam length along the Z-axis

# 1. Create the vertical arm of the cross
# Dimensions: width=thickness, height=profile_height, depth=length
vertical_arm = cq.Workplane("XY").box(thickness, profile_height, length)

# 2. Create the horizontal arm of the cross
# Dimensions: width=profile_width, height=thickness, depth=length
horizontal_arm = cq.Workplane("XY").box(profile_width, thickness, length)

# 3. Combine the two shapes into a single solid
result = vertical_arm.union(horizontal_arm)