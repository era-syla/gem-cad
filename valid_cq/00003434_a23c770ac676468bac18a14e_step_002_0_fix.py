import cadquery as cq
import math

# Main dimensions
outer_radius = 50
inner_radius = 38
base_height = 8
ring_height = 15
wall_thickness = 6

# Create the main ring body
result = (
    cq.Workplane("XY")
    .circle(outer_radius)
    .circle(inner_radius)
    .extrude(ring_height)
)

# Add a wider base flange (lower ring)
base_flange = (
    cq.Workplane("XY")
    .circle(outer_radius + 3)
    .circle(inner_radius - 2)
    .extrude(base_height)
)

result = result.union(base_flange)

# Add a middle groove ring (slightly narrower ring between base and top)
groove_ring = (
    cq.Workplane("XY")
    .workplane(offset=base_height - 1)
    .circle(outer_radius + 1)
    .circle(outer_radius - 1)
    .extrude(3)
)

result = result.union(groove_ring)

# Add inner bottom floor (partial - leaving opening)
# The image shows an open top ring with a diagonal bar/spoke and small hole
# Add a diagonal spoke/bar across the inner opening
spoke_width = 8
spoke_length = inner_radius * 2

spoke = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .rect(spoke_length * 0.7, spoke_width)
    .extrude(base_height + 2)
)

# Rotate spoke diagonally
spoke = spoke.rotate((0, 0, 0), (0, 0, 1), 30)

# Intersect spoke with inner cylinder to keep only what's inside
inner_cyl = (
    cq.Workplane("XY")
    .circle(inner_radius - 1)
    .extrude(base_height + 2)
)

spoke_trimmed = spoke.intersect(inner_cyl)

result = result.union(spoke_trimmed)

# Add small hole on the spoke/floor
small_hole = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .center(-10, -8)
    .circle(4)
    .extrude(base_height + 4)
)

result = result.cut(small_hole)

# Add mounting tabs/ears on the outside (visible in image - 3 tabs)
tab_width = 12
tab_height = 10
tab_depth = 8
tab_thickness = 4

# Tab positions (roughly at 3 positions around the ring)
tab_angles = [0, 120, 240]

for angle in tab_angles:
    angle_rad = math.radians(angle)
    cx = math.cos(angle_rad) * (outer_radius + 3)
    cy = math.sin(angle_rad) * (outer_radius + 3)
    
    tab = (
        cq.Workplane("XY")
        .workplane(offset=2)
        .center(cx, cy)
        .rect(tab_depth, tab_width)
        .extrude(tab_height)
    )
    
    result = result.union(tab)

# Clean up by ensuring result is solid
result = result