import cadquery as cq

# Parameters
rod_length = 200.0
rod_radius = 1.5
head_length = 5.0
head_width = 5.0
head_height = 3.0
post_length = 2.0
post_width = 4.0
post_height = 1.0

# Build rod
result = cq.Workplane("XY").circle(rod_radius).extrude(rod_length)

# Add head block at end of rod
result = result.faces(">Z").workplane().rect(head_width, head_length).extrude(head_height)

# Add small post on top of head
result = result.faces(">Z").workplane().rect(post_width, post_length).extrude(post_height)