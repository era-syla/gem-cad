import cadquery as cq

# Parametric dimensions
base_diameter = 20.0
base_height = 8.0
groove_diameter = 18.0  # Slightly smaller than base diameter
groove_width = 2.0
groove_height_from_bottom = 3.0
shaft_diameter = 6.0
shaft_length = 30.0

# Create the base cylinder
base = cq.Workplane("XY").circle(base_diameter / 2).extrude(base_height)

# Create the groove in the base
# We select the outer face, create a workplane, and cut a rectangular profile revolve
# Alternatively, simpler method: Cut a cylinder out of the middle section
groove = (
    cq.Workplane("XY")
    .workplane(offset=groove_height_from_bottom)
    .circle(base_diameter / 2 + 1) # Make sure it cuts all the way from outside
    .circle(groove_diameter / 2)   # Inner bound of the cut
    .extrude(groove_width)
)

# Apply the cut to the base
base_with_groove = base.cut(groove)

# Create the shaft on top of the base
shaft = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .circle(shaft_diameter / 2)
    .extrude(shaft_length)
)

# Combine the parts
result = base_with_groove.union(shaft)