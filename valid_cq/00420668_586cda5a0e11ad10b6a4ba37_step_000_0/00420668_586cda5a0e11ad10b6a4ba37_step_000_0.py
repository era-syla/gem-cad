import cadquery as cq

# Parametric dimensions based on the visual aspect ratio
length = 14.0       # Horizontal dimension
height = 10.0       # Vertical dimension
thickness = 0.2     # Thickness (thin plate)

# Create a rectangular box geometry standing vertically
# Using the XY workplane and defining dimensions for x, y, and z
# This creates a solid plate aligned primarily with the XZ plane
result = cq.Workplane("XY").box(length, thickness, height)