import cadquery as cq

# Parameters for dimensions
length_outer = 250.0  # Length of the outer rail (right side)
length_inner = 250.0  # Length of the inner rail (left side)
width_outer = 12.0    # Width of the outer rail
height_outer = 10.0   # Height of the outer rail
thickness = 1.5       # Wall thickness of the outer rail profile
block_len = 25.0      # Length of the central slider block
block_width = 16.0    # Width of the central block
block_height = 14.0   # Height of the central block

# 1. Create the Outer Rail (U-Channel Profile)
# Define points for a U-shaped cross-section
w_half = width_outer / 2.0
h_half = height_outer / 2.0
t = thickness

# Points traversing the U-profile counter-clockwise
pts = [
    (-w_half, h_half),
    (-w_half, -h_half),
    (w_half, -h_half),
    (w_half, h_half),
    (w_half - t, h_half),
    (w_half - t, -h_half + t),
    (-w_half + t, -h_half + t),
    (-w_half + t, h_half)
]

outer_rail = (
    cq.Workplane("YZ")
    .polyline(pts)
    .close()
    .extrude(length_outer)
)

# Add mounting holes at the far end of the outer rail
hole_dist_from_end = 8.0
hole_z_offset = -h_half + 3.0 # Position hole near the bottom flange
hole_cutter = (
    cq.Workplane("XZ")
    .moveTo(length_outer - hole_dist_from_end, hole_z_offset)
    .circle(1.2)
    .extrude(width_outer + 5.0, both=True)
)
outer_rail = outer_rail.cut(hole_cutter)

# 2. Create the Inner Rail (Rectangular Bar)
# Calculate inner dimensions with clearance
width_inner = width_outer - 2 * thickness - 1.0
height_inner = height_outer - thickness - 1.0

# Calculate vertical offset to align inner rail inside the U-channel floor
z_offset_inner = (-h_half + thickness) + height_inner / 2.0

inner_rail = (
    cq.Workplane("YZ")
    .rect(width_inner, height_inner)
    .extrude(-length_inner) # Extrude in negative X direction
    .translate((0, 0, z_offset_inner))
)

# Add a small end cap/feature to the inner rail
cap_len = 3.0
inner_cap = (
    cq.Workplane("YZ")
    .rect(width_inner + 1.0, height_inner + 1.0)
    .extrude(-cap_len)
    .translate((-length_inner, 0, z_offset_inner))
    .edges().fillet(0.5)
)
inner_rail = inner_rail.union(inner_cap)

# 3. Create the Central Slider Block
# Main body of the block
block = (
    cq.Workplane("YZ")
    .rect(block_width, block_height)
    .extrude(block_len)
    .translate((-block_len / 2.0, 0, 0)) # Center at origin X
)

# Add chamfers to the block for a styled look
block = block.edges("|X").chamfer(1.5)
block = block.edges("|Y").fillet(1.0)

# Add a central raised band on the block for detail
band_width = 8.0
block_band = (
    cq.Workplane("YZ")
    .rect(block_width + 1.0, block_height + 1.0)
    .extrude(band_width)
    .translate((-band_width / 2.0, 0, 0))
    .edges("|X").chamfer(1.0)
)
block = block.union(block_band)

# 4. Combine all parts into the final assembly
result = outer_rail.union(inner_rail).union(block)