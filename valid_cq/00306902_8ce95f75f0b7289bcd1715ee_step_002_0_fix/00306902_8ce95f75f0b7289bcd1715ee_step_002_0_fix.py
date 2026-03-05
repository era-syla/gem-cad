import cadquery as cq

# Parameters
outer_r = 50.0
wall_t = 5.0
base_h = 10.0
bottom_t = 2.0
text_h = 7.0
text_size = 20.0
cavity_r = outer_r - wall_t

# Create base cylinder
base = cq.Workplane("XY").circle(outer_r).extrude(base_h)

# Cut inner cavity leaving bottom thickness
base = base.faces(">Z").workplane().circle(cavity_r).cutBlind(-(base_h - bottom_t))

# Create 3D text inside the cavity
text = cq.Workplane("XY", origin=(0, 0, bottom_t)).text("NYC?", text_size, text_h)

# Create a few random posts inside the cavity
post1 = cq.Workplane("XY", origin=(20,  20, bottom_t)).circle(3).extrude(text_h + 1)
post2 = cq.Workplane("XY", origin=(-20, 15, bottom_t)).circle(4).extrude(text_h + 1)
post3 = cq.Workplane("XY", origin=(15, -20, bottom_t)).circle(2.5).extrude(text_h + 1)
post4 = cq.Workplane("XY", origin=(-15, -20, bottom_t)).circle(3.5).extrude(text_h + 1)

# Combine all parts into the final result
result = base.union(text).union(post1).union(post2).union(post3).union(post4)