import cadquery as cq

# Parameters
plate_length = 180.0
plate_width = 20.0
thickness = 5.0

mid_hole_dia = 12.0
num_mid_holes = 6
mid_spacing = 30.0

end_hole_dia = 5.0
end_offset = (num_mid_holes - 1) * mid_spacing / 2 + mid_spacing / 2

# Compute X positions for middle holes
first_mid_x = - (num_mid_holes - 1) * mid_spacing / 2
mid_positions = [(first_mid_x + i * mid_spacing, 0) for i in range(num_mid_holes)]
end_positions = [(-end_offset, 0), (end_offset, 0)]

# Build the plate
result = (
    cq.Workplane("XY")
    .rect(plate_length, plate_width)
    .extrude(thickness)
    # Drill middle holes
    .faces(">Z")
    .workplane()
    .pushPoints(mid_positions)
    .hole(mid_hole_dia)
    # Drill end holes
    .pushPoints(end_positions)
    .hole(end_hole_dia)
)