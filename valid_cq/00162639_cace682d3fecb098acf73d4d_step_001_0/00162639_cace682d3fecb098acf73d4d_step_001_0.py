import cadquery as cq

# Parametric dimensions based on visual estimation of the rectangular bar
length = 100.0  # Long dimension
height = 10.0   # Vertical dimension
thickness = 2.0 # Thin dimension

# Create the rectangular prism (box)
# centered=True is the default for box(), centering the geometry at the origin
result = cq.Workplane("XY").box(length, thickness, height)