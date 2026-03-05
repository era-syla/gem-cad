import cadquery as cq

# Create individual components of what appears to be a mechanical assembly
# Components: a curved blade/wing, a connecting arm, small cylinders/bushings, and a pin

# 1. Curved blade/wing (the large curved piece on the right)
blade = (
    cq.Workplane("XY")
    .ellipse(15, 45)
    .extrude(3)
)

# Create the curved/tapered profile for the blade
blade = (
    cq.Workplane("XZ")
    .moveTo(0, 0)
    .lineTo(15, 0)
    .threePointArc((20, 22), (15, 45))
    .lineTo(0, 45)
    .close()
    .extrude(3)
)

# Use a simpler approach - lofted blade shape
blade_bottom = cq.Workplane("XY").ellipse(8, 3).wires().toPending()
blade_profile = (
    cq.Workplane("XY")
    .workplane(offset=90)
    .ellipse(2, 1)
    .wires()
    .toPending()
)

# Simple curved blade using sweep approach
blade_path = (
    cq.Workplane("XZ")
    .spline([(0, 0), (5, 20), (3, 45), (0, 50)])
)

# Build blade as extruded and then cut to shape
blade = (
    cq.Workplane("XY")
    .ellipse(12, 40)
    .extrude(4)
)

# 2. Connecting arm (elongated flat bar)
arm = (
    cq.Workplane("XY")
    .rect(80, 8)
    .extrude(3)
    .edges("|Z")
    .fillet(3)
)

# Add hole at one end of arm
arm = (
    arm
    .faces(">Z")
    .workplane()
    .center(-35, 0)
    .circle(2.5)
    .cutThruAll()
)

# 3. Large bushing/wheel
bushing_large = (
    cq.Workplane("XY")
    .circle(12)
    .extrude(8)
    .faces(">Z")
    .workplane()
    .circle(5)
    .cutThruAll()
)

# 4. Small bushing
bushing_small = (
    cq.Workplane("XY")
    .circle(8)
    .extrude(6)
    .faces(">Z")
    .workplane()
    .circle(3)
    .cutThruAll()
)

# 5. Small cylinder/spacer
spacer = (
    cq.Workplane("XY")
    .circle(4)
    .extrude(10)
    .faces(">Z")
    .workplane()
    .circle(2)
    .cutThruAll()
)

# 6. Pin/bolt
pin = (
    cq.Workplane("XY")
    .circle(2)
    .extrude(20)
)

# Position components in an exploded view arrangement
blade_positioned = blade.translate((80, 20, 0))
arm_positioned = arm.translate((20, -20, 0))
bushing_large1 = bushing_large.translate((-40, 20, 0))
bushing_large2 = bushing_large.translate((-55, 5, 0))
bushing_small_pos = bushing_small.translate((-30, -30, 0))
spacer_pos = spacer.translate((35, -15, 0))
pin_pos = pin.translate((-20, 40, 0))

# Combine all components into result
result = (
    blade_positioned
    .union(arm_positioned)
    .union(bushing_large1)
    .union(bushing_large2)
    .union(bushing_small_pos)
    .union(spacer_pos)
    .union(pin_pos)
)