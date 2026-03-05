import cadquery as cq

# Base block
base_height = 100
base_width = 20
base = cq.Workplane("XY").box(base_width, 60, base_height)

# Bottom arc
bottom_arc = cq.Workplane("XY").center(0, -30).circle(30).extrude(base_width)

# Combine base and arc
combined_base = base.union(bottom_arc)

# Holes in the base
combined_base = combined_base.faces(">Z").workplane().rarray(30, 30, 2, 3).hole(5)

# Vertical rectangle feature
vertical_feature = cq.Workplane("XY").center(0, -50).rect(20, 30).extrude(40)

# Upper block
upper_block = cq.Workplane("XY").center(0, -50).workplane(offset=40).rect(30, 30).extrude(10)

# Pin on vertical feature
pin = cq.Workplane("XY").center(0, -50).workplane(offset=35).circle(5).extrude(5)

# Combine all parts together
result = combined_base.union(vertical_feature).union(upper_block).union(pin)