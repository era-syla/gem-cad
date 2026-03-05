import cadquery as cq

# Define base profile
points = [
    (-50, -15), (-50, 15),
    (-25, 15), (-25, 7.5),
    (25, 7.5), (25, 15),
    (50, 15), (50, -15),
    (25, -15), (25, -7.5),
    (-25, -7.5), (-25, -15)
]

# Build the model
result = (
    cq.Workplane("XY")
    .polyline(points).close().extrude(8)                    # Base extrusion
    .faces(">Z").workplane().rect(60, 20).extrude(4)       # Raised central pad
    .faces(">Z").workplane().text("B", 14, 2, combine=True)  # Letter B
    # Holes through the central pad and base
    .faces(">Z").workplane().pushPoints([(-20, 0), (20, 0)]).hole(8)
    # Side flange small holes
    .faces("<X").workplane().center(0, 7.5).hole(5)
    .faces(">X").workplane().center(0, 7.5).hole(5)
)
