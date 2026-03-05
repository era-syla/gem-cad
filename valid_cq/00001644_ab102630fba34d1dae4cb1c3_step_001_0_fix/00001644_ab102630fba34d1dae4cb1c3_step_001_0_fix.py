import cadquery as cq

# Parameters
frame_length = 150
frame_gap = 20
half_len = (frame_length - frame_gap) / 2
frame_height = 60
frame_thickness = 10
block_thickness = 15
hole_diameter = 6
n_holes = 6

# Frame 1
frame1 = (
    cq.Workplane("XY")
    .box(half_len, frame_thickness, frame_height)
    # cut inner window
    .faces(">Y").workplane(centerOption="CenterOfMass")
    .rect(half_len - 10, frame_height - 10).cutThruAll()
    # holes along the length
    .faces(">Y").workplane(centerOption="CenterOfMass")
    .pushPoints(
        [
            (-half_len + 10 + i * ((2 * (half_len - 10)) / (n_holes - 1)), 0)
            for i in range(n_holes)
        ]
    )
    .hole(hole_diameter)
    .translate((- (half_len + frame_gap / 2), 0, frame_height / 2))
)

# Frame 2 (mirror of Frame 1)
frame2 = (
    cq.Workplane("XY")
    .box(half_len, frame_thickness, frame_height)
    .faces(">Y").workplane(centerOption="CenterOfMass")
    .rect(half_len - 10, frame_height - 10).cutThruAll()
    .faces(">Y").workplane(centerOption="CenterOfMass")
    .pushPoints(
        [
            (-half_len + 10 + i * ((2 * (half_len - 10)) / (n_holes - 1)), 0)
            for i in range(n_holes)
        ]
    )
    .hole(hole_diameter)
    .translate((half_len + frame_gap / 2, 0, frame_height / 2))
)

# Central sliding block
block = (
    cq.Workplane("XY")
    .box(frame_gap, block_thickness, frame_height)
    .translate((0, 0, frame_height / 2))
    # screw hole through block
    .faces(">Y").workplane(centerOption="CenterOfMass")
    .hole(hole_diameter + 2)
)

# Combine all parts
result = frame1.union(frame2).union(block)