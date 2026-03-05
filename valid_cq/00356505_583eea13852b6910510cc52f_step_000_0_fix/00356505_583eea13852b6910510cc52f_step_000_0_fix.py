import cadquery as cq

# Create the base part
base = cq.Workplane("XY").rect(40, 20).extrude(10)

# Create the arc cutout
arc_cutout = cq.Workplane("XY").center(0, 0).threePointArc((10, 10), (0, 20)).lineTo(0, 0).close().extrude(10)

# Subtract the arc cutout from the base
part_with_arc = base.cut(arc_cutout)

# Create the U-shape cut
u_cutout = cq.Workplane("XY").center(0, 10).rect(10, 20).extrude(10)

# Subtract the U-shape cut from the part
part_with_u_cut = part_with_arc.cut(u_cutout)

# Create holes on the flange
holes = part_with_u_cut.faces(">Z").workplane().center(-10, -5).circle(2).extrude(-10)
holes = holes.faces(">Z").workplane().center(20, 0).circle(2).extrude(-10)

# Create the central hole
final_part = holes.faces(">Z").workplane().center(-10, 0).circle(3).extrude(-10)

result = final_part


