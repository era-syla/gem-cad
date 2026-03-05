import cadquery as cq

# Parameters
L = 80          # total length of the bar
W = 20          # total width of the bar
T = 5           # thickness
hole_d = 6      # hole diameter
pocket_depth = 2
pocket_length = 6
pocket_offset = 12
R = W/2         # radius for the semicircular ends

result = (
    cq.Workplane("XY")
    # Draw the capsule (rectangle + semicircles) 2D profile
    .moveTo(-L/2 + R,  W/2)
    .lineTo( L/2 - R,  W/2)
    .threePointArc(( L/2, 0), ( L/2 - R, -W/2))
    .lineTo(-L/2 + R, -W/2)
    .threePointArc((-L/2, 0), (-L/2 + R,  W/2))
    .close()
    # Extrude to thickness
    .extrude(T)
    # Create a workplane on the top face
    .faces(">Z")
    .workplane()
    # Drill the two end holes at the semicircle centers
    .pushPoints([( L/2 - R, 0), (-(L/2 - R), 0)])
    .hole(hole_d)
    # Cut the two rectangular grooves near each end
    .pushPoints([( L/2 - R - pocket_offset, 0), (-(L/2 - R - pocket_offset), 0)])
    .rect(pocket_length, W)
    .cutBlind(pocket_depth)
)

result