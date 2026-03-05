import cadquery as cq

# Define parametric dimensions based on the visual proportions
plate_width = 80.0      # Dimension along the X-axis
plate_height = 100.0    # Dimension along the Z-axis (vertical)
plate_thickness = 4.0   # Dimension along the Y-axis

# Create the solid rectangular plate
# We use the box primitive oriented to stand upright (thickness along Y)
result = cq.Workplane("XY").box(plate_width, plate_thickness, plate_height)