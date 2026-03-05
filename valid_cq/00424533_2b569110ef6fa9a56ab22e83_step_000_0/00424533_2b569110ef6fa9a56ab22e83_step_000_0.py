import cadquery as cq

# Define parametric dimensions for the rectangular plate
length = 100.0  # Dimension along the X axis
width = 60.0    # Dimension along the Y axis
thickness = 5.0 # Dimension along the Z axis

# Create the rectangular plate centered on the XY plane
result = cq.Workplane("XY").box(length, width, thickness)