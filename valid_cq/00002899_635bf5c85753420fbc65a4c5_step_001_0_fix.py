import cadquery as cq

# Main flat plate (key bow - the rounded square end)
plate = (
    cq.Workplane("XY")
    .moveTo(20, 0)
    .rect(40, 30, centered=True)
    .extrude(3)
)

# Round the corners of the plate
plate = plate.edges("|Z").fillet(5)

# Hole in the plate (rounded rectangle cutout)
plate = (
    plate
    .faces(">Z")
    .workplane()
    .moveTo(20, 0)
    .rect(14, 10, centered=True)
    .cutBlind(-3)
)

# Add small notch/tab on the hole (key bit shape)
plate = (
    plate
    .faces(">Z")
    .workplane()
    .moveTo(24, 0)
    .rect(6, 4, centered=True)
    .cutBlind(-3)
)

# Neck/shank connecting plate to the head
shank = (
    cq.Workplane("XY")
    .moveTo(-10, 0)
    .rect(30, 10, centered=True)
    .extrude(3)
)

# Raised ridge on the shank
ridge = (
    cq.Workplane("XY")
    .moveTo(-10, 0)
    .rect(28, 6, centered=True)
    .extrude(6)
)

# Head/bow part - vertical wall at the end
head_base = (
    cq.Workplane("XY")
    .moveTo(-28, 0)
    .rect(8, 16, centered=True)
    .extrude(3)
)

# Vertical wall of the head
head_wall = (
    cq.Workplane("XY")
    .moveTo(-30, 0)
    .rect(4, 16, centered=True)
    .extrude(16)
)

# Top cap of the head
head_top = (
    cq.Workplane("XY")
    .transformed(offset=cq.Vector(-30, 0, 13))
    .rect(8, 16, centered=True)
    .extrude(3)
)

# Combine all parts
result = (
    plate
    .union(shank)
    .union(ridge)
    .union(head_base)
    .union(head_wall)
    .union(head_top)
)

# Fillet some edges to smooth
result = result.edges("|Z").fillet(1)