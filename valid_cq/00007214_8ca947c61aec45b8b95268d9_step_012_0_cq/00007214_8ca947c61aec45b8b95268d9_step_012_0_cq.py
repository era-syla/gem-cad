import cadquery as cq

# --- Parameters ---
# Dimensions estimated from the visual proportions
base_width = 40.0      # Total width of the U-shaped base
base_length = 50.0     # Length of the parallel legs
leg_width = 8.0        # Width of each individual leg
base_thickness = 5.0   # Thickness of the base plate
bridge_width = 10.0    # Width of the connecting piece at the back of the legs (if different, looks like just part of the U)

top_length = 35.0      # Length of the top rectangular block
top_width = 40.0       # Width of the top rectangular block (matches base width)
top_height = 25.0      # Total height from the bottom of the base to the top surface
wall_thickness = 4.0   # Thickness of the vertical walls and top face

# --- Modeling ---

# 1. Create the U-shaped Base
# We'll sketch on the XY plane.
# The shape is essentially a rectangle with a rectangular cutout in the middle.
cutout_width = base_width - 2 * leg_width
cutout_length = base_length - leg_width # Assuming the back connection is also `leg_width` thick

base = (
    cq.Workplane("XY")
    .rect(base_width, base_length)
    .extrude(base_thickness)
)

# Create the cutout to form the U-shape
# We center the cutout relative to the front
cutout = (
    cq.Workplane("XY")
    .center(0, leg_width/2) # Shift forward so the back bar remains
    .rect(cutout_width, cutout_length)
    .extrude(base_thickness)
)

base_u_shape = base.cut(cutout)

# 2. Create the Top Structure (Inverted U profile)
# This sits on top of the base. It looks like a table or bridge.
# It has two vertical walls and a top plate.

# Let's sketch the side profile of this top part on the YZ plane (or XZ depending on orientation)
# Looking at the image, the U-base legs point towards +Y (or -Y). Let's assume legs are along Y.
# The top part bridges across the X-axis width.

# We'll construct it as a solid block first, then shell or cut underneath.
# Position: centered in X, aligned with the back of the base in Y.
# The back of the base is at y = -base_length/2.
# The top structure seems to start at the back edge.

top_block_z_start = base_thickness
top_structure = (
    cq.Workplane("XY")
    .workplane(offset=top_block_z_start)
    .center(0, -base_length/2 + top_length/2) # Align with the back edge
    .rect(top_width, top_length)
    .extrude(top_height - base_thickness)
)

# Now we need to hollow out the "tunnel" underneath the top block.
# The tunnel runs along the Y axis.
tunnel_width = top_width - 2 * wall_thickness
tunnel_height = (top_height - base_thickness) - wall_thickness # Leave wall_thickness at the top

tunnel_cut = (
    cq.Workplane("XY")
    .workplane(offset=top_block_z_start)
    .center(0, -base_length/2 + top_length/2)
    .rect(tunnel_width, top_length)
    .extrude(tunnel_height)
)

top_hollow = top_structure.cut(tunnel_cut)

# 3. Combine parts
# The image shows the top structure integrated with the base.
# However, there are small "feet" or tabs at the end of the legs.
# Looking closely at the image:
# The ends of the legs have small raised sections or steps.
# Let's add those details.

tip_length = 5.0
tip_height_offset = 2.0 # How much higher than the base

# Left leg tip
tip1 = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .center(-base_width/2 + leg_width/2, base_length/2 - tip_length/2)
    .rect(leg_width, tip_length)
    .extrude(tip_height_offset)
)

# Right leg tip
tip2 = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .center(base_width/2 - leg_width/2, base_length/2 - tip_length/2)
    .rect(leg_width, tip_length)
    .extrude(tip_height_offset)
)

# Combine everything
result = base_u_shape.union(top_hollow).union(tip1).union(tip2)

# Export or display
# cq.exporters.export(result, "model.step")