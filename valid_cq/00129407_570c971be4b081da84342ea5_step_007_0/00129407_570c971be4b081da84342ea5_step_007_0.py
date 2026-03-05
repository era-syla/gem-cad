import cadquery as cq

# --- Parametric Dimensions ---
# Based on standard action camera mount dimensions
mount_width = 15.0       # Total width (Y axis)
body_depth = 15.0        # Thickness of the central body (X axis)
hole_spacing = 35.0      # Distance between top and bottom hole centers
ear_radius = 7.5         # Radius of the mounting lobes
hole_diameter = 5.0      # Diameter of the bolt holes
prong_width = 3.0        # Width of a single prong
gap_width = 3.0          # Width of the gaps between prongs
chamfer_size = 0.8       # Chamfer size on body edges
window_width = 7.0       # Width of the central cutout
window_height = 18.0     # Height of the central cutout

# --- Geometry Construction ---

# 1. Create the Central Body Block
# A rectangular prism connecting the two mounting ends.
# Height spans the distance between hole centers.
body = cq.Workplane("XY").box(body_depth, mount_width, hole_spacing)

# Apply chamfers to the vertical edges of the body for the styled look
body = body.edges("|Z").chamfer(chamfer_size)

# 2. Create the Rounded Ends (Ears)
# Cylinders oriented along the Y-axis at the top and bottom hole positions.
top_ear = (
    cq.Workplane("XZ")
    .workplane(offset=mount_width / 2.0)
    .moveTo(0, hole_spacing / 2.0)
    .circle(ear_radius)
    .extrude(-mount_width)
)

bottom_ear = (
    cq.Workplane("XZ")
    .workplane(offset=mount_width / 2.0)
    .moveTo(0, -hole_spacing / 2.0)
    .circle(ear_radius)
    .extrude(-mount_width)
)

# Combine body and ears
result = body.union(top_ear).union(bottom_ear)

# --- Cuts ---

# Parameters for cutting tools
cut_depth = body_depth * 2  # Ensure full cut through X
# Vertical range of the slot cuts (from hole center outwards and inwards)
slot_cut_height = ear_radius * 2.5 

# 3. Create Slots for Top (2-Prong) Adapter
# Standard configuration: Gap in Center, Prongs on sides.
# We cut away the center and the far outsides.
# Center cut
result = result.cut(
    cq.Workplane("XY")
    .workplane(offset=hole_spacing / 2.0)
    .box(cut_depth, gap_width, slot_cut_height)
)

# Left Outer cut (removing material to leave 3mm prong)
result = result.cut(
    cq.Workplane("XY")
    .workplane(offset=hole_spacing / 2.0)
    .center(0, -(gap_width + prong_width + 5.0)) # Offset to outside
    .box(cut_depth, 10.0, slot_cut_height)
)

# Right Outer cut
result = result.cut(
    cq.Workplane("XY")
    .workplane(offset=hole_spacing / 2.0)
    .center(0, (gap_width + prong_width + 5.0))
    .box(cut_depth, 10.0, slot_cut_height)
)

# 4. Create Slots for Bottom (3-Prong) Adapter
# Standard configuration: Prongs in Center and outsides, Gaps in between.
# Gap centers at +/- 3.0mm from axis
# Gap 1
result = result.cut(
    cq.Workplane("XY")
    .workplane(offset=-hole_spacing / 2.0)
    .center(0, -3.0)
    .box(cut_depth, gap_width, slot_cut_height)
)
# Gap 2
result = result.cut(
    cq.Workplane("XY")
    .workplane(offset=-hole_spacing / 2.0)
    .center(0, 3.0)
    .box(cut_depth, gap_width, slot_cut_height)
)

# 5. Drill Mounting Holes
# Through-holes along the Y-axis at both ends
result = (
    result.faces(">Y").workplane()
    .pushPoints([(0, hole_spacing / 2.0), (0, -hole_spacing / 2.0)])
    .hole(hole_diameter)
)

# 6. Create Central Window
# A rectangular cutout through the body (X-axis)
result = result.cut(
    cq.Workplane("YZ")
    .rect(window_width, window_height)
    .extrude(body_depth * 2, both=True)
)

# Final Result
# result is the variable containing the final CadQuery object