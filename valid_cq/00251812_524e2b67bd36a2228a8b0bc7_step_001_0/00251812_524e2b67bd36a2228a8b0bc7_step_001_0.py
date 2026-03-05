import cadquery as cq

# --- Parametric Dimensions ---

# Left Part (Double Clip)
p1_od = 14.0         # Outer diameter of the rings
p1_id = 10.0         # Inner diameter of the rings
p1_height = 5.0      # Thickness of the part
p1_spacing = 13.0    # Distance between ring centers
p1_gap = 8.0         # Opening size of the C-clip section

# Right Part (Stepped Retaining Ring)
p2_od = 18.0         # Outer diameter
p2_id_small = 10.0   # Inner diameter (bottom)
p2_id_large = 14.0   # Inner diameter (top/counterbore)
p2_height = 6.0      # Total thickness
p2_step_depth = 3.0  # Depth of the counterbore
p2_gap = 10.0        # Opening width

# --- Modeling Left Part ---

# Create the closed ring (left side)
ring_closed = (
    cq.Workplane("XY")
    .circle(p1_od / 2.0)
    .circle(p1_id / 2.0)
    .extrude(p1_height)
)

# Create the open ring (right side), initially closed
ring_open_base = (
    cq.Workplane("XY")
    .center(p1_spacing, 0)
    .circle(p1_od / 2.0)
    .circle(p1_id / 2.0)
    .extrude(p1_height)
)

# Cut the opening in the second ring
# We position a box to cut the right side of the ring
cutter_p1 = (
    cq.Workplane("XY")
    .center(p1_spacing + p1_od/2.0, 0)
    .box(p1_od, p1_gap, p1_height * 2.0)
)

ring_open = ring_open_base.cut(cutter_p1)

# Combine into the left part
part1 = ring_closed.union(ring_open)

# --- Modeling Right Part ---

# Create the base cylinder with the smaller ID
part2_base = (
    cq.Workplane("XY")
    .circle(p2_od / 2.0)
    .circle(p2_id_small / 2.0)
    .extrude(p2_height)
)

# Create the counterbore (step) from the top face
part2_stepped = (
    part2_base.faces(">Z")
    .workplane()
    .circle(p2_id_large / 2.0)
    .cutBlind(-p2_step_depth)
)

# Cut the opening slot
# We position a box to cut the left side of the cylinder (relative to its center)
cutter_p2 = (
    cq.Workplane("XY")
    .center(-p2_od / 2.0, 0)
    .box(p2_od, p2_gap, p2_height * 2.0)
)

part2_final = part2_stepped.cut(cutter_p2)

# --- Assembly / Positioning ---

# Position Part 2 to match the image layout (to the right and back, rotated)
part2_positioned = (
    part2_final
    .rotate((0, 0, 0), (0, 0, 1), -45) # Rotate so opening faces towards Part 1
    .translate((40, 25, 0))            # Move away from Part 1
)

# Combine both parts into the final result
result = part1.union(part2_positioned)