import cadquery as cq

# Define parametric dimensions
length = 100.0        # Length of the tube
outer_diameter = 20.0 # External diameter
inner_diameter = 8.0  # Internal diameter of the through-hole

# Create the cylindrical tube
# We draw two concentric circles on the XY plane and extrude them.
# CadQuery automatically subtracts the inner circle from the outer one during extrusion.
result = (
    cq.Workplane("XY")
    .circle(outer_diameter / 2.0)
    .circle(inner_diameter / 2.0)
    .extrude(length)
)