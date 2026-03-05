import cadquery as cq

# Parameters
length = 120
width = 20
height = 15
chamfer_size = 2
slot_clearance = 10
side_window_clearance = 4
boss_length = 20
boss_width = 4
boss_height = 2

# Base prism
result = cq.Workplane("XY").box(length, width, height)

# Chamfer all vertical edges
result = result.edges("|Z").chamfer(chamfer_size)

# Cut a centered slot through the top face
result = result.faces(">Z").workplane().rect(length - slot_clearance, width - side_window_clearance).cutThruAll()

# Cut side windows on both long faces
result = result.faces(">Y").workplane().rect(length - slot_clearance, height - side_window_clearance).cutThruAll()
result = result.faces("<Y").workplane().rect(length - slot_clearance, height - side_window_clearance).cutThruAll()

# Add a central boss on the top face
result = result.faces(">Z").workplane().rect(boss_length, boss_width).extrude(boss_height)