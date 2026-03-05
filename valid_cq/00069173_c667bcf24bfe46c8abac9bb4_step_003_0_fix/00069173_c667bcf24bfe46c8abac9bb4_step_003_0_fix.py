import cadquery as cq

# Vertical plate
vertical = cq.Workplane("XZ", origin=(0, 0, 50)) \
    .rect(100, 100) \
    .extrude(5)

# Horizontal base plate with two mounting holes
horizontal = (
    cq.Workplane("XY", origin=(0, 20, 0))
      .rect(100, 40)
      .extrude(5)
      .faces(">Z")
      .workplane()
      .pushPoints([(-40, 10), (40, 10)])
      .hole(6)
)

# Combine plates
combined = vertical.union(horizontal)

# Cut the large central hole and four corner holes in the vertical plate
result = (
    combined
      .faces(">Y")
      .workplane()
      .circle(40)
      .cutThruAll()
      .pushPoints([(-40, -40), (-40, 40), (40, -40), (40, 40)])
      .hole(6)
)