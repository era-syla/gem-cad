import cadquery as cq

# Define parametric dimensions based on visual estimation
outer_diameter = 50.0  # Overall diameter of the disc
thickness = 5.0        # Thickness of the disc
hole_diameter = 6.0    # Diameter of the central hole

# Generate the geometry
# 1. Create a workplane
# 2. Draw the outer circle
# 3. Draw the inner circle (which creates a hole when extruded with the outer circle)
# 4. Extrude to the specified thickness
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(hole_diameter / 2.0)
    .extrude(thickness)
)