import cadquery as cq

def make_clamp_half(width, height, depth, pipe_radius, has_square_hole=True):
    """Create a single clamp half piece"""
    
    # Main body block
    body = (
        cq.Workplane("XY")
        .box(width, depth, height)
    )
    
    # Semicircular pipe channel - cut from front face
    body = (
        body
        .faces(">Y")
        .workplane()
        .center(0, 0)
        .circle(pipe_radius)
        .cutBlind(-depth * 0.6)
    )
    
    # Add top block/cap
    top_cap = (
        cq.Workplane("XY")
        .box(width, depth * 0.7, height * 0.2)
        .translate((0, 0, height * 0.5 + height * 0.1))
    )
    
    body = body.union(top_cap)
    
    # Square hole in top cap for bolt
    if has_square_hole:
        sq_size = width * 0.25
        body = (
            body
            .faces(">Z")
            .workplane()
            .center(0, 0)
            .rect(sq_size, sq_size)
            .cutBlind(-height * 0.25)
        )
    
    # Side bolt holes
    body = (
        body
        .faces(">X")
        .workplane()
        .center(0, height * 0.1)
        .circle(width * 0.08)
        .cutThruAll()
    )
    
    return body


def make_full_clamp(pipe_radius, width=18, height=35, depth=20):
    """Create a full pipe clamp (two halves)"""
    
    half1 = make_clamp_half(width, height, depth, pipe_radius)
    
    # Second half is mirrored
    half2 = make_clamp_half(width, height, depth, pipe_radius)
    half2 = half2.mirror("YZ")
    
    # Position halves together
    h1 = half1.translate((width * 0.5, 0, 0))
    h2 = half2.translate((-width * 0.5, 0, 0))
    
    return h1.union(h2)


# Create two pipe clamps of different sizes
# Large clamp
large_clamp_half = (
    cq.Workplane("XY")
    .box(20, 22, 38)
)

# Semicircular channel on front
large_clamp_half = (
    large_clamp_half
    .faces(">Y")
    .workplane()
    .circle(8)
    .cutBlind(-14)
)

# Top protrusion
large_top = (
    cq.Workplane("XY")
    .box(20, 16, 8)
    .translate((0, -3, 23))
)
large_clamp_half = large_clamp_half.union(large_top)

# Square recess on top
large_clamp_half = (
    large_clamp_half
    .faces(">Z")
    .workplane()
    .rect(7, 7)
    .cutBlind(-5)
)

# Side hole
large_clamp_half = (
    large_clamp_half
    .faces(">X")
    .workplane()
    .center(0, 5)
    .circle(2.5)
    .cutThruAll()
)

# Mirror for second half
large_half2 = large_clamp_half.mirror("YZ")

# Combine large clamp
large_clamp = large_clamp_half.translate((10, 0, 0)).union(large_half2.translate((-10, 0, 0)))

# Small clamp
small_clamp_half = (
    cq.Workplane("XY")
    .box(15, 18, 30)
)

small_clamp_half = (
    small_clamp_half
    .faces(">Y")
    .workplane()
    .circle(6)
    .cutBlind(-11)
)

small_top = (
    cq.Workplane("XY")
    .box(15, 13, 6)
    .translate((0, -2.5, 18))
)
small_clamp_half = small_clamp_half.union(small_top)

small_clamp_half = (
    small_clamp_half
    .faces(">Z")
    .workplane()
    .rect(5, 5)
    .cutBlind(-4)
)

small_clamp_half = (
    small_clamp_half
    .faces(">X")
    .workplane()
    .center(0, 3)
    .circle(2.0)
    .cutThruAll()
)

small_half2 = small_clamp_half.mirror("YZ")

small_clamp = small_clamp_half.translate((7.5, 0, 0)).union(small_half2.translate((-7.5, 0, 0)))

# Position both clamps side by side
large_positioned = large_clamp.translate((-22, 0, 0))
small_positioned = small_clamp.translate((18, 0, -4))

result = large_positioned.union(small_positioned)