import cadquery as cq

# Main cylinder
cylinder = cq.Workplane("XY").circle(10).extrude(40)

# Shaft
shaft = cq.Workplane("XY").circle(2).extrude(50).translate((0, 0, -5))

# End disk
end_disk = cq.Workplane("XY").circle(5).extrude(3).translate((0, 0, 40))

# Support rod
support_rod = cq.Workplane("XY").circle(1).extrude(60).translate((-30, 0, 15)).rotate((0, 0, 0), (0, 1, 0), 90)

# Plate
plate = cq.Workplane("YZ").rect(60, 40).extrude(1).translate((0, 0, 18))

# Combining all parts
result = cylinder.union(shaft).union(end_disk).union(support_rod).union(plate)