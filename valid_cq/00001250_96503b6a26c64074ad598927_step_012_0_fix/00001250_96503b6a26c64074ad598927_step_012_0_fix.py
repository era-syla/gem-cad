import cadquery as cq

# Parameters
length = 200
width = 40
thickness = 5

# Base plate
result = cq.Workplane("XY").rect(length, width).extrude(thickness)

# Central large hole
result = result.faces(">Z").workplane().hole(60)

# Small screw holes at corners
corner_points = [
    (-length/2 + 10, -width/2 + 10),
    ( length/2 - 10, -width/2 + 10),
    ( length/2 - 10,  width/2 + -10),
    (-length/2 + 10,  width/2 - 10),
]
result = result.faces(">Z").workplane().pushPoints(corner_points).hole(5)

# Additional small holes near center
mid_points = [(0, width/4), (0, -width/4)]
result = result.faces(">Z").workplane().pushPoints(mid_points).hole(5)

# Bosses (raised collars)
boss_specs = [
    (-70, 0, 10, 3),  # x, y, diameter, height
    ( 70, 0, 15, 3),
]
for x, y, dia, h in boss_specs:
    result = (
        result.faces(">Z")
        .workplane()
        .pushPoints([(x, y)])
        .circle(dia/2)
        .extrude(h)
    )

# Ribs on top surface
rib_angles = [45, 0, -45]
for angle in rib_angles:
    rib = (
        cq.Workplane("XY")
        .transformed(offset=(0, 0, thickness), rotate=(0, 0, angle))
        .rect(length - 30, 2)
        .extrude(2)
    )
    result = result.union(rib)