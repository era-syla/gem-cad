import cadquery as cq

# --- Parametric Dimensions ---
# Overall dimensions
length = 100.0
width = 40.0
thickness = 15.0
corner_radius = 5.0

# Central channel dimensions (semi-circular/cylindrical cuts)
# The channel has three sections: large, small, large
large_channel_radius = 12.0
small_channel_radius = 8.0
small_channel_length = 30.0  # Length of the middle section

# Mounting holes
hole_diameter = 4.0
hole_inset_x = 8.0  # Distance from the long edge
hole_inset_y = 6.0  # Distance from the short edge
mid_hole_spacing = 0.0 # Center hole is at x=0

# --- Modeling Strategy ---
# 1. Create the base rectangular block.
# 2. Fillet the vertical corners.
# 3. Create the central channel cuts (three overlapping cylinders or a revolved profile).
#    Looking at the image, it's a semi-circular groove running along the length.
#    Since it's likely a clamp or housing half, the cut is from the top face down.
# 4. Create the counterbored/countersunk mounting holes. The image shows simple through holes or slight counterbores.
#    Let's assume simple through holes based on the view, possibly spot-faced.

# --- Build Geometry ---

# 1. Base Block
result = (
    cq.Workplane("XY")
    .box(length, width, thickness)
)

# 2. Fillet Corners
result = result.edges("|Z").fillet(corner_radius)

# 3. Central Channel Cuts
# The cut axis runs along the X-axis. The center of the cut is likely at Z = thickness/2 (top surface).
# We need to subtract material from the top face.

# Create the profile for the cut on the YZ plane (or cut cylinders along X)
# Method: Cut cylinders.
# Position: y=0, z = thickness/2 (top face)

# Large cylinder (runs full length technically, but we will intersect or just cut distinct sections)
# Actually, the image shows: Large -> Small -> Large.
# Let's cut the small one all the way through first (or just in the middle), then the large ones on ends.

# Define Z position for the center of the cut. 
# It looks like a half-cylinder cut into the top face.
cut_center_z = thickness / 2.0

# Middle section (Small channel)
result = result.cut(
    cq.Workplane("YZ")
    .workplane(offset=-small_channel_length/2.0) # Start of middle section
    .circle(small_channel_radius)
    .extrude(small_channel_length) # Extrude along X
    .translate((0, 0, cut_center_z)) # Move to top face
)

# End sections (Large channels)
# Left end cut
end_cut_length = (length - small_channel_length) / 2.0

# Since extrude goes in positive normal direction, we need to be careful with planes.
# Cut 1: From left end (-length/2) to start of middle section
result = result.cut(
    cq.Workplane("YZ")
    .workplane(offset=-length/2.0)
    .circle(large_channel_radius)
    .extrude(end_cut_length + 0.1) # Overlap slightly to ensure continuity
    .translate((0, 0, cut_center_z))
)

# Cut 2: From end of middle section to right end
result = result.cut(
    cq.Workplane("YZ")
    .workplane(offset=small_channel_length/2.0 - 0.1) # Overlap slightly
    .circle(large_channel_radius)
    .extrude(end_cut_length + 0.2)
    .translate((0, 0, cut_center_z))
)

# 4. Mounting Holes
# There are 6 holes total. 3 on each side.
# Positions relative to center (0,0):
# X coords: 0, +/- (length/2 - hole_inset_x)
# Y coords: +/- (width/2 - hole_inset_y)

x_pos = length/2.0 - hole_inset_x
y_pos = width/2.0 - hole_inset_y

pts = [
    (-x_pos, -y_pos), (0, -y_pos), (x_pos, -y_pos),
    (-x_pos, y_pos),  (0, y_pos),  (x_pos, y_pos)
]

result = (
    result.faces(">Z")
    .workplane()
    .pushPoints(pts)
    .hole(hole_diameter)
)

# Optional: Add small fillets to the channel transition edges if desired, 
# but the image looks sharp at the transition. The top edges of the channel, however, look slightly chamfered or just clean.
# Let's leave them sharp as standard machining would produce.

# Ensure the result is exported/visible if run in an environment
if "show_object" in locals():
    show_object(result)