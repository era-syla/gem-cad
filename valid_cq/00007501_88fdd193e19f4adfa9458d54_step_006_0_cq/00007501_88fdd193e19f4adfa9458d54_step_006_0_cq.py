import cadquery as cq

# Parametric dimensions
rod_length = 100.0  # Length of the rod
rod_diameter = 2.0  # Diameter of the rod

# Create the rod geometry
# We start by drawing a circle on the XY plane and extruding it
result = (
    cq.Workplane("XY")
    .circle(rod_diameter / 2)
    .extrude(rod_length)
)

# Alternatively, using the cylinder primitive for simpler syntax:
# result = cq.Workplane("XY").cylinder(rod_length, rod_diameter / 2)