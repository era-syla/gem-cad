import cadquery as cq

# Parametric dimensions
circumscribed_diameter = 20.0  # Controls the overall size of the triangle
thickness = 1.0                # Thickness of the triangular plate

# Create a regular triangular prism (equilateral triangle)
# polygon(nSides=3) creates a triangle inscribed in a circle of the given diameter
result = (
    cq.Workplane("XY")
    .polygon(nSides=3, diameter=circumscribed_diameter)
    .extrude(thickness)
)