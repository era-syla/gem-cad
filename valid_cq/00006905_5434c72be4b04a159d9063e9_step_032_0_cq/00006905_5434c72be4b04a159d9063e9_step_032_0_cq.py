import cadquery as cq

# Parametric dimensions
height = 100.0       # Total length of the profile
base_width = 10.0    # Width of the back plate (the "top" of the T)
base_thickness = 2.0 # Thickness of the back plate
leg_length = 8.0     # Length of the protruding legs
leg_thickness = 2.0  # Thickness of each leg
slot_width = 2.0     # Width of the gap between legs

# Calculations for positioning
# The cross-section looks roughly like this:
# 
#  +------------------+  <- base_width
#  +------------------+
#      |  |    |  |
#      |  |    |  |
#      |  |    |  |
#      +--+    +--+
# 
# Let's sketch this on the XY plane and extrude in Z.

# Create the sketch points
# Centering the base on the Y-axis for symmetry
half_base = base_width / 2.0
half_slot = slot_width / 2.0

# Define the profile sketch
# We can draw the entire contour as a single polyline
pts = [
    (-half_base, 0),                        # Bottom-left of base
    (half_base, 0),                         # Bottom-right of base
    (half_base, base_thickness),            # Top-right of base corner
    (half_slot + leg_thickness, base_thickness), # Start of right leg outer
    (half_slot + leg_thickness, base_thickness + leg_length), # End of right leg
    (half_slot, base_thickness + leg_length),    # Inside of right leg tip
    (half_slot, base_thickness),            # Inside of right leg base
    (-half_slot, base_thickness),           # Inside of left leg base
    (-half_slot, base_thickness + leg_length),   # Inside of left leg tip
    (-(half_slot + leg_thickness), base_thickness + leg_length), # End of left leg
    (-(half_slot + leg_thickness), base_thickness), # Start of left leg outer
    (-half_base, base_thickness),           # Top-left of base corner
    (-half_base, 0)                         # Close the loop
]

# Create the solid geometry
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(height)
)