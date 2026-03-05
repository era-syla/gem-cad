import cadquery as cq

length = 300
width = 150
thickness = 3
pattern_length = 25
pattern_width = 25
spacing = 2

plate = cq.Workplane("XY").box(length, width, thickness)

pattern = cq.Workplane("XY").rarray(pattern_length + spacing, pattern_width + spacing, 6, 4).box(pattern_length, pattern_width, thickness)

result = plate.cut(pattern)