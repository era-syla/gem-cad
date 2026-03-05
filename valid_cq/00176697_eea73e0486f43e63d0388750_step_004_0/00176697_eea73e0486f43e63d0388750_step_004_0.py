import cadquery as cq

# Parametric dimensions
length = 140.0
height = 35.0
plate_thickness = 5.0
block_protrusion = 30.0
center_block_width = 60.0
end_block_width = 30.0
wall_thickness = 4.0

# Create the backplate
# Orientation: Length along X, Height along Z, Thickness along Y
# This orients the part "standing up"
result = cq.Workplane("XY").box(length, plate_thickness, height)

# Add the center and end blocks
# Select the front face (>Y) to sketch the profiles
result = (
    result.faces(">Y").workplane()
    # 1. Center Block Profile
    .rect(center_block_width, height)
    # 2. Left Block Profile
    # Move workplane center to the left position
    .center(-length / 2 + end_block_width / 2, 0)
    .rect(end_block_width, height)
    # 3. Right Block Profile
    # Move relative to the previous center (Left -> Right)
    # Distance = (L/2 - W/2) - (-L/2 + W/2) = L - W
    .center(length - end_block_width, 0)
    .rect(end_block_width, height)
    # Extrude all profiles
    .extrude(block_protrusion)
)

# Cut the square holes in the end blocks
# Define hole size
hole_width = end_block_width - 2 * wall_thickness
hole_height = height - 2 * wall_thickness

# Select the new front faces (>Y)
# Use pushPoints to target the end block centers using absolute coordinates relative to the plane origin
result = (
    result.faces(">Y").workplane()
    .pushPoints([
        (-length / 2 + end_block_width / 2, 0),  # Left hole center
        (length / 2 - end_block_width / 2, 0)    # Right hole center
    ])
    .rect(hole_width, hole_height)
    .cutBlind(-block_protrusion)
)