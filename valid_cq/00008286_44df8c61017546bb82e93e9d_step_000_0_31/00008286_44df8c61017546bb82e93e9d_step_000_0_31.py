import cadquery as cq

# Wheel Parameters
rim_outer_radius = 100.0
rim_inner_radius = 98.5
rim_width = 4.0
rim_fillet = 0.5

hub_outer_radius = 10.0
hub_inner_radius = 3.5
hub_width = 8.0
hub_fillet = 0.8

spoke_radius = 0.3
num_spokes = 24

# Create Rim
rim = (
    cq.Workplane("XY")
    .circle(rim_outer_radius)
    .circle(rim_inner_radius)
    .extrude(rim_width / 2.0, both=True)
    .edges()
    .fillet(rim_fillet)
)

# Create Hub
hub = (
    cq.Workplane("XY")
    .circle(hub_outer_radius)
    .circle(hub_inner_radius)
    .extrude(hub_width / 2.0, both=True)
    .edges()
    .fillet(hub_fillet)
)

# Create Spokes
spokes_list = []
for i in range(num_spokes):
    angle = i * (360.0 / num_spokes)
    
    # Alternate Z offset for the spokes at the hub to mimic a realistic wheel structure
    z_offset = (hub_width / 2.0 - 1.5) if i % 2 == 0 else -(hub_width / 2.0 - 1.5)
    
    # Start slightly inside the hub and end slightly inside the rim for clean boolean unions
    start_pt = cq.Vector(hub_outer_radius - 1.5, 0, z_offset)
    end_pt = cq.Vector(rim_inner_radius + 0.5, 0, 0)
    
    direction = end_pt - start_pt
    length = direction.Length
    direction_normalized = direction.normalized()
    
    # Make the cylindrical spoke
    spoke = cq.Solid.makeCylinder(spoke_radius, length, start_pt, direction_normalized)
    
    # Rotate into position
    spoke = spoke.rotate(cq.Vector(0, 0, 0), cq.Vector(0, 0, 1), angle)
    spokes_list.append(spoke)

# Combine all parts
result = rim.union(hub)
for spoke in spokes_list:
    result = result.union(cq.Workplane("XY").newObject([spoke]))
