import cadquery as cq

# Main cylinder
main = cq.Workplane("XY").circle(10).extrude(100)

# Side holes
hole1 = cq.Workplane("YZ", origin=(0, 0, 30)).circle(2.5).extrude(30)
hole2 = cq.Workplane("YZ", origin=(0, 0, 60)).circle(2.5).extrude(30)

# Subtract holes from main cylinder
result = main.cut(hole1).cut(hole2)