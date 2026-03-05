import cadquery as cq

# Define polygon with nSides and diameter
polygon_shape = cq.Workplane("XY").polygon(nSides=3, diameter=10)

# Extrude the polygon to create a 3D prism
result = polygon_shape.extrude(100)