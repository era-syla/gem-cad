import cadquery as cq

# Parameters
body_length = 100
body_width = 40
body_height = 30

rail_length = 80
rail_width = 3
rail_height = 3
rail_offset_y = 12

conn_dia = 10
conn_length = 15
conn_offset_y = 8

shaft_dia = 6
shaft_length = 10

tab_length = 10
tab_width = 10
tab_thickness = 4
hole_radius = 1.5

# Main body
result = cq.Workplane("XY").box(body_length, body_width, body_height)

# Top rails
result = result.faces(">Z").workplane() \
    .center(0, rail_offset_y).rect(rail_length, rail_width).extrude(rail_height) \
    .faces(">Z").workplane() \
    .center(0, -rail_offset_y).rect(rail_length, rail_width).extrude(rail_height)

# Front connectors
result = result.faces(">X").workplane() \
    .center(0, conn_offset_y).circle(conn_dia/2).extrude(conn_length) \
    .faces(">X").workplane() \
    .center(0, -conn_offset_y).circle(conn_dia/2).extrude(conn_length)

# Back shaft
result = result.faces("<X").workplane() \
    .circle(shaft_dia/2).extrude(shaft_length)

# Mounting tabs with holes
tab_x = body_length/2 + tab_length/2
tab_y = body_width/2 + tab_width/2
tab_positions = [
    ( tab_x,  tab_y),
    ( tab_x, -tab_y),
    (-tab_x,  tab_y),
    (-tab_x, -tab_y),
]
for x, y in tab_positions:
    # Add tab
    result = result.union(
        cq.Workplane("XY")
          .transformed(offset=(x, y, -body_height/2 - tab_thickness/2))
          .box(tab_length, tab_width, tab_thickness)
    )
    # Subtract hole
    result = result.cut(
        cq.Workplane("XY")
          .transformed(offset=(x, y, -body_height/2 - tab_thickness/2))
          .circle(hole_radius)
          .extrude(tab_thickness + 1)
    )