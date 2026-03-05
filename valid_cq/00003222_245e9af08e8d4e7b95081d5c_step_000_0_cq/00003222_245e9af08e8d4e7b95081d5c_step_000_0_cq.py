import cadquery as cq

# Parameters
total_length = 120.0
base_thickness = 2.0
strip_width = 12.0
head_radius = 12.0
head_offset = 2.0  # Extra thickness on the circular head
head_step_radius = 10.0 # Inner circle radius

# Rib parameters
rib_length = 45.0
rib_width_top = 4.0
rib_width_bottom = 8.0
rib_height = 5.0
rib_start_offset = 5.0 # From center of head

# Slit/Hole parameters
slit_length = 12.0
slit_width = 2.0
square_hole_side = 4.0
hole_spacing = 8.0 # Gap between features
features_start_distance = 60.0 # From center of head

# 1. Base Geometry: The main strip with a circular head
# Create the long rectangular part
strip = cq.Workplane("XY").box(total_length, strip_width, base_thickness, centered=(False, True, False))
# Move it so the start is near the origin to help with the head alignment
strip = strip.translate((-head_radius, 0, 0))

# Create the circular head
head_base = cq.Workplane("XY").circle(head_radius).extrude(base_thickness)
head_step = cq.Workplane("XY").workplane(offset=base_thickness).circle(head_step_radius).extrude(head_offset)

# Fuse base components
base_structure = strip.union(head_base).union(head_step)

# 2. The Rib Feature
# This looks like a loft or a tapered extrusion.
# We'll create a profile on the top surface and extrude/chamfer or loft.
# Let's try a loft approach for the tapered sides.

rib_start_x = -head_radius + rib_start_offset + 5 # approximate start position
rib_z_level = base_thickness + (head_offset if rib_start_x < head_radius else 0) 
# Note: The rib seems to sit on top of the 'step' of the head and transition down to the strip.
# Let's simplify: It sits on the main level (z=base_thickness) but passes through the head step.

# Let's make the rib profile on the XY plane at z=base_thickness
# Bottom profile of the rib
rib_p1 = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness)
    .moveTo(0, 0)
    .rect(rib_length, rib_width_bottom, centered=(True, True))
    .translate((rib_length/2, 0, 0)) # Center the rect locally then move
)

# Top profile of the rib
rib_p2 = (
    cq.Workplane("XY")
    .workplane(offset=base_thickness + rib_height)
    .moveTo(0, 0)
    .rect(rib_length - (rib_height*2), rib_width_top, centered=(True, True)) # Shorten top to make slanted ends
    .translate((rib_length/2, 0, 0))
)

# Create the rib solid
rib = cq.Workplane("XY").workplane(offset=base_thickness).rect(rib_length, rib_width_bottom, centered=(False, True)).extrude(rib_height)
# Add chamfers to simulate the draft angle seen in the image
rib = rib.edges("|Z").chamfer(rib_height * 0.4) # Approximation for side slope
rib = rib.edges(">Z").fillet(0.5) # Slight rounding on top

# Position the rib. It starts near the center of the circle.
rib = rib.translate((-2, 0, 0))

# 3. Create the Holes (Cuts)
# Location calculation
slit1_center = features_start_distance
square_center = slit1_center + (slit_length/2) + hole_spacing + (square_hole_side/2)
slit2_center = square_center + (square_hole_side/2) + hole_spacing + (slit_length/2)

# Create the cut shapes
cutter = cq.Workplane("XY").workplane(offset=0)

# Slit 1
cutter = cutter.moveTo(slit1_center, 0).rect(slit_length, slit_width)
# Square Hole
cutter = cutter.moveTo(square_center, 0).rect(square_hole_side, square_hole_side)
# Slit 2
cutter = cutter.moveTo(slit2_center, 0).rect(slit_length, slit_width)

# Extrude cutters for boolean operation
cut_solid = cutter.extrude(base_thickness * 3) # Make sure it goes through

# 4. Final Assembly
# Combine base and rib
part = base_structure.union(rib)

# Apply cuts
result = part.cut(cut_solid)

# Optional: Add small fillets to the neck transition where the circle meets the strip
result = result.edges(cq.selectors.NearestToPointSelector((head_radius, strip_width/2, 0))).fillet(5.0)

# Refine: The rib in the image looks more like a trapezoidal prism with chamfered ends.
# Let's reconstruct the rib to match the image better (sloped sides and ends).
# Override previous rib logic for a cleaner look
rib_sketch_bottom = cq.Workplane("XY").workplane(offset=base_thickness).moveTo(-5, 0).rect(rib_length, rib_width_bottom)
rib_sketch_top = cq.Workplane("XY").workplane(offset=base_thickness + rib_height).moveTo(-5, 0).rect(rib_length - rib_height, rib_width_top)

# Lofting creates the tapered look
rib_better = rib_sketch_bottom.add(rib_sketch_top).toPending().loft()

# Re-unite with base structure (re-doing the assembly step)
part_v2 = base_structure.union(rib_better)
part_v2 = part_v2.cut(cut_solid)

# Re-apply fillets
result = part_v2.edges(cq.selectors.NearestToPointSelector((head_radius, strip_width/2, 0))).fillet(8.0)
result = result.edges(cq.selectors.NearestToPointSelector((head_radius, -strip_width/2, 0))).fillet(8.0)