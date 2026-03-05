import cadquery as cq

# Parametric dimensions
outer_diameter = 100.0  # Overall diameter of the ring
height = 10.0           # Height of the band
thickness = 2.0         # Wall thickness of the ring

# Calculate inner diameter based on wall thickness
inner_diameter = outer_diameter - (2 * thickness)

# Create the ring geometry
# We can create a ring by sketching two concentric circles and extruding them
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2)  # Outer boundary
    .circle(inner_diameter / 2)  # Inner boundary (hole)
    .extrude(height)
)

# Alternatively, using the tube method directly from primitives:
# result = cq.Workplane("XY").tube(outerRadius=outer_diameter/2, innerRadius=inner_diameter/2, length=height)