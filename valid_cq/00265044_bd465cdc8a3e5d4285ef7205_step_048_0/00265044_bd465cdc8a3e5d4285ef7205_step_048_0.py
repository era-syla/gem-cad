import cadquery as cq

# Dimensions
length = 60.0
width = 20.0
height = 10.0

# Feature Dimensions
# Female part slot (stadium shape)
slot_length = 14.0  # Long dimension (transverse)
slot_width = 6.0    # Short dimension (longitudinal)
slot_depth = 2.0
slot_fillet = slot_width / 2.0 - 0.001

# Inner hole (rectangular)
hole_length = 8.0   # Matches tenon width
hole_width = 4.0    # Matches tenon thickness

# Male part tenon
tenon_len = 8.0
tenon_w = hole_length
tenon_t = hole_width

# Shoulder notches
notch_radius = 1.5
notch_offset_y = 6.5 # Distance from center line to notch center

# --- Build Female Part (Left) ---
# Create base block centered at origin
female = cq.Workplane("XY").box(length, width, height)

# Cut the stadium-shaped pocket on the top face
female = (
    female.faces(">Z")
    .workplane()
    .sketch()
    .rect(slot_width, slot_length)
    .vertices()
    .fillet(slot_fillet)
    .finalize()
    .cutBlind(-slot_depth)
)

# Cut the through-hole for the tenon inside the pocket
female = (
    female.faces(">Z")
    .workplane()
    .sketch()
    .rect(hole_width, hole_length)
    .finalize()
    .cutThruAll()
)

# --- Build Male Part (Right) ---
# Create base block
male_base = cq.Workplane("XY").box(length, width, height)

# Add Tenon to the +X face
# On the >X workplane, local X is global Y (Width), local Y is global Z (Height)
male = (
    male_base.faces(">X")
    .workplane()
    .rect(tenon_w, tenon_t)
    .extrude(tenon_len)
)

# Add the semi-circular notches to the shoulders
# These are vertical cuts on the corners of the face where the tenon starts
male = (
    male.faces(">Z")
    .workplane()
    .moveTo(length / 2.0, notch_offset_y)
    .circle(notch_radius)
    .moveTo(length / 2.0, -notch_offset_y)
    .circle(notch_radius)
    .cutThruAll()
)

# --- Assembly / Layout ---
# Position parts to match the image (Female left, Male right facing each other)
displacement = length / 2.0 + 10.0

# Move Female part to the left
part1 = female.translate((-displacement, 0, 0))

# Rotate Male part 180 degrees so tenon points left, and move to the right
part2 = male.rotate((0, 0, 0), (0, 0, 1), 180).translate((displacement, 0, 0))

# Combine into a single result object
result = part1.union(part2)