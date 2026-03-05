import cadquery as cq

# Parametric Dimensions
ring_od = 25.0          # Outer diameter of the rings
ring_id = 19.0          # Inner diameter of the rings
height = 6.0            # Height of the part
radius = 32.0           # Distance from center 0,0 to the center of outer rings
connector_width = 5.0   # Width of the rectangular bridges

# 1. Base Geometry Construction
# Create the central cylinder solid
center_geo = cq.Workplane("XY").circle(ring_od / 2.0).extrude(height)

# Create the three outer cylinders using a polar array
outer_geo = (
    cq.Workplane("XY")
    .polarArray(radius, 0, 360, 3)
    .circle(ring_od / 2.0)
    .extrude(height)
)

# Create the connecting bridges
# The rectangles are positioned at half the radius, spanning the full distance
# rotate=True aligns the rectangle with the radial direction
connectors_geo = (
    cq.Workplane("XY")
    .polarArray(radius / 2.0, 0, 360, 3, rotate=True)
    .rect(radius, connector_width)
    .extrude(height)
)

# Union the solid components to form a single body
solid_base = center_geo.union(outer_geo).union(connectors_geo)

# 2. Cut Holes
# Cut the hole in the central ring
result = solid_base.faces(">Z").workplane().circle(ring_id / 2.0).cutThruAll()

# Cut the holes in the three outer rings
result = (
    result.faces(">Z")
    .workplane()
    .polarArray(radius, 0, 360, 3)
    .circle(ring_id / 2.0)
    .cutThruAll()
)