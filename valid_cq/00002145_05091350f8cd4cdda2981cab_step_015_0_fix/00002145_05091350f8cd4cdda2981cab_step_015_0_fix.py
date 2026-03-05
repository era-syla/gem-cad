import cadquery as cq

# Parameters
frame_size = 80.0
frame_thickness = 10.0
mount_hole_dia = 6.0
mount_hole_offset = frame_size / 2 - 5.0
hub_dia = 30.0
hub_height = 5.0
blade_width = 6.0
blade_length = 40.0
blade_height = hub_height
blade_offset = hub_dia / 2 + blade_length / 2

# Build main frame
result = (
    cq.Workplane("XY")
    .rect(frame_size, frame_size)
    .extrude(frame_thickness)
)

# Mounting holes at corners
for x in (-mount_hole_offset, mount_hole_offset):
    for y in (-mount_hole_offset, mount_hole_offset):
        result = (
            result
            .faces(">Z")
            .workplane()
            .pushPoints([(x, y)])
            .hole(mount_hole_dia, frame_thickness)
        )

# Top face workplane
wp = result.faces(">Z").workplane()

# Central hub
hub = wp.circle(hub_dia / 2).extrude(hub_height)
result = result.union(hub)

# One blade
blade = (
    wp
    .rect(blade_width, blade_length)
    .extrude(blade_height)
    .translate((0, blade_offset, 0))
)

# Union four blades rotated around center
for angle in (0, 90, 180, 270):
    result = result.union(blade.rotate((0, 0, 0), (0, 0, 1), angle))

# Final result
result  # variable containing the final solid geometry