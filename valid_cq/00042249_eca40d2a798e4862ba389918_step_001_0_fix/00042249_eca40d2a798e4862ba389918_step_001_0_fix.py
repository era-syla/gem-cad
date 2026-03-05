import cadquery as cq

# parameters
d = 12     # tube diameter
r = 20     # bend radius
h = 60     # initial vertical height
l1 = 120   # first straight length
l2 = 40    # final drop length

# build the sweep path in the XZ plane
path = (
    cq.Workplane("XZ")
      .moveTo(0, 0)
      .lineTo(0, h)
      .radiusArc((r, h + r), r)
      .lineTo(r + l1, h + r)
      .radiusArc((r + l1 + r, h), r)
      .lineTo(r + l1 + r, h - l2)
      .wire()
)

# sweep a circle along that path to create the tube
result = (
    cq.Workplane("YZ")
      .circle(d / 2)
      .sweep(path, isFrenet=True)
)