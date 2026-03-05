import cadquery as cq

# Dimensions of the part
length = 60.0       # Total length from base to tip
base_width = 18.0   # Width of the base face
thickness = 12.0    # Extrusion thickness

# Create the part
# The profile is created on the XY plane:
# 1. Starts at the top corner of the base (0, base_width)
# 2. Straight vertical line to origin (0, 0)
# 3. Straight horizontal line to the tip (length, 0)
# 4. A curved arc connecting the tip back to the start point
result = (
    cq.Workplane("XY")
    .moveTo(0, base_width)
    .lineTo(0, 0)
    .lineTo(length, 0)
    .threePointArc((length * 0.35, base_width * 0.85), (0, base_width))
    .close()
    .extrude(thickness)
)