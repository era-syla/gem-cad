import cadquery as cq

# Create a cylindrical puck with two slots cut into the top
# The slots appear to go from near center to the edge, arranged like a screwdriver slot (cross or single)

# Main cylinder
radius = 50
height = 15

# Create base cylinder
base = cq.Workplane("XY").cylinder(height, radius)

# Cut a slot across the top - looks like a single slot (screwdriver head)
# The slot appears to go diagonally across the top surface
slot_width = 3
slot_depth = 4
slot_length = radius * 1.8  # slightly longer than diameter to ensure it cuts through

# First slot - appears to go from upper-left to lower-right area
slot1 = (
    cq.Workplane("XY")
    .workplane(offset=height / 2)
    .center(0, 0)
    .rect(slot_length, slot_width)
    .extrude(slot_depth)
)

# Looking at the image more carefully, there appear to be two slots that don't 
# fully cross - one longer slot and one shorter slot creating an asymmetric pattern
# Let's do two slots at roughly 90 degrees but offset

# Slot 1: longer slot going roughly from left to right (slightly angled)
result = (
    cq.Workplane("XY")
    .cylinder(height, radius)
)

# Cut slot 1 - horizontal-ish slot
cut1 = (
    cq.Workplane("XY")
    .workplane(offset=height / 2 - slot_depth)
    .transformed(rotate=cq.Vector(0, 0, -20))
    .rect(slot_length, slot_width)
    .extrude(slot_depth + 1)
)

result = result.cut(cut1)

# Cut slot 2 - perpendicular slot (shorter, going to edge on right side)
slot_length2 = radius * 1.2
cut2 = (
    cq.Workplane("XY")
    .workplane(offset=height / 2 - slot_depth)
    .transformed(rotate=cq.Vector(0, 0, 70))
    .center(radius * 0.3, 0)
    .rect(slot_length2, slot_width)
    .extrude(slot_depth + 1)
)

result = result.cut(cut2)