import cadquery as cq

# Parameters
gear_diameter = 50
gear_thickness = 10
hole_diameter = 10
hole_spacing = 20
num_teeth = 40
tooth_depth = 2

# Create base cylinder
base = cq.Workplane("XY").circle(gear_diameter / 2).extrude(gear_thickness)

# Cut center hole
base = base.faces(">Z").workplane().circle(hole_diameter / 2).cutBlind(-gear_thickness)

# Create teeth
tooth_profile = (
    cq.Workplane("XY")
    .circle(gear_diameter / 2)
    .workplane(offset=tooth_depth)
    .circle((gear_diameter / 2) - tooth_depth)
    .loft()
)

# Polar array of teeth
teeth = (
    tooth_profile.faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .polarArray(gear_diameter / 2, 0, 360, num_teeth, True)
    .union()
)

# Combine base and teeth
result = base.union(teeth)

# Cut holes in gear
result = (
    result.faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .rarray(hole_spacing, hole_spacing, 2, 2)
    .hole(hole_diameter)
)