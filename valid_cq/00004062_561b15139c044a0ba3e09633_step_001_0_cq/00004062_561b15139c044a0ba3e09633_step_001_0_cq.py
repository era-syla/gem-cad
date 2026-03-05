import cadquery as cq

# Parametric dimensions
outer_diameter = 100.0  # Main diameter of the disc
inner_diameter = 70.0   # Diameter of the inner recessed area
thickness = 5.0         # Total thickness of the disc
recess_depth = 0.5      # Depth of the inner circular recess

# Create the base disc
base = cq.Workplane("XY").circle(outer_diameter / 2).extrude(thickness)

# Create the recess
# Select the front face, draw the inner circle, and cut slightly
result = (
    base.faces(">Z")
    .workplane()
    .circle(inner_diameter / 2)
    .cutBlind(-recess_depth)
)