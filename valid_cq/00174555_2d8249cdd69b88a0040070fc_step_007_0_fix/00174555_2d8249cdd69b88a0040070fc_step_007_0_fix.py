import cadquery as cq

side = 20
thickness = 2
diameter = side / 0.8660254037844386  # circumscribed circle diameter for equilateral triangle

# create one triangular prism
triangle = cq.Workplane("XY").polygon(3, diameter).extrude(thickness)

# position and orient four copies
p1 = triangle.translate((-15, 10, 0))
p2 = triangle.rotate((0, 0, 0), (0, 0, 1), 90).translate((15, 12, 0))
p3 = triangle.rotate((0, 0, 0), (0, 0, 1), 210).translate((10, -15, 0))
p4 = triangle.rotate((0, 0, 0), (0, 0, 1), 300).translate((-15, -10, 0))

result = p1.union(p2).union(p3).union(p4)