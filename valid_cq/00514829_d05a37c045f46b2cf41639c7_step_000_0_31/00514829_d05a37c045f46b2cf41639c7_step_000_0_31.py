import cadquery as cq

# Base Plate
base = (
    cq.Workplane("XY")
    .moveTo(0, -25)
    .spline([
        (20, -24),
        (50, -12)
    ], includeCurrent=True)
    .lineTo(50, -2)
    .spline([
        (35, 2),
        (22, 12),
        (16, 25),
        (0, 30),
        (-20, 32),
        (-38, 25),
        (-40, 5),
        (-30, -20),
        (-15, -25),
        (0, -25)
    ], includeCurrent=True)
    .close()
    .extrude(10)
)

# Central Tier 1
tier1 = cq.Workplane("XY", origin=(0, 0, 10)).circle(16).extrude(14)

# Central Tier 2
tier2 = cq.Workplane("XY", origin=(0, 0, 24)).circle(6).extrude(16)

# Front Left Ellipse
fl_shape = (
    cq.Workplane("XY", origin=(-16, -16, 10))
    .ellipse(10, 6)
    .extrude(20)
)

# Left Back Shape
lb_shape = (
    cq.Workplane("XY", origin=(0, 0, 10))
    .moveTo(-12, 6)
    .lineTo(-25, 10)
    .lineTo(-28, 25)
    .lineTo(-12, 25)
    .close()
    .extrude(24)
    .edges("|Z").fillet(4)
)

# Right Back Cylinder
rb_shape = cq.Workplane("XY", origin=(12, 16, 10)).circle(4.5).extrude(32)

# Right Front Prism
rf_shape = (
    cq.Workplane("XY", origin=(0, 0, 10))
    .moveTo(12, -2)
    .lineTo(12, -18)
    .lineTo(26, -2)
    .close()
    .extrude(22)
)

# Combine all components into the final result
result = (
    base
    .union(tier1)
    .union(tier2)
    .union(fl_shape)
    .union(lb_shape)
    .union(rb_shape)
    .union(rf_shape)
)