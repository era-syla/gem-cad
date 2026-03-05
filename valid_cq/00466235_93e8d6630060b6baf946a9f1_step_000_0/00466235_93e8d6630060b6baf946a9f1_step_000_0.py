import cadquery as cq

# Parametric dimensions based on visual estimation
thickness = 5.0
ring_outer_dia = 22.0
ring_inner_dia = 12.0
bridge_width = 14.0
center_spacing = 35.0  # Distance from center ring to end rings
square_hole_side = 7.0

# 1. Create the three circular bosses (rings)
# Positions: Center (0,0), Left (-spacing, 0), Right (+spacing, 0)
rings = (
    cq.Workplane("XY")
    .pushPoints([(0, 0), (-center_spacing, 0), (center_spacing, 0)])
    .circle(ring_outer_dia / 2.0)
    .extrude(thickness)
)

# 2. Create the rectangular bridges connecting the rings
# Positions: Midpoint between Left and Center, Midpoint between Center and Right
bridges = (
    cq.Workplane("XY")
    .pushPoints([(-center_spacing / 2.0, 0), (center_spacing / 2.0, 0)])
    .rect(center_spacing, bridge_width)
    .extrude(thickness)
)

# 3. Combine rings and bridges into a single solid
base_body = rings.union(bridges)

# 4. Cut circular holes in the rings
body_with_circle_holes = (
    base_body.faces(">Z")
    .workplane()
    .pushPoints([(0, 0), (-center_spacing, 0), (center_spacing, 0)])
    .circle(ring_inner_dia / 2.0)
    .cutThruAll()
)

# 5. Cut square holes in the bridges
result = (
    body_with_circle_holes.faces(">Z")
    .workplane()
    .pushPoints([(-center_spacing / 2.0, 0), (center_spacing / 2.0, 0)])
    .rect(square_hole_side, square_hole_side)
    .cutThruAll()
)