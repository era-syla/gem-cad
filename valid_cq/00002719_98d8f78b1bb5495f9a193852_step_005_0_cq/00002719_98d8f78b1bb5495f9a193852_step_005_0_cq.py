import cadquery as cq

# Parametric dimensions
height = 100.0   # Total height of the channel
width = 60.0     # Total width of the channel
depth = 40.0     # External depth of the channel (flange length)
thickness = 10.0 # Wall thickness

# Create the U-channel profile
# Strategy: Create a solid box and cut out the center to form the 'U' shape.
# Alternatively, draw the profile and extrude. Let's use the profile drawing method
# as it's cleaner for this specific shape.

result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    # Draw the outer 'U' shape
    .lineTo(width, 0)
    .lineTo(width, depth)
    .lineTo(width - thickness, depth)
    .lineTo(width - thickness, thickness)
    .lineTo(thickness, thickness)
    .lineTo(thickness, depth)
    .lineTo(0, depth)
    .close()
    # Extrude vertically
    .extrude(height)
)