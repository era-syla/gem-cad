import cadquery as cq

# -- Parametric Dimensions --
length = 80.0
width = 40.0
thickness = 15.0
fillet_radius = 5.0

# Clamping/split hole section
large_hole_diam = 15.0
large_hole_center_dist_from_edge = 20.0  # Center from the left edge
slit_width = 3.0
side_hole_diam = 6.0 # Horizontal hole for screw

# Locking tabs/small hole section
tab_width = 10.0
tab_length = 8.0
tab_height = 8.0
tab_spacing_from_center = 12.0 # Offset from centerline to inside edge of tab
small_hole_diam = 8.0
small_hole_center_dist_from_right = 15.0

# -- Construction --

# 1. Base Block
# Create the main rectangular body centered on XY plane for easier symmetry
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
)

# 2. Add Fillets to the four vertical corners
result = result.edges("|Z").fillet(fillet_radius)

# 3. Create the Split Clamp Feature (Left side)
# 3a. Large vertical hole
result = (
    result
    .faces(">Z")
    .workplane()
    .center(-length/2 + large_hole_center_dist_from_edge, 0)
    .hole(large_hole_diam)
)

# 3b. The slit connecting the hole to the edge
# We cut a slot from the edge to the hole center
result = (
    result
    .faces(">Z")
    .workplane()
    .center(-length/2 + large_hole_center_dist_from_edge/2, 0)
    .rect(large_hole_center_dist_from_edge, slit_width)
    .cutThruAll()
)

# 3c. Side hole for tightening screw
# This goes through the side of the block, intersecting the split
result = (
    result
    .faces("<X")
    .workplane()
    .center(0, 0) # Center on the face
    .hole(side_hole_diam)
)

# 4. Create the Locking Tabs (Right side)
# We add material on top of the block
# We need two tabs symmetric about the X-axis
# Calculating center positions for the tabs based on spacing

# Tab center Y position
tab_center_y = tab_spacing_from_center + (tab_length / 2.0)
# Tab center X position (aligned with small hole roughly, let's place them relative to right edge)
# Looking at image, tabs seem aligned with the small hole center area
tab_center_x_from_right = small_hole_center_dist_from_right + 5.0 # Slightly offset inwards or centered
# Let's align them with the small hole X position for simplicity, or slightly further back. 
# Visually, they flank the small hole but are slightly further 'left' (negative X) in the image orientation.
# Let's position them at x = length/2 - 25
tab_pos_x = length/2 - 25.0

result = (
    result
    .faces(">Z")
    .workplane()
    .pushPoints([
        (tab_pos_x, tab_center_y),
        (tab_pos_x, -tab_center_y)
    ])
    .rect(tab_width, tab_length)
    .extrude(tab_height)
)

# 5. Small Hole (Right side)
result = (
    result
    .faces(">Z")
    .workplane()
    .center(length/2 - small_hole_center_dist_from_right, 0)
    .hole(small_hole_diam)
)