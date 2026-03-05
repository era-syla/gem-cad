import cadquery as cq

# Define the main plate
result = (
    cq.Workplane("XY")
    .box(100, 50, 2)  # Main plate size
    .faces(">Z")
    .workplane()
    .rect(10, 10, forConstruction=True)
    .vertices()
    .hole(8)  # Small square holes
    .rect(70, 20, forConstruction=True)
    .center(0, 0)
    .rarray(20, 0, 3, 1)
    .hole(10)  # Large oval hole
)