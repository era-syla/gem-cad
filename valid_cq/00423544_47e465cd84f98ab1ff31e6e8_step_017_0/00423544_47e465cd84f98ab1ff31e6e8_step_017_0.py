import cadquery as cq

# Parametric dimensions
width = 100.0         # Total width of the object
height_top = 35.0     # Y-height of the top arc at the center
height_bottom = 12.0  # Y-height of the bottom arc at the center (arch height)
thickness = 5.0       # Extrusion thickness

# Define the key points for the profile
# The shape is symmetric about the Y-axis
left_tip = (-width / 2.0, 0.0)
right_tip = (width / 2.0, 0.0)
top_peak = (0.0, height_top)
bottom_peak = (0.0, height_bottom)

# Create the 3D model
# 1. Start on the XY plane
# 2. Draw the top convex arc from left tip to right tip
# 3. Draw the bottom concave arc from right tip back to left tip
# 4. Extrude to create the solid
result = (
    cq.Workplane("XY")
    .moveTo(*left_tip)
    .threePointArc(top_peak, right_tip)
    .threePointArc(bottom_peak, left_tip)
    .close()
    .extrude(thickness)
)