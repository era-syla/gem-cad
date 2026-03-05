import cadquery as cq
import math

# Parameters
num_teeth = 36
module = 2.0
pitch_dia = num_teeth * module
outer_dia = pitch_dia + 2 * module
root_dia = pitch_dia - 2.5 * module
thickness = 6.0
bore_dia = 10.0

outer_r = outer_dia / 2.0
root_r = root_dia / 2.0

# Compute the width of the space (chord) at the root circle
half_tooth_angle = math.pi / (2.0 * num_teeth)
space_chord = 2.0 * root_r * math.sin(half_tooth_angle)

# Create the base cylinder for the gear
base = cq.Workplane("XY").circle(outer_r).extrude(thickness)

# Build a compound of radial cutting boxes to form the spaces between teeth
cut_tool = None
cut_length = outer_dia * 2.0
for i in range(num_teeth):
    angle = 360.0 * i / num_teeth
    tooth_space = (
        cq.Workplane("XY")
        .transformed(rotate=(0, 0, angle))
        .box(space_chord, cut_length, thickness + 2.0)
    )
    cut_tool = tooth_space if cut_tool is None else cut_tool.union(tooth_space)

# Cut out the spaces to form the teeth
gear = base.cut(cut_tool)

# Add central bore
gear = gear.faces(">Z").workplane().hole(bore_dia)

# Add a D-flat on the bore
flat_cut = (
    cq.Workplane("XY")
    .box(root_r, outer_dia + 1.0, thickness + 2.0)
    .translate((root_r / 2.0, 0, thickness / 2.0))
)
gear = gear.cut(flat_cut)

result = gear