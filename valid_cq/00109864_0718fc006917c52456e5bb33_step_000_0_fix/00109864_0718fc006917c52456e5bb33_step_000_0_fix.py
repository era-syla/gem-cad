import cadquery as cq

# Main body
main_body = cq.Workplane("XY").ellipse(30, 15).extrude(5)

# Cut holes
holes = cq.Workplane("XY").ellipse(30, 15).extrude(5)
inner_holes = holes.faces(">Z").workplane().circle(8).extrude(-5)
inner_holes = inner_holes.faces(">Z").workplane(centerOption='CenterOfBoundBox').move(15, 0).circle(5).cutBlind(-5)
inner_holes = inner_holes.faces(">Z").workplane(centerOption='CenterOfBoundBox').move(-15, 0).circle(5).cutBlind(-5)

# Combine main body and holes
ebracket = main_body.cut(inner_holes)

# Central block
block = cq.Workplane("XY").center(0, 0).box(8, 8, 8)

# Assemble final result
result = ebracket.union(block)