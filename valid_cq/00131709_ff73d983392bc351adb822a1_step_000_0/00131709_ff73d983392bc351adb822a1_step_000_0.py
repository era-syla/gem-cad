import cadquery as cq

# Parametric dimensions
base_diameter = 20.0
base_length = 15.0
shaft_diameter = 10.0
shaft_height = 60.0

# Create the horizontal base cylinder
# Aligned along the Y-axis (Drawing on XZ plane and extruding symmetrically)
base = cq.Workplane("XZ").circle(base_diameter / 2.0).extrude(base_length / 2.0, both=True)

# Create the vertical shaft cylinder
# Aligned along the Z-axis, starting from the origin to intersect the base
shaft = cq.Workplane("XY").circle(shaft_diameter / 2.0).extrude(shaft_height)

# Combine the parts into a single solid
result = base.union(shaft)