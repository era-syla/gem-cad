import cadquery as cq

# Base Plate Dimensions
base_thick = 8
base_half_w = 50

# Create the base plate contour with rear arms and central U-gap
base_wp = (
    cq.Workplane("XY")
    .moveTo(base_half_w, 35)
    .lineTo(-base_half_w, 35)
    .lineTo(-base_half_w, -60)
    # Left arm rounded end
    .threePointArc((-35, -75), (-20, -60))
    # Left arm inner edge
    .lineTo(-20, -30)
    # Center U-gap (semicircular cutout pointing forwards)
    .threePointArc((0, -10), (20, -30))
    # Right arm inner edge
    .lineTo(20, -60)
    # Right arm rounded end
    .threePointArc((35, -75), (base_half_w, -60))
    .close()
    .extrude(base_thick)
)

# Fillet the two front corners
base = base_wp.edges("|Z").edges(">Y").fillet(8)

# Add 4 through holes (2 front, 2 at rear arm centers)
holes_pts = [(-40, 25), (40, 25), (-35, -60), (35, -60)]
base = base.faces("<Z").workplane().pushPoints(holes_pts).hole(6)

# Central Body Dimensions
body_h = 35

# Create central body profile with front half-cylinder and rear "bat-shaped" cutout
body_wp = (
    cq.Workplane("XY").workplane(offset=base_thick)
    .moveTo(30, 0)
    # Front half cylinder
    .threePointArc((0, 30), (-30, 0))
    # Left straight side
    .lineTo(-30, -25)
    # Back left flat edge
    .lineTo(-20, -25)
    # Left inward bat curve
    .threePointArc((-10, -12), (0, -18))
    # Right inward bat curve
    .threePointArc((10, -12), (20, -25))
    # Back right flat edge
    .lineTo(30, -25)
    .close()
    .extrude(body_h)
)

# Create the horizontal side slot (pocket on the left face)
slot = (
    cq.Workplane("XY").workplane(offset=23) # Center Z height of the slot
    .center(-15, -15)                       # Center X, Y of the slot
    .box(40, 20, 10)                        # Width, Depth, Height
)
body = body_wp.cut(slot)

# Combine the base and body into the final solid
result = base.union(body)