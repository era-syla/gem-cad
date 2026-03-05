import cadquery as cq

length = 100
width = 50
thickness = 2

r = width/2
offset = length/2 - r

circle1 = cq.Workplane("XY").center(-offset, 0).circle(r).extrude(thickness)
circle2 = cq.Workplane("XY").center(offset, 0).circle(r).extrude(thickness)
rectangle = cq.Workplane("XY").rect(length - width, width).extrude(thickness)

result = circle1.union(circle2).union(rectangle)