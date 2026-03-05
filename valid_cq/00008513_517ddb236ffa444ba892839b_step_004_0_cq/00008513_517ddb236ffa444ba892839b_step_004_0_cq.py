import cadquery as cq

# --- Parameters ---
height = 60.0          # Total height
width = 12.0           # Width of the main body (X-axis)
depth = 12.0           # Depth of the main body (Y-axis)

# Top cap parameters
cap_height = 8.0
cap_fillet = 2.0
hole_dia = 4.0

# Vertical spine/back parameters
spine_thickness = 3.0
spine_width = 8.0

# Cylinder parameters
cyl_dia = 6.0
cyl_length = 35.0      # Length of the central cylindrical part

# Bottom base parameters
base_height = 6.0
base_chamfer = 2.0

# Locking/latch features
latch_width = 4.0
latch_depth = 4.0
latch_pos_z = 15.0 # From bottom
latch_length = 15.0

# Side rib parameters
rib_thickness = 2.0

# --- Construction ---

# 1. Base Geometry (The L-shaped profile formed by the spine and base)
# We build from the bottom up.

# Create the main spine extending the full height
spine = (
    cq.Workplane("XY")
    .box(width, spine_thickness, height, centered=(True, True, False))
)

# 2. Top Cap
top_cap = (
    cq.Workplane("XY")
    .workplane(offset=height - cap_height)
    .box(width, depth, cap_height, centered=(True, True, False))
    .edges("|Z").fillet(cap_fillet)
)

# 3. Bottom Base
base = (
    cq.Workplane("XY")
    .box(width, depth, base_height, centered=(True, True, False))
)

# Apply chamfer/cut to the front of the base to match the image
base = (
    base.faces(">Y").edges(">Z")
    .workplane(centerOption="CenterOfMass")
    .transformed(offset=(0, 0, 0), rotate=(45, 0, 0)) # Sloped cut
    .rect(width + 2, 5) # Oversized rect to cut
    .cutThruAll()
)

# 4. Central Cylinder
# Attached to the top cap, extending downwards
cylinder = (
    cq.Workplane("XY")
    .workplane(offset=height - cap_height - cyl_length)
    .circle(cyl_dia / 2.0)
    .extrude(cyl_length)
)

# 5. Front Vertical Feature (The latch-like part on the right side of the image)
# It sits on the base and goes up
front_feature = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .center(width/4.0, depth/2.0 - latch_depth/2.0) # Positioned to the side
    .box(latch_width, latch_depth, latch_length, centered=(True, True, False))
)
# Add a chamfer or taper to the top of this latch
front_feature = front_feature.faces(">Z").edges(">Y").chamfer(2.0)

# Add the small rectangular protrusion on the front feature
bump = (
    cq.Workplane("XY")
    .workplane(offset=base_height + 5.0)
    .center(width/4.0, depth/2.0)
    .box(latch_width - 1.0, 1.0, 6.0, centered=(True, False, False))
)

# 6. Side/Back Ribs (The features on the left side of the image)
# There's a tapered rib structure on the back/side
side_rib = (
    cq.Workplane("YZ")
    .workplane(offset=-width/2.0) # Left side face
    .moveTo(-spine_thickness/2.0, height - cap_height - 5.0)
    .lineTo(-depth/2.0, height - cap_height - 5.0)
    .lineTo(-depth/2.0 + 2.0, height - cap_height - 20.0) # Taper
    .lineTo(-spine_thickness/2.0, height - cap_height - 20.0)
    .close()
    .extrude(rib_thickness) # Extrude inwards
)

# 7. Combine Main Body parts
result = spine.union(top_cap).union(base).union(cylinder).union(front_feature).union(bump).union(side_rib)

# 8. Refinements

# Hole in the top
result = result.faces(">Z").workplane().circle(hole_dia / 2.0).cutThruAll()

# Fillets to smooth transitions (optional but makes it look molded)
# We selectively fillet vertical edges to match the smooth look
try:
    result = result.edges("|Z").fillet(0.5)
except:
    pass # If geometry is too complex for global fillet, skip or do specific edges

# The specific angled cut at the bottom front where the cylinder meets the base area
# The image shows a triangular/pyramidal transition below the cylinder
transition_cut = (
    cq.Workplane("XY")
    .workplane(offset=base_height)
    .center(0, 0)
    .rect(cyl_dia, cyl_dia)
    .workplane(offset=5.0)
    .rect(cyl_dia + 2, cyl_dia + 2) # Taper out
    .loft(combine=False)
)
# This is tricky to get exact from one image, but let's ensure the cylinder 
# connects cleanly to the spine.

# Shift the cylinder and front features slightly to align better with the "C" shape profile implied
# Let's rebuild the final union with a slight offset on the cylinder to merge it into the spine
cylinder_shifted = (
    cq.Workplane("XY")
    .workplane(offset=height - cap_height - cyl_length)
    .center(0, -1.0) # Shift back towards spine
    .circle(cyl_dia / 2.0)
    .extrude(cyl_length)
)

# Re-assemble for a cleaner boolean
result = spine.union(top_cap).union(base).union(cylinder_shifted).union(front_feature).union(bump).union(side_rib)
result = result.faces(">Z").workplane().circle(hole_dia / 2.0).cutThruAll()

# Add the chamfer at the very bottom corners
result = result.faces("<Z").edges().chamfer(0.5)

# Ensure the "L" shape cutout is clear
# The main body is essentially an L-bracket with things attached.
# Let's clean up the area between the front latch and the cylinder.

# Final Export
if 'show_object' in globals():
    show_object(result)