import cadquery as cq

# Parameters
width = 100
height = 70
thickness = 3.5
corner_hole_dia = 3.2
mount_hole_dia = 3.2
corner_offset = 5
cutout_radius = 10
edge_fillet = 1.0

# Base plate
plate = cq.Workplane("XY").rect(width, height).extrude(thickness)

# Side cutouts (half-circles on long edges)
plate = plate.faces(">Z").workplane().pushPoints([
    (0,  height/2),
    (0, -height/2),
]).circle(cutout_radius).cutThruAll()

# Hole positions
corner_holes = [
    (-width/2 + corner_offset, -height/2 + corner_offset),
    ( width/2 - corner_offset, -height/2 + corner_offset),
    ( width/2 - corner_offset,  height/2 - corner_offset),
    (-width/2 + corner_offset,  height/2 - corner_offset),
]
central_holes = [
    (-20,  0),
    (  0, 10),
    (  0,-10),
]
side_cluster = [
    ( 25, 10),
    ( 30,  5),
    ( 25,  0),
    ( 30, -5),
    ( 25,-10),
]

all_holes = corner_holes + central_holes + side_cluster

# Drill holes
plate = plate.faces(">Z").workplane().pushPoints(all_holes).hole(mount_hole_dia)

# Fillet all outer vertical edges
result = plate.edges("|Z").fillet(edge_fillet)