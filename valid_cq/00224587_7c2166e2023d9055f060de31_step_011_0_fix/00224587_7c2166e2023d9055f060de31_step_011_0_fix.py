import cadquery as cq

# Parameters
base_length = 100
base_width = 50
base_height = 3
corner_radius = 5
hole_diameter = 3
standoff_height = 10
standoff_diameter = 10

# Create base plate
base = (
    cq.Workplane("XY")
    .rect(base_length, base_width)
    .extrude(base_height)
    .edges("|Z").fillet(corner_radius)
)

# Positions for standoffs
standoff_positions = [
    (-base_length/2 + corner_radius, -base_width/2 + corner_radius),
    (base_length/2 - corner_radius, -base_width/2 + corner_radius),
    (-base_length/2 + corner_radius, base_width/2 - corner_radius),
    (base_length/2 - corner_radius, base_width/2 - corner_radius)
]

# Add standoffs
standoffs = (
    cq.Workplane("XY")
    .pushPoints(standoff_positions)
    .circle(standoff_diameter / 2)
    .extrude(standoff_height)
)

# Add holes in standoffs
holes = (
    standoffs.faces(">Z")
    .workplane()
    .circle(hole_diameter / 2)
    .cutThruAll()
)

# Combine all parts
result = base.union(standoffs).cut(holes)