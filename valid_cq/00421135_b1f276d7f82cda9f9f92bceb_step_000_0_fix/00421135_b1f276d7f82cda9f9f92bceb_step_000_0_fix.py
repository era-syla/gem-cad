import cadquery as cq

# Parameters
length = 60.0
width = 20.0
thickness = 15.0
end_radius = width / 2.0
cut_length = 20.0
cut_width = width
hole_diameter = 5.0
hole_positions = [(-10.0, 0.0), (10.0, 0.0)]

# Base rectangular mid section
base = cq.Workplane("XY").rect(length - 2 * end_radius, width).extrude(thickness)

# Add rounded ends by extruding circles and unioning
left_end = cq.Workplane("XY").center(- (length / 2.0 - end_radius), 0).circle(end_radius).extrude(thickness)
right_end = cq.Workplane("XY").center(  (length / 2.0 - end_radius), 0).circle(end_radius).extrude(thickness)

result = base.union(left_end).union(right_end)

# Cut the step-shaped pocket on one side
result = result.faces(">Z").workplane().center(- (length / 2.0 - cut_length / 2.0), 0).rect(cut_length, cut_width).cutThruAll()

# Drill through holes
result = result.faces(">Z").workplane().pushPoints(hole_positions).hole(hole_diameter)

# 'result' contains the final solid
