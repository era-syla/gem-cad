import cadquery as cq

# Define parameters for the ring dimensions
# These values are estimated based on visual proportions
outer_diameter = 50.0  # The total diameter of the ring
inner_diameter = 35.0  # The diameter of the hole
thickness = 15.0       # The width/extrusion depth of the ring

# Create the 3D model
# We start by drawing on the XY plane
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)  # Draw outer circle
    .circle(inner_diameter / 2.0)  # Draw inner circle
    .extrude(thickness)            # Extrude the difference to create the ring
)

# Alternatively, using the tube method which is more direct for this shape:
# result = cq.Workplane("XY").tube(outer_diameter/2.0, inner_diameter/2.0, thickness)