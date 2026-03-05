import cadquery as cq
import math

# Hex nut parameters
across_flats = 13.0  # M8 hex nut across flats
height = 6.5         # nut height
hole_dia = 6.8       # through hole diameter (M8 thread minor dia approx)
chamfer_size = 1.2   # top/bottom chamfer

# Calculate across corners (circumradius)
across_corners = across_flats / math.cos(math.radians(30))
hex_radius = across_flats / (2 * math.cos(math.radians(30)))

# Create hex prism
hex_nut = (
    cq.Workplane("XY")
    .polygon(6, across_corners)
    .extrude(height)
)

# Chamfer top and bottom edges
hex_nut = (
    hex_nut
    .faces(">Z")
    .edges()
    .chamfer(chamfer_size)
)

hex_nut = (
    hex_nut
    .faces("<Z")
    .edges()
    .chamfer(chamfer_size)
)

# Cut through hole
hex_nut = (
    hex_nut
    .faces(">Z")
    .workplane()
    .circle(hole_dia / 2)
    .cutThruAll()
)

# Add a bearing surface ring on top (the raised circular collar visible in image)
collar_outer = hole_dia / 2 + 1.5
collar_height = 0.8

collar = (
    cq.Workplane("XY")
    .workplane(offset=height - chamfer_size * 0.5)
    .circle(collar_outer)
    .circle(hole_dia / 2)
    .extrude(collar_height)
)

# Union collar with nut (already part of nut geometry, skip separate union)
# The image shows the nut face has a slight raised ring around the hole
# Let's add it via the main body with a slight boss

# Rebuild cleanly
result = (
    cq.Workplane("XY")
    .polygon(6, across_corners)
    .extrude(height)
)

# Chamfer top
result = result.faces(">Z").edges().chamfer(chamfer_size)

# Chamfer bottom
result = result.faces("<Z").edges().chamfer(chamfer_size)

# Through hole
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(hole_dia / 2)
    .cutThruAll()
)

# Add small raised collar ring on top face around hole
top_z = height
ring_inner = hole_dia / 2
ring_outer = ring_inner + 1.8
ring_h = 0.6

ring = (
    cq.Workplane("XY")
    .workplane(offset=top_z - chamfer_size - ring_h + 0.1)
    .circle(ring_outer)
    .extrude(ring_h)
)

ring = (
    ring
    .faces(">Z")
    .workplane()
    .circle(ring_inner)
    .cutThruAll()
)

result = result.union(ring)

# Final through hole cleanup
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(hole_dia / 2)
    .cutThruAll()
)