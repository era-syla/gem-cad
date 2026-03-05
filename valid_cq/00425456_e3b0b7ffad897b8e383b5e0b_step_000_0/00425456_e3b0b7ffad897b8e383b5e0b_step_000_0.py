import cadquery as cq

# Parametric dimensions
length = 120.0  # Length of the plate
width = 90.0    # Width of the plate
thickness = 3.0 # Thickness of the plate

# Create the rectangular plate geometry
# Start on the XY plane, draw a centered rectangle, and extrude it to create the solid
result = (
    cq.Workplane("XY")
    .rect(length, width)
    .extrude(thickness)
)