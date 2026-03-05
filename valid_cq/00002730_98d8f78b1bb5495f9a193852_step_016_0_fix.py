import cadquery as cq

# Main disc base
base_radius = 40
base_height = 12

# Create the main disc
base = cq.Workplane("XY").cylinder(base_height, base_radius)

# Add fillet to top edge of base
base = base.edges(">Z").fillet(2.5)

# Add small cylindrical hub on top
hub_radius = 8
hub_height = 8

hub = cq.Workplane("XY").workplane(offset=base_height).cylinder(hub_height, hub_radius)

# Add fillet to top edge of hub
hub = hub.edges(">Z").fillet(1.5)

# Combine base and hub
result = base.union(hub)

# Add a small hole/depression on top of hub
hole_radius = 3
hole_depth = 2

result = result.cut(
    cq.Workplane("XY")
    .workplane(offset=base_height + hub_height - hole_depth)
    .circle(hole_radius)
    .extrude(hole_depth + 1)
)