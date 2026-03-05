import cadquery as cq

# Geometric parameters
radius = 50.0  # Radius of the disk
thickness = 2.0  # Thickness of the disk

# Create the cylinder/disk
result = (
    cq.Workplane("XY")
    .circle(radius)
    .extrude(thickness)
)