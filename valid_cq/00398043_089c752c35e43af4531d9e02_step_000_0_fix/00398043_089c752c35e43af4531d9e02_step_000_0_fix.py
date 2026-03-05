import cadquery as cq

length = 120
width = 20
height = 10
pocket_depth = 3

# Outer curved handle shape
result = (
    cq.Workplane("XZ")
      .polyline([
          (0, 0),
          (30, 5),
          (90, 5),
          (length, 0),
          (length, -height),
          (0, -height)
      ])
      .close()
      .extrude(width)
)

# Pocket on top face
result = (
    result
      .faces(">Y")
      .workplane()
      .rect(length - 20, height - 4)
      .cutBlind(pocket_depth)
)

# Internal cylindrical posts in pocket
post_z = - (height - pocket_depth) / 2
post_positions = [(length * 0.25, post_z), (length * 0.75, post_z)]
result = (
    result
      .faces("<Y")
      .workplane()
      .pushPoints(post_positions)
      .circle(2.5)
      .extrude(pocket_depth)
)

# Drill through-holes in those posts
result = (
    result
      .faces("<Y")
      .workplane()
      .pushPoints(post_positions)
      .circle(1.5)
      .cutBlind(pocket_depth + height)
)

# Central rectangular boss inside pocket
result = (
    result
      .faces("<Y")
      .workplane()
      .center(length/2, post_z)
      .rect(10, 5)
      .extrude(pocket_depth)
)

# Bolt-clearance holes at ends
bolt_positions = [(length * 0.1, -height/2), (length * 0.9, -height/2)]
result = (
    result
      .faces("<Y")
      .workplane()
      .pushPoints(bolt_positions)
      .circle(1.5)
      .cutBlind(height + 2)
)