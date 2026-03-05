import cadquery as cq

# Create the main base shape
base = (cq.Workplane("XY")
        .box(20, 60, 5)
        .faces(">Y")
        .workplane()
        .circle(15)
        .extrude(30))

# Create the hook part
hook_profile = cq.Workplane("XY").moveTo(0, 15).threePointArc((15, 15), (15, 0)).lineTo(0, 0).close()
hook = hook_profile.extrude(10).faces(">Z").workplane().hole(5, 5)

# Combine base and hook
result = base.union(hook)

# Create the vertical support and combine
support = (cq.Workplane("XZ")
           .moveTo(-10, 0)
           .lineTo(-10, 60)
           .lineTo(10, 60)
           .lineTo(10, 40)
           .threePointArc((0, 30), (-10, 40))
           .close()
           .extrude(5))

result = result.union(support)

# Create fillets
result = result.edges("|Z").fillet(2)