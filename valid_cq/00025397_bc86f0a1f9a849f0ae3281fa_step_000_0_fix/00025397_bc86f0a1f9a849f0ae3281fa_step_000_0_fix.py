import cadquery as cq

# Base of the vise
base = cq.Workplane("XY").box(100, 50, 10)

# Fixed jaw
fixed_jaw = (
    base.faces(">Z").workplane()
    .center(-35, 0)
    .rect(30, 50)
    .extrude(40)
)

# Movable jaw
movable_jaw = (
    base.faces(">Z").workplane()
    .center(15, 0)
    .rect(30, 50)
    .extrude(40)
)

# Lead screw (simplified)
lead_screw = (
    base.faces(">Z").workplane()
    .center(0, 0)
    .circle(5)
    .extrude(70)
)

# Handles on lead screw
handle = (
    lead_screw.faces(">Z[-2]").workplane()
    .center(0, 0)
    .circle(15)
    .extrude(5)
)

# Combine all parts
result = base.union(fixed_jaw).union(movable_jaw).union(lead_screw).union(handle)