import cadquery as cq

# Parameters
post_d = 20
post_h = 40
beam_w = 10
beam_h = 10
span = 150
hole_r = beam_h/2 + 1

# Left and right support posts
left = cq.Workplane("XY").circle(post_d/2).extrude(post_h)
right = cq.Workplane("XY").transformed(offset=(span, 0, 0)).circle(post_d/2).extrude(post_h)

# Curved beam path (in XY plane)
path2d = cq.Workplane("XY").polyline([
    (0, post_d/2),
    (span/2, -post_d/2),
    (span, post_d/2)
]).wire()

# Beam profile at start of path, oriented in YZ plane
beam_profile = cq.Workplane("YZ", origin=(0, post_d/2, post_h)).rect(beam_w, beam_h)

# Sweep profile along the path
beam = beam_profile.sweep(path2d)

# Create hole cylinders and union them
hole_positions = [span * 0.25, span * 0.5, span * 0.75]
holes = None
for x in hole_positions:
    h = cq.Workplane("XZ", origin=(x, 0, post_h)).circle(hole_r).extrude(beam_w+2, both=True)
    holes = h if holes is None else holes.union(h)

# Combine all and cut holes
result = left.union(right).union(beam).cut(holes)