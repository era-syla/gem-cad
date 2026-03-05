import cadquery as cq

# Parameters
base_thickness = 5
base_radius = 30
hole_radius = 10
recess_inner_radius = 20
recess_depth = 2
arm_length = 40
arm_width = 10
rail_width = 4
rail_height = 2

# Base disk
base = cq.Workplane("XY").circle(base_radius).extrude(base_thickness)

# Central hole
base = base.faces(">Z").workplane().circle(hole_radius).cutThruAll()

# Recess around hole
base = base.faces(">Z").workplane().circle(recess_inner_radius).cutBlind(recess_depth)

# Arm extrusion
arm = (
    cq.Workplane("XY")
    .transformed(offset=(base_radius + arm_length/2, 0, 0))
    .rect(arm_length, arm_width)
    .extrude(base_thickness)
)

# Raised rail on arm
rail = (
    cq.Workplane("XY")
    .transformed(offset=(base_radius + arm_length/2, 0, base_thickness))
    .rect(arm_length, rail_width)
    .extrude(rail_height)
)

# Combine all parts
result = base.union(arm).union(rail)