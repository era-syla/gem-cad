import cadquery as cq

# Parameters
total_height = 40.0
drive_end_diam = 22.0
drive_end_height = 18.0
socket_end_diam = 18.0
socket_end_height = 15.0
taper_height = total_height - drive_end_height - socket_end_height

hex_size = 12.0  # Distance across flats
hex_depth = 12.0
drive_size = 12.7 # 1/2 inch square drive (approximate standard)
drive_depth = 15.0

# Create the main body profile to revolve
# We will define points for a revolution
# (0,0) is center bottom
points = [
    (0, 0),
    (drive_end_diam / 2, 0),
    (drive_end_diam / 2, drive_end_height),
    (socket_end_diam / 2, drive_end_height + taper_height),
    (socket_end_diam / 2, total_height),
    (0, total_height)
]

# Create the solid body by revolving the profile
body = cq.Workplane("XZ").polyline(points).close().revolve()

# Create the hex socket cut at the top
hex_cut = (
    cq.Workplane("XY")
    .workplane(offset=total_height)
    .polygon(6, hex_size / 0.866025, circumscribed=True) # dividing by sin(60) for circumscribed radius
    .extrude(-hex_depth)
)

# Create the square drive cut at the bottom (standard feature for sockets)
# Although not visible in the top-down view, it's essential for a socket.
# If strictly adhering ONLY to visual geometry, this might be skipped, 
# but a valid engineering model of a socket usually includes it.
square_cut = (
    cq.Workplane("XY")
    .rect(drive_size, drive_size)
    .extrude(drive_depth)
)

# Combine operations
result = body.cut(hex_cut).cut(square_cut)

# Optional: Add small fillets for realism
result = result.edges("|Z").fillet(0.5) # Fillet vertical edges (though none exist on outer cyl)
result = result.faces(">Z").edges().fillet(0.5) # Top rim fillet
result = result.faces("<Z").edges().fillet(0.5) # Bottom rim fillet

# If needed for visualization or export
if 'show_object' in globals():
    show_object(result)