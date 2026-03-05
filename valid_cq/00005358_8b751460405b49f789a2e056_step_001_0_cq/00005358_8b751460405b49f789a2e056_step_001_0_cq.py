import cadquery as cq

# Parametric dimensions
outer_diameter = 100.0  # Outer diameter of the ring
inner_diameter = 95.0   # Inner diameter of the ring (defines the thickness of the band)
thickness = 2.0         # Thickness (height) of the ring

# Create the ring
# We create a workplane, draw two circles, and extrude the difference
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)
    .circle(inner_diameter / 2)
    .extrude(thickness)
)