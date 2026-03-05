import cadquery as cq

# Parameter definitions
bar_height = 300.0
bar_width = 30.0
bar_thickness = 15.0
hole_diameter = 6.0
hole_spacing = 15.0
hole_depth = 25.0

# Generate the 3D model
result = (
    cq.Workplane("XY")
    .box(bar_width, bar_thickness, bar_height)
    .faces(">Z")
    .workplane()
    .pushPoints([(-hole_spacing / 2.0, 0), (hole_spacing / 2.0, 0)])
    .hole(hole_diameter, hole_depth)
)