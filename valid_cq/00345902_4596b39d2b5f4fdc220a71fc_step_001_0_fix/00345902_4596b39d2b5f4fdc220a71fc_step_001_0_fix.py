import cadquery as cq

thickness = 5.0

result = (
    cq.Workplane("XY")
    # Define the outline of the part
    .moveTo(0, 0)
    .lineTo(50, 0)
    .lineTo(90, 20)
    .lineTo(90, 80)
    .lineTo(60, 100)
    .lineTo(20, 80)
    .lineTo(30, 60)
    .threePointArc((5, 50), (0, 20))
    .close()
    # Extrude to thickness
    .extrude(thickness)
    # Create the mounting hole
    .faces(">Z")
    .workplane()
    .center(10, 5)
    .hole(5.0)
)