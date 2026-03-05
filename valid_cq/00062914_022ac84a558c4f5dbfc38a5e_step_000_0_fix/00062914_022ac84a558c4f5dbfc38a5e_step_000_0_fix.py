import cadquery as cq

thickness = 6

# Outline profile of the bracket in the XY plane
profile = [
    (-60, 5),
    (-60, 25),
    (-30, 25),
    (-30, 55),
    (30, 55),
    (30, 25),
    (60, 25),
    (60, 5),
    (-60, 5),
]

# Create the base solid
result = (
    cq.Workplane("XY")
    .polyline(profile)
    .close()
    .extrude(thickness)
)

# Add holes and slot on the top face
result = (
    result
    .faces(">Z")
    .workplane()
    # Larger 8mm holes at the upright ends
    .pushPoints([(-45, 10), (-45, 20), (45, 10), (45, 20)])
    .hole(8)
    # Medium 6mm holes at corners and mid plates
    .pushPoints([
        (-30, 15), (30, 15),
        (-30, 45), (30, 45),
        (-15, 50), (0, 50), (15, 50)
    ])
    .hole(6)
    # Large through holes (20mm) in the center plate
    .pushPoints([(-15, 40), (0, 40), (15, 40)])
    .hole(20)
    # Central vertical slot
    .pushPoints([(0, 30)])
    .rect(6, 30)
    .cutThruAll()
)

# 'result' now contains the final bracket geometry.