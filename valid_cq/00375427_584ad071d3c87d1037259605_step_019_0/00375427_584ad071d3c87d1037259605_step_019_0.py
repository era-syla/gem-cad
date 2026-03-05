import cadquery as cq

# Parametric dimensions based on visual estimation of the aspect ratio
# The object is a long, thin cylindrical rod.
rod_length = 200.0
rod_diameter = 4.0

# Create the rod geometry
# We define a workplane, draw the cross-section (circle), and extrude it.
result = (
    cq.Workplane("XY")
    .circle(rod_diameter / 2.0)
    .extrude(rod_length)
)