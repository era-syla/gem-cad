import cadquery as cq

# Define parameters
hub_radius = 5
hub_thickness = 3
blade_length = 50
blade_width = 5
blade_thickness = 1
blade_twist_angle = 30

# Create hub
hub = cq.Workplane("XY").circle(hub_radius).extrude(hub_thickness)

# Create one blade
blade = (
    cq.Workplane("XY")
    .moveTo(hub_radius, 0)
    .lineTo(hub_radius + blade_length, blade_width / 2)
    .lineTo(hub_radius + blade_length, -blade_width / 2)
    .close()
    .extrude(blade_thickness)
    .rotate((0, 0, 0), (0, 0, 1), blade_twist_angle)
)

# Mirror blade to create the opposite blade
opposite_blade = blade.mirror("YZ")

# Combine hub and blades
result = hub.union(blade).union(opposite_blade)