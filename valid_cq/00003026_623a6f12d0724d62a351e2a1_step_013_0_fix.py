import cadquery as cq

# Flexible shaft coupling
# Main dimensions
outer_radius = 20
height = 30
inner_radius = 5
wall_thickness = 3

# Create main cylinder body
result = (
    cq.Workplane("XY")
    .cylinder(height, outer_radius)
)

# Cut central bore (top half)
result = (
    result
    .faces(">Z")
    .workplane()
    .hole(inner_radius * 2)
)

# Cut central bore (bottom half) - separate hole from bottom
result = (
    result
    .faces("<Z")
    .workplane()
    .hole(inner_radius * 2)
)

# Add groove cuts around the middle - helical flex grooves
# These are the spiral/helical cuts visible in the middle section
# Simulate with angled slots cut from the side

# Cut horizontal grooves (the flex grooves in the middle)
groove_depth = 3
groove_width = 1.5

# Upper groove set - cut slots that go almost all the way around
# We'll use rectangular cuts rotated around the cylinder

# Groove positions along Z axis
groove_positions = [-5, -2.5, 0, 2.5, 5]

for z_pos in groove_positions:
    # Cut groove from one side (leaves a small tab on the other side)
    result = (
        result
        .workplane(offset=z_pos)
        .transformed(offset=(0, 0, 0))
        .rect(outer_radius * 2 + 2, groove_width)
        .cutBlind(-groove_depth)
    )

# Actually rebuild with proper approach using shell cuts
# Start fresh with a cleaner approach

result = cq.Workplane("XY").cylinder(height, outer_radius)

# Central through hole - top
result = result.faces(">Z").workplane().hole(inner_radius * 2)

# The flex coupling has two halves connected by helical cuts
# Top half clamping slit
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, 0)
    .rect(outer_radius * 2 + 2, 1.5)
    .cutBlind(-height * 0.4)
)

# Bottom half clamping slit (rotated 90 degrees)
result = (
    result
    .faces("<Z")
    .workplane()
    .transformed(rotate=(0, 0, 90))
    .rect(outer_radius * 2 + 2, 1.5)
    .cutBlind(-height * 0.4)
)

# Add flex grooves in the middle section
for z_offset in [-6, -3, 0, 3, 6]:
    # Cut from +X side (leaves tab on -X side)
    result = (
        result
        .workplane(offset=z_offset)
        .center(outer_radius / 4, 0)
        .rect(outer_radius * 1.5, 1.2)
        .cutBlind(-groove_depth)
    )

# Add screw holes for clamping (visible as circular holes on the side)
# Top half screw hole
result = (
    result
    .workplane(offset=height * 0.25)
    .transformed(rotate=(90, 0, 0))
    .center(0, height * 0.25)
    .circle(3)
    .cutThruAll()
)

# Bottom half screw hole (rotated 90 degrees)
result = (
    result
    .workplane(offset=-height * 0.25)
    .transformed(rotate=(90, 0, 90))
    .center(0, -height * 0.25)
    .circle(3)
    .cutThruAll()
)

# Chamfer top and bottom edges
result = (
    result
    .edges(">Z or <Z")
    .chamfer(1.0)
)