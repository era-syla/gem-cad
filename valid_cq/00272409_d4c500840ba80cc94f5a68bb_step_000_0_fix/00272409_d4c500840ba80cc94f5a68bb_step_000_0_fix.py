import cadquery as cq

# Define 2D outline of the bird silhouette
points = [
    (0, 0),
    (80, 0),
    (100, 20),
    (90, 35),
    (70, 60),
    (75, 90),
    (45, 95),
    (20, 60),
    (5, 50),
    (0, 20),
]

# Build and extrude the shape
result = (
    cq.Workplane("XY")
    .polyline(points)
    .close()
    .extrude(10)
    .edges("|Z")       # fillet all vertical edges
    .fillet(2)
)