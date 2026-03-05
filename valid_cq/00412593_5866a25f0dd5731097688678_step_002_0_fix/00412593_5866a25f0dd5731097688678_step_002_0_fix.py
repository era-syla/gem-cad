import cadquery as cq

# Create the main body shape
main_body = cq.Workplane("XY").rect(40, 60).extrude(10).edges("|Z").fillet(5)

# Create a hole in the main body
hole = main_body.faces(">Z").workplane().circle(10).cutThruAll()

# Create the rod shape
rod = cq.Workplane("XY").circle(3).extrude(100)

# Create the end cap shape
end_cap = cq.Workplane("XY").circle(6).extrude(2)

# Position the rod through the main body
assembled_rod = rod.union(end_cap.translate((0, 0, 100))).translate((0, 0, 5))

# Combine everything into a single part
result = hole.union(assembled_rod)

# Mirror the rod to make a similar structure on the other side
result = result.union(assembled_rod.mirror("XZ"))