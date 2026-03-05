import cadquery as cq

# Parametric dimensions
height = 100.0  # Total height of the vertical leg
width = 50.0    # Total width of the horizontal leg
thickness = 10.0 # Thickness of the material
depth = 40.0    # Depth (extrusion length) of the profile

# Create the L-shape profile and extrude it
# Method: Sketch on the XY plane, draw an L-shape, and extrude in Z.
result = (
    cq.Workplane("XY")
    .moveTo(0, 0)
    .lineTo(0, height)           # Draw up the back
    .lineTo(thickness, height)   # Draw right along top thickness
    .lineTo(thickness, thickness)# Draw down inside vertical leg
    .lineTo(width, thickness)    # Draw right along inside horizontal leg
    .lineTo(width, 0)            # Draw down to bottom
    .close()                     # Close back to (0,0)
    .extrude(depth)
)

# Alternative method using simple boxes if preferred for constructability:
# vertical_leg = cq.Workplane("XY").box(thickness, depth, height, centered=(False, False, False))
# horizontal_leg = cq.Workplane("XY").box(width, depth, thickness, centered=(False, False, False))
# result = vertical_leg.union(horizontal_leg)