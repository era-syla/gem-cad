import cadquery as cq

# Define dimensions
base_radius = 5
cylinder_height = 40
hole_radius = 2
arm_thickness = 2

# Create the base
base = (
    cq.Workplane("XY")
    .circle(base_radius)
    .extrude(cylinder_height)
)

# Fillet the top edges
base = base.edges(">Z").fillet(3)

# Create the arm
arm = (
    cq.Workplane("XY")
    .workplane(offset=cylinder_height - arm_thickness)
    .rect(cylinder_height, arm_thickness * 2, centered=(False, True))
    .extrude(arm_thickness)
)

# Create the hole in the arm
arm_hole = (
    arm.faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .circle(hole_radius)
    .cutThruAll()
)

# Join arm to base
result = base.union(arm_hole)

# Add second arm with offset
arm_offset = (
    cq.Workplane("XZ")
    .workplane(offset=arm_thickness * 2)
    .transformed(offset=(cylinder_height, 0, 0))
    .rect(cylinder_height, arm_thickness * 2, centered=(False, True))
    .extrude(arm_thickness)
)

# Add hole to the second arm
arm_hole_offset = (
    arm_offset.faces(">Z")
    .workplane(centerOption="CenterOfMass")
    .circle(hole_radius)
    .cutThruAll()
)

# Combine everything into the final result
result = result.union(arm_hole_offset)