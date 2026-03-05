import cadquery as cq

# Parameters
rod_diameter = 6
rod_spacing = 30
rod_length = 100
plate_thickness = 5
top_plate_length = 70
top_plate_width = 15
mid_plate_length = 50
mid_plate_width = 12
angle_top = 0
angle_mid = 30

# Create the two vertical rods
rods = (
    cq.Workplane("XY")
    .pushPoints([(-rod_spacing/2, 0), (rod_spacing/2, 0)])
    .circle(rod_diameter / 2)
    .extrude(rod_length + plate_thickness)
)

# Create the top plate
top_plate = (
    cq.Workplane("XY")
    .workplane(offset=rod_length)
    .transformed(rotate=(0, 0, angle_top))
    .rect(top_plate_length, top_plate_width)
    .extrude(plate_thickness)
)

# Create the middle plate
middle_plate = (
    cq.Workplane("XY")
    .workplane(offset=rod_length / 2)
    .transformed(rotate=(0, 0, angle_mid))
    .rect(mid_plate_length, mid_plate_width)
    .extrude(plate_thickness)
)

# Create undercut blocks beneath the middle plate
undercuts = (
    cq.Workplane("XY")
    .workplane(offset=(rod_length / 2) - plate_thickness)
    .transformed(rotate=(0, 0, angle_mid))
    .pushPoints(
        [
            (0, mid_plate_width / 3),
            (0, 0),
            (0, -mid_plate_width / 3),
        ]
    )
    .rect(6, 4)
    .extrude(-10)
)

# Combine all parts into the final result
result = rods.union(top_plate).union(middle_plate).union(undercuts)