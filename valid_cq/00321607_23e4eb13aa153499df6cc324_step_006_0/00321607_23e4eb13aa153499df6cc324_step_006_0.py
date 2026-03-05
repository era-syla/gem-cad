import cadquery as cq

# Model parameters
length = 100.0        # Total length of the part
height = 40.0         # Full height of the part
thickness = 8.0       # Width/Depth of the part
taper_length = 25.0   # Length of the tapered section from the left
tip_height = 25.0     # Height at the very tip (left end)

# Create the profile on the XZ plane (Front view) and extrude along Y
# The shape is a polygon representing the side profile:
# 1. Start at bottom-left (0,0)
# 2. Line to bottom-right (length, 0)
# 3. Line to top-right (length, height)
# 4. Line to start of taper on top edge (taper_length, height)
# 5. Line down to the tip height at x=0 (0, tip_height)
# 6. Close back to (0,0)
result = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(length, 0)
    .lineTo(length, height)
    .lineTo(taper_length, height)
    .lineTo(0, tip_height)
    .close()
    .extrude(thickness)
)