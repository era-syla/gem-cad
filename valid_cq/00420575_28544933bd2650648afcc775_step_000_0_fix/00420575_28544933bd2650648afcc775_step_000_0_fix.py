import cadquery as cq

# Parameters
beam_length = 100
beam_depth = 20
beam_thick = 10
support_height = 30
support_length = 10
n_grooves = 5
groove_radius = beam_thick
groove_spacing = beam_length / (n_grooves + 1)

# Build the horizontal beam
beam = cq.Workplane("XY").box(beam_length, beam_depth, beam_thick)

# Build the vertical support at the left end
support = (
    cq.Workplane("XY")
    .transformed(
        offset=(
            -beam_length/2 + support_length/2,
            0,
            -beam_thick/2 - (support_height - beam_thick)/2,
        )
    )
    .box(support_length, beam_depth, support_height)
)

# Combine beam and support
part = beam.union(support)

# Generate and subtract the half‐cylinder grooves
grooves = None
for i in range(n_grooves):
    x_i = -beam_length/2 + groove_spacing * (i + 1)
    cyl = (
        cq.Workplane("XZ", origin=(x_i, 0, beam_thick / 2))
        .circle(groove_radius)
        .extrude(beam_depth * 1.2, both=True)
    )
    grooves = cyl if grooves is None else grooves.union(cyl)

result = part.cut(grooves)