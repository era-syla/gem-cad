import cadquery as cq

# 1. Define Parameters for the parametric model
length = 150.0          # Total length of the part
height_center = 35.0    # Height at the central peak
height_end = 12.0       # Height at the outer ends
end_taper_x = 20.0      # Horizontal inset for the top corners (creates the angled ends)
thickness = 3.0         # Thickness of the material
slot_width = 3.2        # Width of the interlocking slots
slot_depth = 12.0       # Depth of the slots measured from the top surface
slot_pos_offset = 40.0  # Distance from the center to the slot location

# 2. Define Profile Points
# The shape is drawn on the XY plane centered horizontally
# Coordinates are calculated to create the trapezoidal/peaked profile
p_bottom_left = (-length / 2.0, 0.0)
p_bottom_right = (length / 2.0, 0.0)
p_top_right = (length / 2.0 - end_taper_x, height_end)
p_peak = (0.0, height_center)
p_top_left = (-length / 2.0 + end_taper_x, height_end)

profile_points = [
    p_bottom_left,
    p_bottom_right,
    p_top_right,
    p_peak,
    p_top_left
]

# 3. Create the Base Solid
# Create a closed polyline and extrude it to create the main plate
base = (
    cq.Workplane("XY")
    .polyline(profile_points)
    .close()
    .extrude(thickness)
)

# 4. Create Cutters for Slots
# Calculate the Y-height of the top surface at the slot position to ensure correct depth
# We use linear interpolation between the peak and the end point
# x_dist is the horizontal distance from the peak (0) to the slope end
x_slope_end = length / 2.0 - end_taper_x
# Ratio of the slot position along the slope
slope_ratio = slot_pos_offset / x_slope_end
# Calculate Y height at the specific X location
surface_y_at_slot = height_center + (height_end - height_center) * slope_ratio

# Determine the Y coordinate for the bottom of the slot
slot_bottom_y = surface_y_at_slot - slot_depth

# Define a cutter box dimensions
# Height needs to be sufficient to cut through the top peak
cutter_height = height_center 
# Center Y of the cutter box so its bottom edge aligns with slot_bottom_y
cutter_y_center = slot_bottom_y + cutter_height / 2.0

# Create a generic cutter object
# We extrude more than the thickness to ensuring a clean boolean cut
cutter_tool = (
    cq.Workplane("XY")
    .rect(slot_width, cutter_height)
    .extrude(thickness * 2)
    .translate((0, cutter_y_center, -thickness / 2.0))
)

# 5. Apply Cuts
# Translate the cutter tool to the left and right positions and subtract from base
result = (
    base
    .cut(cutter_tool.translate((-slot_pos_offset, 0, 0)))
    .cut(cutter_tool.translate((slot_pos_offset, 0, 0)))
)