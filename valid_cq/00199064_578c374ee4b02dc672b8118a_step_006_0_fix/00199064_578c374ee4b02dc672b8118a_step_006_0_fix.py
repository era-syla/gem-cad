import cadquery as cq

# Define the initial rectangle
rect = cq.Workplane("XY").rect(10, 5).extrude(1)

# Create a polar array of the rectangles
result = rect.translate((15, 0, 0)).union(
    rect.translate((11, 0, 0)).rotate((0, 0, 0), (0, 0, 1), 10)
).union(
    rect.translate((6, 0, 0)).rotate((0, 0, 0), (0, 0, 1), 20)
).union(
    rect.translate((0, 0, 0)).rotate((0, 0, 0), (0, 0, 1), 30)
)