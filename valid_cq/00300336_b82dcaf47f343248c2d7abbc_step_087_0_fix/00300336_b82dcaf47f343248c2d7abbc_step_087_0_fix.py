import cadquery as cq

# Parameters
length = 200.0
width = 20.0
plate_thickness = 3.0
wall_height = 10.0
wall_thickness = 2.0
hole_dia = 5.0
hole_count = 9
scallop_radius = 2.0
scallop_count = 9
end_offset = 10.0

hole_spacing = (length - 2 * end_offset) / (hole_count - 1)
scallop_spacing = (length - 2 * end_offset) / (scallop_count - 1)

# Create U-profile extrusion
profile = [
    (-width/2, 0),
    ( width/2, 0),
    ( width/2, -wall_height),
    ( width/2 - wall_thickness, -wall_height),
    ( width/2 - wall_thickness, -plate_thickness),
    (-width/2 + wall_thickness, -plate_thickness),
    (-width/2 + wall_thickness, -wall_height),
    (-width/2, -wall_height),
]
result = cq.Workplane("YZ").polyline(profile).close().extrude(length)

# Top holes
hole_pts = [(end_offset + i * hole_spacing, 0) for i in range(hole_count)]
result = result.faces(">Z").workplane().pushPoints(hole_pts).hole(hole_dia)

# Scallops on one side wall
scallop_pts = [(end_offset + i * scallop_spacing, -wall_height/2) for i in range(scallop_count)]
result = result.faces(">Y").workplane().pushPoints(scallop_pts).circle(scallop_radius).cutThruAll()