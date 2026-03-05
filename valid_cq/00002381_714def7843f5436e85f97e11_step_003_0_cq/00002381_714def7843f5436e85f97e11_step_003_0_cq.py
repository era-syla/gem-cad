import cadquery as cq

# --- Parametric Dimensions ---
# Main body dimensions
diameter = 10.0           # Main diameter of the cylindrical part
total_height = 25.0       # Approximate total height based on proportions

# Groove dimensions
groove_z_pos = 12.0       # Position of the groove from the top
groove_width = 1.5        # Width of the groove cut
groove_depth = 0.5        # Depth of the groove cut

# Bottom cut dimensions
flat_cut_height = 8.0     # Height of the bottom section with flats
flat_distance = 3.0       # Distance from center to the flat face (half of width across flats)

# --- Geometry Construction ---

# 1. Create the base cylinder
# We'll create a cylinder representing the full stock material first.
base = cq.Workplane("XY").circle(diameter / 2).extrude(total_height)

# 2. Create the circumferential groove
# We sketch a profile on a vertical plane and revolve-cut it.
# Alternatively, we can just make a cut with a specific shape. 
# A simple torus cut or a revolved triangle profile works. 
# Looking at the image, it's a V-groove with a slight radius, located roughly in the middle.
# Let's use a revolved profile approach for precision.
groove_profile = (
    cq.Workplane("XZ")
    .workplane(offset=0)
    .moveTo(diameter/2, total_height - groove_z_pos)
    .lineTo(diameter/2 - groove_depth, total_height - groove_z_pos - groove_width/2)
    .lineTo(diameter/2, total_height - groove_z_pos - groove_width)
    .close()
)

# Cut the groove
# To revolve cut around Z, we need to ensure the profile is placed correctly relative to the axis.
body_with_groove = base.cut(
    groove_profile.revolve(360, (0, 0, 0), (0, 0, 1))
)

# 3. Create the bottom flats
# The bottom section has material removed on two sides to create parallel flats.
# We can achieve this by cutting away two large rectangular blocks on the sides.
# The `flat_cut_height` determines how far up from the bottom (Z=0) this feature goes.
# The `flat_distance` is the distance from the center to the flat surface.

# Define a cutting tool for one side
cut_width = diameter * 2 # Make it large enough to clear the material
cut_depth = diameter     # Large enough
side_cut = (
    cq.Workplane("XY")
    .rect(cut_width, cut_depth)
    .extrude(flat_cut_height)
    .translate((0, flat_distance + cut_depth/2, 0)) # Shift it to the side
)

# Apply cuts
# Cut one side
result = body_with_groove.cut(side_cut)
# Cut the opposite side (mirror the cutting tool or create a new one)
result = result.cut(side_cut.rotate((0,0,0), (0,0,1), 180))

# Alternatively, a more direct way to cut the flats is to sketch on the bottom face.
# Let's refine the approach to be cleaner: select the bottom face, draw the shape to *keep* or shape to *remove*.
# Removing is easier. We remove everything outside the "flat_distance".

# Let's re-do step 3 with a cleaner logic:
# Create a cutting solid that represents the space to be removed.
# Dimensions for the box to cut:
cut_box_size = diameter * 1.5
cut_z_offset = 0 # Starts at bottom

# Cut 1: Positive Y side
cut1 = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .moveTo(0, flat_distance)
    .rect(cut_box_size, cut_box_size, centered=False) # Rectangle starting at (0, flat_distance) going +X +Y is wrong
    # Let's center X, and start Y at flat_distance
    .center(0, flat_distance)
    .rect(cut_box_size, cut_box_size, centered=False) # Logic tricky with moveTo/center combined
)

# Simplest reliable way for the flats:
# Use a large rectangle offset from center
cutter = (
    cq.Workplane("XY")
    .rect(diameter*2, diameter) # Width, Height
    .extrude(flat_cut_height)
    .translate((0, flat_distance + diameter/2, 0))
)

result = body_with_groove.cut(cutter).cut(cutter.rotate((0,0,0),(0,0,1), 180))

# Optional: Add the slight chamfer/fillet visible on the top edge if desired, 
# but looking closely at the image, it's quite sharp. The groove edges are sharp too.
# The transition from the flat part to the round part is a flat shelf.

# Final Result
result = result