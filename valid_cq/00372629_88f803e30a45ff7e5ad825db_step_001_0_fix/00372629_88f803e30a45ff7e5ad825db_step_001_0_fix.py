import cadquery as cq

result = (
    cq.Workplane("XY")
    .rect(50, 100)  # Create a base rectangle
    .extrude(5)     # Extrude it to create a flat plate
    .faces(">Z").workplane()  # Select the top face and create a new workplane
    .transformed(offset=(0, 0, 5), rotate=(0, 90, 0))  # Offset and rotate to create a bend
    .rect(50, 10)   # Create a small top rectangle for bending
    .cutThruAll()   # Remove material to form the bend
    .edges("|Z")    # Select edges for filleting
    .fillet(2)      # Apply fillet to soften edges
)