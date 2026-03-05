import cadquery as cq

# Parameters
rail_length = 300
rail_width = 15
rail_height = 10

vert_plate_th = 5
vert_plate_height = 100

frame_outer = 200
frame_inner = 180
frame_thickness = 5

truss_thickness = 5

# Horizontal rail
rail = cq.Workplane("XY").box(rail_length, rail_width, rail_height)

# Vertical support plate at mid-rail
vert = (
    cq.Workplane("XY")
    .workplane(origin=(rail_length/2, 0, rail_height))
    .rect(vert_plate_th, rail_width)
    .extrude(vert_plate_height)
)

# Square frame on top of the vertical plate
frame = (
    cq.Workplane("XY")
    .workplane(origin=(rail_length/2, 0, rail_height + vert_plate_height))
    .rect(frame_outer, frame_outer)
    .rect(frame_inner, frame_inner)
    .extrude(frame_thickness)
)

# Triangular truss at the right end of the rail
truss_points = [(-50, -50), (50, -50), (0, 0)]
truss = (
    cq.Workplane("XY")
    .workplane(origin=(rail_length, 0, rail_height))
    .polyline(truss_points)
    .close()
    .extrude(truss_thickness)
)

# Combine all parts
result = rail.union(vert).union(frame).union(truss)