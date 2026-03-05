import cadquery as cq

# Parameters
bolt_diameter = 5
bolt_length = 40
hex_size = 8.5
hex_height = 5
chamfer_size = 0.5
thread_diameter = 5
thread_pitch = 1.25

# Bolt head
bolt_head = cq.Workplane("XY").polygon(6, hex_size).extrude(hex_height)
bolt_head = bolt_head.faces(">Z").workplane().circle(bolt_diameter / 2).extrude(bolt_length)

# Chamfer the edges of the hex head
bolt_head = bolt_head.edges("|Z").chamfer(chamfer_size)

# Create thread
thread = bolt_head.faces(">Z").workplane().circle(thread_diameter / 2).extrude(-bolt_length, combine=False)
bolt = bolt_head.cut(thread)

# Nut
nut = cq.Workplane("XY").polygon(6, hex_size).extrude(hex_height)
nut = nut.faces(">Z").workplane().circle(thread_diameter / 2).cutThruAll()

result = bolt.union(nut.translate((20, 0, 0)))