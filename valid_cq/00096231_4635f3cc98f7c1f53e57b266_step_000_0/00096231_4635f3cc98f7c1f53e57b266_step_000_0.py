import cadquery as cq

# -- Parametric Dimensions --
base_diameter = 8.0       # Diameter of the bottom cylindrical section
base_length = 45.0        # Length of the bottom section
taper_length = 55.0       # Length of the top tapered section
tip_diameter = 3.0        # Diameter at the top before rounding
tip_fillet = 1.0          # Radius of the fillet at the tip
hole_diameter = 0.8       # Diameter of the hole at the tip
hole_depth = 3.0          # Depth of the hole

# -- Geometry Construction --

# 1. Create the base cylinder
result = cq.Workplane("XY").circle(base_diameter / 2.0).extrude(base_length)

# 2. Create the tapered top section using a loft
# We select the top face, define the starting profile, offset to the top, define the ending profile, and loft.
result = (
    result.faces(">Z")
    .workplane()
    .circle(base_diameter / 2.0)
    .workplane(offset=taper_length)
    .circle(tip_diameter / 2.0)
    .loft(combine=True)
)

# 3. Round the tip edge
result = result.edges(">Z").fillet(tip_fillet)

# 4. Create the small hole at the very top
result = result.faces(">Z").workplane().hole(hole_diameter, hole_depth)