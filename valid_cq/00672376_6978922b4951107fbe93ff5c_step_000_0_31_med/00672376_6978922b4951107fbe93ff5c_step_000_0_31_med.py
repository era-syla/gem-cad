import cadquery as cq

# Dimensional parameters
radius_outer = 60.0
radius_inner = 55.0
thickness = 5.0
strut_width = 3.0

# 1. Create the outer bounding ring
ring = (
    cq.Workplane("XY")
    .circle(radius_outer)
    .circle(radius_inner)
    .extrude(thickness)
)

# 2. Create the structural cross struts supporting the center geometry
struts = (
    cq.Workplane("XY")
    .rect(radius_inner * 2, strut_width)
    .extrude(thickness)
    .union(
        cq.Workplane("XY")
        .rect(strut_width, radius_inner * 2)
        .extrude(thickness)
    )
)

# 3. Define the stylized leaping fish geometry
# Outer boundary spline points
fish_pts = [
    (-40, 20),   # Upper tail
    (-20, 10),   # Tail base
    (-10, 30),   # Rear dorsal
    (10, 35),    # Front dorsal
    (30, 20),    # Head top
    (40, 0),     # Snout
    (35, -20),   # Lower jaw
    (20, -30),   # Front belly
    (0, -20),    # Mid belly
    (-20, -30),  # Rear belly
    (-30, -10),  # Lower tail base
    (-45, -20),  # Lower tail
    (-40, 0)     # Tail notch
]

# Generate the main fish solid body
fish_body = (
    cq.Workplane("XY")
    .spline(fish_pts)
    .close()
    .extrude(thickness)
)

# 4. Detail cuts for the fish shape
# Crescent cut to shape the leaping inner curve
belly_cut = (
    cq.Workplane("XY")
    .center(-5, 5)
    .circle(18)
    .extrude(thickness)
)

# Eye cut out
eye_cut = (
    cq.Workplane("XY")
    .center(28, 5)
    .circle(2.5)
    .extrude(thickness)
)

# Lower fin separation cut
fin_cut = (
    cq.Workplane("XY")
    .center(10, -25)
    .circle(7)
    .extrude(thickness)
)

# Apply cuts to the fish body
fish_final = fish_body.cut(belly_cut).cut(eye_cut).cut(fin_cut)

# 5. Combine all elements into the final result
result = ring.union(struts).union(fish_final)

# Clean up any extraneous internal edges
result = result.clean()