import cadquery as cq

# Main dimensions
width = 40
depth = 30
clamp_height = 15
pipe_radius = 8
hole_radius = 3
hole_offset_x = 14
hole_offset_y = 8

def make_clamp_half(pipe_r, w, d, h):
    """Make one clamp half with a semicircular cutout"""
    # Base block
    block = (
        cq.Workplane("XY")
        .box(w, d, h)
    )
    
    # Cut semicircle from front face (the pipe channel)
    # The cutout goes through the depth
    block = (
        block
        .faces(">Y")
        .workplane()
        .center(0, 0)
        .circle(pipe_r)
        .cutBlind(-d)
    )
    
    return block

# Create top clamp half (upper portion)
top_half = (
    cq.Workplane("XY")
    .box(width, depth, clamp_height)
    .faces(">Y")
    .workplane()
    .center(0, 0)
    .circle(pipe_radius)
    .cutBlind(-depth)
    .faces(">Z")
    .workplane()
    .pushPoints([(hole_offset_x, hole_offset_y), (-hole_offset_x, hole_offset_y)])
    .circle(hole_radius)
    .cutBlind(-clamp_height)
)

# Apply fillets to top half edges
top_half = (
    top_half
    .edges("|Z")
    .fillet(3)
)

# Create bottom clamp half (lower portion) - mirror of top
bottom_half = (
    cq.Workplane("XY")
    .box(width, depth, clamp_height)
    .faces(">Y")
    .workplane()
    .center(0, 0)
    .circle(pipe_radius)
    .cutBlind(-depth)
    .faces(">Z")
    .workplane()
    .pushPoints([(hole_offset_x, -hole_offset_y), (-hole_offset_x, -hole_offset_y)])
    .circle(hole_radius)
    .cutBlind(-clamp_height)
)

# Apply fillets to bottom half
bottom_half = (
    bottom_half
    .edges("|Z")
    .fillet(3)
)

# Move top half up and bottom half down to create gap
top_solid = top_half.val().moved(cq.Location(cq.Vector(0, 0, clamp_height/2 + 2)))
bottom_solid = bottom_half.val().moved(cq.Location(cq.Vector(0, 0, -clamp_height/2 - 2)))

# Create middle flange/separator plate
mid_flange = (
    cq.Workplane("XY")
    .box(width - 4, depth - 2, 4)
)
mid_flange_solid = mid_flange.val()

# Create base/foot at bottom
base = (
    cq.Workplane("XY")
    .box(width - 8, depth - 4, 6)
)
base_z = -clamp_height - 2 - 3
base_solid = base.val().moved(cq.Location(cq.Vector(0, 0, base_z)))

# Combine all parts
combined = (
    cq.Workplane("XY")
    .add(top_solid)
    .add(bottom_solid)
    .add(mid_flange_solid)
    .add(base_solid)
)

# Union everything together
result_shape = top_solid.fuse(bottom_solid).fuse(mid_flange_solid).fuse(base_solid)

result = cq.Workplane("XY").add(result_shape)