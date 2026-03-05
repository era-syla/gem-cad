import cadquery as cq

# --- Parameter Definitions ---
# Overall plate dimensions
plate_width = 50.0   # Assumed width based on visual proportions
plate_length = 80.0  # Assumed length
plate_thickness = 5.0 # Assumed thickness

# Large central hole
center_hole_diam = 20.0
# Position relative to the center of the plate or an end?
# It looks offset towards one end. Let's place it relative to the 'front' end.
center_hole_offset_from_front = 25.0 

# Mounting holes (4 small ones)
mounting_hole_diam = 3.5
# These look like a standard NEMA stepper motor pattern or similar.
# Let's assume a square or rectangular pattern centered around the large hole.
mounting_pattern_width = 31.0 # Standard NEMA 17 is 31mm
mounting_pattern_length = 31.0

# Counterbored slots/holes at the rear
# These look like they are for mounting the plate itself to something else.
rear_mount_hole_diam = 5.0
rear_mount_cbore_diam = 10.0
rear_mount_cbore_depth = 3.0
rear_mount_spacing = 30.0 # Distance between centers
rear_mount_offset_from_back = 10.0 # Distance from the back edge

# The grey unpainted area suggests a distinct feature, likely a step or just visual representation of raw metal. 
# Looking closely, the plate seems uniform thickness, but there might be a "tab" at the back.
# However, simpler interpretation is a single rectangular plate.
# Let's treat it as a single solid block.

# --- Construction ---

# 1. Base Plate
# We'll create the base rectangle centered on X, but Y aligned to make positioning easier.
result = (
    cq.Workplane("XY")
    .box(plate_width, plate_length, plate_thickness)
)

# 2. The Large Center Hole
# Let's define the position of the large hole. 
# Visually, the plate has a "front" (bottom right in image) and "back" (top left).
# Let's define the center hole position relative to the geometric center.
# Actually, looking at standard motor mounts, the large hole is usually central to the mounting holes.

# Let's re-orient: Center the workplane on the large hole location.
# Visual estimation: The large hole is roughly 1/3rd from the front edge.
hole_center_y = -plate_length/2 + center_hole_offset_from_front

result = (
    result
    .faces(">Z")
    .workplane()
    # Move to the location of the large hole
    .center(0, hole_center_y)
    .hole(center_hole_diam)
)

# 3. The 4 Mounting Holes (NEMA style)
# We are currently centered on the large hole.
result = (
    result
    .faces(">Z")
    .workplane()
    .center(0, hole_center_y) # Re-center on the large hole
    .rect(mounting_pattern_width, mounting_pattern_length, forConstruction=True)
    .vertices()
    .hole(mounting_hole_diam)
)

# 4. The Rear Mounting Slots/Counterbores
# These are located near the "back" of the plate (positive Y relative to our start, or just offset from edge).
# From the center of the original box (0,0), the back edge is at y = +plate_length/2.
rear_y_pos = (plate_length / 2) - rear_mount_offset_from_back

result = (
    result
    .faces(">Z")
    .workplane()
    # Move to the rear mounting line
    .center(0, rear_y_pos)
    # Create two points for the holes
    .pushPoints([(-rear_mount_spacing/2, 0), (rear_mount_spacing/2, 0)])
    .cboreHole(rear_mount_hole_diam, rear_mount_cbore_diam, rear_mount_cbore_depth)
)

# Optional: Add the visual "step" or unpainted section at the back if strictly modeling geometry.
# The image shows the back section is grey, front is black.
# Sometimes this implies a thickness change. The grey part looks slightly thinner in some CAD renders, 
# or it's just a surface finish.
# Let's assume it's a slight mill-down (step) for accuracy to the visual cue.
# Let's Mill down the black area slightly? Or assume the grey area is the full thickness?
# Looking at the reflection on the edge, the grey part seems to be the full thickness 
# and the black part might be the same thickness. It's likely just a texture application in the render.
# However, to be safe, if that is a mechanical feature, it looks like a "tab".
# I will keep it as a flat plate as it's the most robust interpretation of the geometry.

# However, looking closely at the transition line where the color changes:
# There is a faint line across the side face. This often indicates a geometric seam.
# The grey part (back) looks like the base material, the black part might be a slightly raised surface or just anodized.
# Let's just treat it as a single solid for the generated CAD as geometric topology is continuous.

# Final cleanup/fillets if visible? 
# The corners look sharp.

# Export or Return
# (The prompt requires the variable 'result')