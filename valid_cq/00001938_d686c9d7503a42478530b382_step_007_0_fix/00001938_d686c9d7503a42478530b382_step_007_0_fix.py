import cadquery as cq

# Parameters
length = 100.0
width = 30.0
thickness = 5.0
pocket_length = 30.0
pocket_width = 10.0
pocket_depth = 4.0
pocket_spacing = 20.0
lug_length = 10.0
prong_width = 3.0
prong_gap = 4.0
hole_dia = 2.0
text_height_main = 3.0
text_thickness = 1.0
text_height_inner = 4.0

# Compute positions
pocket_positions = [
    -(pocket_length/2 + pocket_spacing/2),
    +(pocket_length/2 + pocket_spacing/2)
]
prong_y_positions = [
    +(prong_gap/2 + prong_width/2),
    -(prong_gap/2 + prong_width/2)
]
lug_positions = [
    -(length/2 + lug_length/2),
    +(length/2 + lug_length/2)
]

# Base plate
result = cq.Workplane("XY").box(length, width, thickness)

# Cut two rectangular pockets
for x in pocket_positions:
    result = (
        result
        .faces(">Z")
        .workplane()
        .center(x, 0)
        .rect(pocket_length, pocket_width)
        .cutBlind(-pocket_depth)
    )

# Add inner text in each pocket
for x, label in zip(pocket_positions, ["GΦ", "SHΦ"]):
    result = (
        result
        .faces(">Z")
        .workplane()
        .center(x, 0)
        .text(label, text_height_inner, text_thickness)
    )

# Add side text on the long side
result = (
    result
    .faces(">Y")
    .workplane()
    .transformed(rotate=(0, 90, 0))
    .center(0, 0)
    .text("HOOD TO GRL VOW", text_height_main, text_thickness)
)

# Build end prongs with holes
for x in lug_positions:
    for y in prong_y_positions:
        prong = (
            cq.Workplane("XY")
            .transformed(offset=(x, y, 0))
            .box(lug_length, prong_width, thickness)
        )
        prong = (
            prong
            .faces(">Z")
            .workplane()
            .center(0, 0)
            .hole(hole_dia)
        )
        result = result.union(prong)

# Add "50" text on top of each end
for x in lug_positions:
    result = (
        result
        .faces(">Z")
        .workplane()
        .center(x, 0)
        .text("50", text_height_main, text_thickness)
    )