import cadquery as cq

# Thickness of the plates
t = 2.0

# Right Part - Largest Plate
right = (
    cq.Workplane("XY")
    .rect(42, 42)
    .extrude(t)
    .edges("|Z")
    .fillet(3)
    .faces(">Z")
    .workplane()
    .hole(16)  # Center hole
    .faces(">Z")
    .workplane()
    .rect(31, 31, forConstruction=True)
    .vertices()
    .hole(3)  # Corner mounting holes
    .faces(">Z")
    .workplane()
    .pushPoints([(-9, -15.5)])
    .hole(2)  # Extra small hole
)

# Middle Part - Medium Plate
middle = (
    cq.Workplane("XY")
    .rect(34, 34)
    .extrude(t)
    .edges("|Z")
    .fillet(3)
    .faces(">Z")
    .workplane()
    .hole(12)  # Center hole
    .faces(">Z")
    .workplane()
    .rect(24, 24, forConstruction=True)
    .vertices()
    .hole(2.5)  # Corner mounting holes
    .faces(">Z")
    .workplane()
    .pushPoints([(-7, -12)])
    .hole(1.5)  # Extra small hole
)

# Left Part - L-Shaped/Cut Plate
# Create an L-shaped profile (square with bottom-right corner removed)
pts = [
    (-14, -14),
    (2, -14),
    (2, -2),
    (14, -2),
    (14, 14),
    (-14, 14)
]

left = (
    cq.Workplane("XY")
    .polyline(pts)
    .close()
    .extrude(t)
    .edges("|Z")
    .fillet(2)
    .faces(">Z")
    .workplane()
    # 3 corner holes
    .pushPoints([(-9, 9), (9, 9), (-9, -9)])
    .hole(2.5)
    .faces(">Z")
    .workplane()
    # Extra small hole
    .pushPoints([(3, 9)])
    .hole(1.5)
)

# Combine the three parts into a single result, translating them to visually match the image
result = (
    left.translate((-45, 0, 0))
    .union(middle)
    .union(right.translate((50, 0, 0)))
)