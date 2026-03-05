import cadquery as cq

# Parametric dimensions based on the visual proportions of the image
length = 100.0    # Total length of the extrusion
width = 40.0      # Total width of the profile
height = 40.0     # Total height of the profile
thickness = 12.0  # Thickness of the walls

# Create the model
# 1. Select the Front plane (XZ plane) to draw the cross-section
# 2. Draw the inverted L-shape profile (Angle profile)
#    Orientation: Top leg is horizontal, Right leg is vertical
# 3. Extrude the profile along the Y-axis
result = (
    cq.Workplane("front")
    .moveTo(0, height)                      # Start at Top-Left corner
    .lineTo(width, height)                  # Top edge to Top-Right
    .lineTo(width, 0)                       # Right edge to Bottom-Right
    .lineTo(width - thickness, 0)           # Bottom edge of the vertical leg
    .lineTo(width - thickness, height - thickness) # Inner vertical edge
    .lineTo(0, height - thickness)          # Inner horizontal edge (underside of top leg)
    .close()                                # Close back to start (Left edge of top leg)
    .extrude(length)                        # Extrude to create the solid
)