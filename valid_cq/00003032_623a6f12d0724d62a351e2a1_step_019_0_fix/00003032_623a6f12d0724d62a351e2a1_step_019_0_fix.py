import cadquery as cq

length = 120.0
width = 20.0
height = 20.0
rod_radius = 3.0

# Create the main rectangular block, centered at the origin, length along X
result = cq.Workplane("YZ").box(width, height, length)

# Calculate the four rod centers in the YZ plane (cross‐section)
y_offset = width/2 - rod_radius
z_offset = height/2 - rod_radius
positions = [
    ( y_offset,  z_offset),
    (-y_offset,  z_offset),
    ( y_offset, -z_offset),
    (-y_offset, -z_offset),
]

# Add four rods running the full length along X
for y, z in positions:
    rod = (
        cq.Workplane("YZ")
        .workplane(origin=(y, z))
        .cylinder(length, rod_radius, centered=(True, True, True))
    )
    result = result.union(rod)