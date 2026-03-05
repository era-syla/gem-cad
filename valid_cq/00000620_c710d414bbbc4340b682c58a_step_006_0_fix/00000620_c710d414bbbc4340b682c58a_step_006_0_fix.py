import cadquery as cq

# T-slot aluminum extrusion profile (20x20mm style)
# Length along Z axis

length = 160
size = 20
slot_width = 6
slot_depth = 4
slot_opening = 3.5
inner_size = 10
wall = 2.5

def make_tslot_profile():
    """Create a 20x20 T-slot extrusion cross-section as a 2D wire"""
    # Start with a 20x20 square
    profile = (
        cq.Workplane("XY")
        .rect(size, size)
    )
    return profile

# Build the main 20x20 square extrusion
result = (
    cq.Workplane("XY")
    .rect(size, size)
    .extrude(length)
)

# Cut the center hole
result = (
    result
    .faces(">Z")
    .workplane()
    .circle(4.3)
    .cutThruAll()
)

# Cut T-slots on all 4 sides
# Top slot (Y+)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, size/2 - slot_depth/2)
    .rect(slot_width, slot_depth)
    .cutThruAll()
)

# Bottom slot (Y-)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, -(size/2 - slot_depth/2))
    .rect(slot_width, slot_depth)
    .cutThruAll()
)

# Right slot (X+)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(size/2 - slot_depth/2, 0)
    .rect(slot_depth, slot_width)
    .cutThruAll()
)

# Left slot (X-)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(-(size/2 - slot_depth/2), 0)
    .rect(slot_depth, slot_width)
    .cutThruAll()
)

# Now cut the slot openings (narrow openings on each face)
# Top face opening
result = (
    result
    .faces(">Y")
    .workplane()
    .center(0, 0)
    .rect(slot_opening, length)
    .cutBlind(-slot_depth + 1)
)

# Bottom face opening
result = (
    result
    .faces("<Y")
    .workplane()
    .center(0, 0)
    .rect(slot_opening, length)
    .cutBlind(-slot_depth + 1)
)

# Right face opening
result = (
    result
    .faces(">X")
    .workplane()
    .center(0, 0)
    .rect(slot_opening, length)
    .cutBlind(-slot_depth + 1)
)

# Left face opening
result = (
    result
    .faces("<X")
    .workplane()
    .center(0, 0)
    .rect(slot_opening, length)
    .cutBlind(-slot_depth + 1)
)

# Cut the wider T-slot undercut on top/bottom/left/right
# Top T-slot undercut
result = (
    result
    .faces(">Y")
    .workplane()
    .center(0, 0)
    .rect(slot_width, length)
    .cutBlind(-(slot_depth - 1))
)

# Bottom T-slot undercut
result = (
    result
    .faces("<Y")
    .workplane()
    .center(0, 0)
    .rect(slot_width, length)
    .cutBlind(-(slot_depth - 1))
)

# Right T-slot undercut
result = (
    result
    .faces(">X")
    .workplane()
    .center(0, 0)
    .rect(slot_width, length)
    .cutBlind(-(slot_depth - 1))
)

# Left T-slot undercut
result = (
    result
    .faces("<X")
    .workplane()
    .center(0, 0)
    .rect(slot_width, length)
    .cutBlind(-(slot_depth - 1))
)