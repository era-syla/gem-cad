import cadquery as cq

# Parameters
center_length = 150
center_depth = 10
thickness = 5
end_bar_length = 60
end_bar_depth = center_depth

# Main beam
center = cq.Workplane("XY").box(center_length, center_depth, thickness)

# End bars perpendicular to main beam
left_bar = (
    cq.Workplane("XY")
    .box(end_bar_depth, end_bar_length, thickness)
    .translate((-center_length/2 + end_bar_depth/2, 0, 0))
)
right_bar = (
    cq.Workplane("XY")
    .box(end_bar_depth, end_bar_length, thickness)
    .translate(( center_length/2 - end_bar_depth/2, 0, 0))
)

# Combine parts
result = center.union(left_bar).union(right_bar)

# Hexagonal cut at center
result = (
    result
    .workplane(offset=thickness/2)
    .polygon(6, 20)
    .cutThruAll()
)

# Two small rectangular cutouts inside the hexagon
slot_positions = [(8, 0), (-8, 0)]
result = (
    result
    .workplane(offset=thickness/2)
    .pushPoints(slot_positions)
    .rect(4, 2)
    .cutThruAll()
)

# Three through-holes on each side face of the center beam
hole_positions = [(-30, 0), (0, 0), (30, 0)]
result = (
    result
    .faces(">Y")
    .workplane()
    .pushPoints(hole_positions)
    .hole(4)
)
result = (
    result
    .faces("<Y")
    .workplane()
    .pushPoints(hole_positions)
    .hole(4)
)