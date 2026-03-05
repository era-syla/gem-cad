import cadquery as cq

# Parameters
plate_thickness = 4.0
corner_fillet = 5.0
pocket_offset = 8.0
pocket_depth = 1.5
boss_diameter = 6.0
boss_height = 12.0
hole_diameter = 2.5

# Triangle plate outline
pts = [(0, 0), (100, 0), (30, 80)]

# Positions for bosses (offset a bit from corners)
boss_pts = [(15, 15), (85, 15), (30, 65)]

# Positions for small through-holes
hole_pts = [(50, 40), (40, 55)]

# Inner pocket outline (offset inward)
inner_pts = [
    (pocket_offset, pocket_offset),
    (100 - pocket_offset, pocket_offset),
    (30, 80 - pocket_offset),
]

# Build the plate
result = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(plate_thickness)
    .edges("|Z")
    .fillet(corner_fillet)
    # Add bosses on top face
    .faces(">Z")
    .workplane()
    .pushPoints(boss_pts)
    .circle(boss_diameter / 2)
    .extrude(boss_height)
    # Drill holes through bosses and plate
    .faces(">Z")
    .workplane()
    .pushPoints(boss_pts)
    .hole(hole_diameter, plate_thickness + boss_height)
    # Drill additional small holes in plate
    .faces(">Z")
    .workplane()
    .pushPoints(hole_pts)
    .hole(3.0, plate_thickness)
    # Cut a shallow pocket on top face
    .faces(">Z")
    .workplane()
    .polyline(inner_pts)
    .close()
    .cutBlind(-pocket_depth)
)

result  # final geometry stored in 'result' variable