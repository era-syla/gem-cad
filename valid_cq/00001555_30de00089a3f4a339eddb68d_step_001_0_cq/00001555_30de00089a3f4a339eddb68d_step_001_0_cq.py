import cadquery as cq
import math

# --- Parameters ---
plate_diameter = 100.0  # Overall diameter of the disk
plate_thickness = 5.0   # Thickness of the disk
num_slots = 16          # Total number of slots around the perimeter
slot_width = 4.0        # Width of each radial slot
slot_depth = 10.0       # Radial depth of the slot from the outer edge
hole_pcd = 85.0         # Pitch Circle Diameter for the counterbored holes
hole_diameter = 4.0     # Through-hole diameter
cbore_diameter = 8.0    # Counterbore diameter
cbore_depth = 2.0       # Depth of the counterbore
# The holes appear to be aligned vertically (at 12 and 6 o'clock positions relative to the slots)
# or slightly offset. Looking closely, the holes are exactly between two slots.
# Let's verify alignment: 
# The top hole is near a slot at the very top. Actually, looking at the image, 
# there are slots at 0, 22.5, 45... degrees.
# The holes seem to be placed at 90 and 270 degrees (or top/bottom in the view),
# but slightly offset from the main axis or perhaps aligned with specific slots?
# Upon closer inspection, the hole at the top is between two slots.
# If there are 16 slots, the angle between slots is 360/16 = 22.5 degrees.
# The holes seem to be at 90 degrees + some offset, or just centered between slots.
# Let's assume the holes are at the "North" and "South" positions, centered between slots.

# --- Modeling ---

# 1. Base Disk
result = cq.Workplane("XY").circle(plate_diameter / 2.0).extrude(plate_thickness)

# 2. Create the Radial Slots
# We will create one cutting shape and rotate it
slot_cutter = (
    cq.Workplane("XY")
    .rect(slot_width, plate_diameter) # Create a long rectangle wider than the diameter
    .extrude(plate_thickness)         # Extrude to match thickness
)

# Move the cutter so it only cuts the edge to the specific depth
# The rectangle is centered. Its half-length is plate_diameter/2.
# We want the cut to go `slot_depth` deep from the edge `plate_diameter/2`.
# So the inner edge of the cut should be at `plate_diameter/2 - slot_depth`.
# A centered rectangle of length `L` extends to `L/2`.
# We need a cutter positioned effectively.
# A simpler way with CadQuery is to make a cutter at the correct radius and use polar arrays.

# Let's redefine the slot cutting strategy using cut and polarArray
# Create a single slot shape at the 3 o'clock position (X-axis)
slot_shape = (
    cq.Workplane("XY")
    .center(plate_diameter/2.0 - slot_depth/2.0, 0) # Position center of cut
    .box(slot_depth, slot_width, plate_thickness) # Box dimensions: length, width, height
)

# Subtract the slots in a pattern
# Since the box is centered on its local origin, we need to adjust the center offset carefully.
# If we center at (R - depth/2), the outer edge is at R, inner at R-depth.
# Wait, box centers on current workplane center.
# Let's use a more robust polar array cut on the main object.

# Re-approach for the slots:
# Draw a rectangle on the top face, move it to the edge, revolve/pattern it, then cut.
result = (
    result.faces(">Z").workplane()
    .polarArray(plate_diameter/2 - slot_depth/2, 0, 360, num_slots)
    .rect(slot_depth, slot_width) # Rect is width x height in local coordinates (radial x tangential)
    .cutBlind(-plate_thickness)
)

# 3. Create the Mounting Holes
# The holes are typically countersunk or counterbored. Image looks like a shallow counterbore.
# Location: Looks like they are at 90 and 270 degrees (top and bottom).
# Let's assume 2 holes, 180 degrees apart.
# In the image, the top hole is between two slots. The slots are at 0, 22.5, 45...
# If slots are at 0, 22.5, 45, 67.5, 90... then a hole at 90 would hit a slot.
# But the image shows the hole between slots.
# So either the slots are offset, or the holes are offset.
# Let's assume slots start at 0. Then 16 slots are at k*22.5 deg.
# 90 degrees / 22.5 = 4. So there is a slot exactly at North (90 deg).
# In the image, there is a slot exactly at the top (12 o'clock).
# The hole is to the left of that top slot.
# It looks like the hole is at angle 90 + (22.5/2) = 101.25 degrees?
# Or maybe the holes are the primary axis and slots are offset by half-pitch.
# Let's rotate the slot pattern by half a pitch (360/16/2 = 11.25 deg) so slots don't align with X/Y axes perfectly?
# Actually, looking at the very bottom (6 o'clock), there is a hole. There is NO slot at 6 o'clock.
# This implies slots are at 11.25, 33.75, etc.
# Let's keep the previous slot code (which puts a slot at 0 degrees/X-axis) and rotate the holes to be between them.
# 360 / 16 = 22.5 degrees pitch. Half pitch = 11.25 degrees.
# If we place holes at 90 and 270, they will be between slots if slots are at 11.25 + k*22.5.
# The previous code puts slots at 0, 22.5, 45, 67.5, 90...
# So a hole at 90 hits a slot.
# Let's rotate the slot pattern by 11.25 degrees so slots avoid the major axes.

# Resetting result to apply offset rotation to slots
result = cq.Workplane("XY").circle(plate_diameter / 2.0).extrude(plate_thickness)

# Create slots with offset angle
# polarArray(radius, start_angle, angle_range, count)
# We start at 11.25 degrees to offset the pattern
start_angle = 360.0 / num_slots / 2.0 

result = (
    result.faces(">Z").workplane()
    .polarArray(plate_diameter/2 - slot_depth/2, start_angle, 360, num_slots)
    .rect(slot_depth, slot_width)
    .cutBlind(-plate_thickness)
)

# Now place holes at 90 and 270 degrees (Top and Bottom)
# Using standard workplane locations
result = (
    result.faces(">Z").workplane()
    .pushPoints([(0, hole_pcd/2.0), (0, -hole_pcd/2.0)]) # Top and Bottom
    .cboreHole(hole_diameter, cbore_diameter, cbore_depth)
)

# Optional: Add small fillets/chamfers to edges if desired, but image is sharp.
# The slots have rounded bottoms? Hard to tell, looks like square cuts.
# The main edge has a slight chamfer? Maybe very small. We will stick to the main geometry.