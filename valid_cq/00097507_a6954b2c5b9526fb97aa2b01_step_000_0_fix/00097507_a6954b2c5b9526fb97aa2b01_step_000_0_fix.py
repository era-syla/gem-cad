import cadquery as cq

# Parameters
width = 20
depth = 12
height = 40
wall = 2
hole_dia = 5
hole_depth = 10
label_w = 12
label_h = 6
label_depth = 1.5
text_size = 4
text_depth = 1

# Base box
result = cq.Workplane("XY").box(width, depth, height)

# Hollow out top
result = result.faces(">Z")\
    .workplane()\
    .rect(width-2*wall, depth-2*wall)\
    .cutBlind(-height+wall)

# Two socket holes from top
y_pos = depth/2 - wall - hole_dia/2
hole_positions = [(-4, y_pos), (4, y_pos)]
result = result.faces(">Z")\
    .workplane()\
    .pushPoints(hole_positions)\
    .hole(hole_dia, hole_depth)

# Front label recess
result = result.faces("<Y")\
    .workplane()\
    .rect(label_w, label_h)\
    .cutBlind(label_depth)

# Emboss text "XT60"
text_solid = result.faces("<Y")\
    .workplane()\
    .text("XT60", text_size, text_depth)
result = result.union(text_solid)