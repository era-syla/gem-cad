import cadquery as cq

# Create a complex layered/tiered structure that resembles the image
# The image shows a multi-layered geometric shape with various rectangular and polygonal tiers

# Base layer - large flat rectangle
base = cq.Workplane("XY").rect(80, 80).extrude(3)

# Second layer - slightly smaller with chamfered corners (octagonal-ish)
layer2 = cq.Workplane("XY").workplane(offset=3).polygon(8, 65).extrude(4)

# Third layer - even smaller octagonal
layer3 = cq.Workplane("XY").workplane(offset=7).polygon(8, 50).extrude(4)

# Inner raised platform
inner = cq.Workplane("XY").workplane(offset=11).rect(35, 35).extrude(5)

# Central small raised area
center = cq.Workplane("XY").workplane(offset=16).rect(20, 20).extrude(4)

# Combine all layers
body = base.union(layer2).union(layer3).union(inner).union(center)

# Add a diagonal bar/strap across the top (rotated rectangle)
# This is the prominent diagonal element visible in the image
bar = (cq.Workplane("XY")
       .workplane(offset=20)
       .transformed(rotate=cq.Vector(0, 0, 35))
       .rect(90, 18)
       .extrude(6))

body = body.union(bar)

# Cut some notches/slots visible in the image (dark areas)
# Left side notch
notch1 = (cq.Workplane("XY")
          .workplane(offset=7)
          .transformed(offset=cq.Vector(-28, -15, 0))
          .rect(12, 10)
          .extrude(10))

# Right side notch
notch2 = (cq.Workplane("XY")
          .workplane(offset=7)
          .transformed(offset=cq.Vector(28, 10, 0))
          .rect(12, 10)
          .extrude(10))

body = body.cut(notch1).cut(notch2)

result = body