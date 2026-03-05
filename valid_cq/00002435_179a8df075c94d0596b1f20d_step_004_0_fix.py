import cadquery as cq

# Main cylindrical body (drum/disc shape)
outer_radius = 50
inner_radius = 44
height = 15
wall_thickness = 6

# Create the main disc body
disc = (
    cq.Workplane("YZ")
    .circle(outer_radius)
    .extrude(height)
)

# Create the rim/band around the disc
rim = (
    cq.Workplane("YZ")
    .circle(outer_radius)
    .circle(outer_radius - wall_thickness)
    .extrude(height)
)

# Front face disc (slightly larger flat disc on one side)
front_disc = (
    cq.Workplane("YZ")
    .circle(outer_radius)
    .extrude(2)
    .translate((height, 0, 0))
)

# Back face disc
back_disc = (
    cq.Workplane("YZ")
    .circle(outer_radius)
    .extrude(2)
)

# Base/stand plate at the bottom
base_plate = (
    cq.Workplane("XY")
    .rect(height + 4, outer_radius * 0.8)
    .extrude(3)
    .translate((height / 2, 0, -outer_radius + 2))
)

# Small mounting tabs/lugs on the side
lug1 = (
    cq.Workplane("XY")
    .rect(8, 8)
    .extrude(6)
    .translate((height / 2, -(outer_radius + 3), -10))
)

lug2 = (
    cq.Workplane("XY")
    .rect(8, 8)
    .extrude(6)
    .translate((height / 2, -(outer_radius + 3), -18))
)

# Small bolt/fastener holes simulation as small cylinders on rim
# Add small protrusions around the rim for texture
def make_bolt(angle_deg):
    import math
    angle_rad = math.radians(angle_deg)
    y = (outer_radius - 3) * math.cos(angle_rad)
    z = (outer_radius - 3) * math.sin(angle_rad)
    bolt = (
        cq.Workplane("YZ")
        .circle(2)
        .extrude(3)
        .translate((height / 2, y, z))
    )
    return bolt

# Combine all parts
result = disc.union(base_plate).union(lug1).union(lug2)

# Add some bolts around the rim
import math
for angle in range(0, 360, 30):
    angle_rad = math.radians(angle)
    y = outer_radius * math.cos(angle_rad)
    z = outer_radius * math.sin(angle_rad)
    small_bump = (
        cq.Workplane("YZ")
        .circle(1.5)
        .extrude(2)
        .translate((height * 0.6, y, z))
    )
    result = result.union(small_bump)