import cadquery as cq

# Parameters
hub_radius = 10
hub_length = 20
cyl_radius = 3
cyl_length = 12
num_cyl = 7
prop_blade_length = 80
prop_blade_width = 10
prop_blade_thickness = 2

# Build central hub
hub = cq.Workplane("XY").circle(hub_radius).extrude(hub_length)
result = hub

# Add radial cylinders
for i in range(num_cyl):
    angle = 360/num_cyl * i
    cyl = (
        cq.Workplane("XY")
        .transformed(offset=(hub_length/2 + cyl_length/2, 0, 0), rotate=(0, 0, angle))
        .circle(cyl_radius)
        .extrude(cyl_length)
    )
    result = result.union(cyl)

# Define a propeller blade profile in the YZ plane
blade_profile = [
    (0, 0),
    (prop_blade_length,  prop_blade_width/2),
    (prop_blade_length, -prop_blade_width/2),
]

# Create first blade at the front of the hub
blade1 = (
    cq.Workplane("YZ")
    .transformed(offset=(hub_length, 0, 0))
    .polyline(blade_profile)
    .close()
    .extrude(prop_blade_thickness)
)

# Create opposite blade by rotating 180° around the hub axis
blade2 = blade1.rotate((0, 0, 0), (1, 0, 0), 180)

# Combine all parts
result = result.union(blade1).union(blade2)