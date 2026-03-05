import cadquery as cq

# Parameters
L = 200    # Length of the bar
W = 10     # Width of the bar
H = 8      # Height of the bar
toothH = 3 # Height of each triangular tooth
count = 8  # Number of teeth
pegR = 5   # Radius of the cylindrical peg
pegL = 10  # Length of the cylindrical peg

# Create the main rectangular bar (from x=0 to x=L)
result = cq.Workplane("XY").box(L, W, H, centered=(False, True, False))

# Add the cylindrical peg at the right end (centered in Y, halfway up in Z)
peg = cq.Workplane("YZ", origin=(L, 0, H/2)).circle(pegR).extrude(pegL)
result = result.union(peg)

# Add triangular teeth on the top face
spacing = L / count
for i in range(count):
    x0 = i * spacing
    tooth = (
        cq.Workplane("XZ", origin=(0, -W/2, H))
        .polyline([
            (x0, 0),
            (x0 + spacing/2, toothH),
            (x0 + spacing, 0),
            (x0, 0),
        ])
        .close()
        .extrude(W, combine=False)
    )
    result = result.union(tooth)