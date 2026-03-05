import cadquery as cq

# --- Parameters ---

# Battery Dimensions (Modeled after a generic AA battery)
batt_diameter = 14.5
batt_length = 50.5
batt_pos_nub_dia = 5.5
batt_pos_nub_height = 2.0

# Holder Dimensions
holder_length = batt_length + 2.0  # Slightly longer than battery
wall_thickness = 1.5               # Wall thickness around batteries
gap_width = 4.0                    # Central gap between the left and right pairs
center_bridge_height = 8.0         # Height of the bridge connecting sides
mount_hole_dia = 3.0               # Diameter of mounting holes in the gap

# Derived Geometry
holder_radius = batt_diameter / 2 + wall_thickness
offset_x = holder_radius + gap_width / 2  # Horizontal offset of cylinder centers
offset_z = batt_diameter / 2              # Vertical offset for stacking

# --- Model Construction ---

# 1. Create the Single Reference Battery (for visualization, floating above)
# Main body
battery_body = cq.Workplane("XY").circle(batt_diameter/2).extrude(batt_length)
# Positive terminal nub
battery_nub = (
    cq.Workplane("XY")
    .workplane(offset=batt_length)
    .circle(batt_pos_nub_dia/2)
    .extrude(batt_pos_nub_height)
)
# Combine battery parts and move it up for the view
battery = battery_body.union(battery_nub).translate((0, -30, 40))


# 2. Create the Battery Holder

# We will sketch the cross-section of one side (a pair of cylinders) and then mirror/extrude.

# Define the centers of the two stacked cylinders on the right side
top_cyl_center = (0, offset_z)
bot_cyl_center = (0, -offset_z)

# Create the profile for the right side (looking from Front/YZ plane logic, but we'll sketch on YZ)
# Actually, let's sketch on XY plane for length extrusion along Z, or YZ for extrusion along X.
# Let's sketch on the "Front" plane (XZ usually in CQ, but let's stick to standard sketch plane).
# Let's sketch on XY plane and extrude up Z. This means the cross section is in XY.

# Right side centers
r_top = (offset_x, offset_z)
r_bot = (offset_x, -offset_z)
# Left side centers
l_top = (-offset_x, offset_z)
l_bot = (-offset_x, -offset_z)

# Create the main shape by unioning 4 cylinders and a central block
# We model the solid block first, then cut the holes.

# A. Create the four outer shells
# We create a sketch based on circles and hulls or just union cylinders. 
# A cleaner way for the specific "figure-8" shape is to union cylinders and a bridge.

# Right Side Block
right_col = (
    cq.Workplane("XY")
    .moveTo(r_bot[0], r_bot[1]).circle(holder_radius)
    .moveTo(r_top[0], r_top[1]).circle(holder_radius)
    .extrude(holder_length)
)

# Left Side Block
left_col = (
    cq.Workplane("XY")
    .moveTo(l_bot[0], l_bot[1]).circle(holder_radius)
    .moveTo(l_top[0], l_top[1]).circle(holder_radius)
    .extrude(holder_length)
)

# Connect the columns with a central bridge
# The bridge connects the inner edges.
bridge = (
    cq.Workplane("XY")
    .rect(offset_x * 2, center_bridge_height) # Spans the gap
    .extrude(holder_length)
)

# Combine into raw block
holder_block = right_col.union(left_col).union(bridge)

# B. Cut the battery slots
# We need 4 cylindrical cuts.
# Note: The image shows open slots (C-shaped clips).
# To make them clips, the cut diameter usually needs to break through the surface slightly
# or we define a specific "mouth" opening.
# Looking at the image, the outer sides are open. The "opening" width is less than diameter.

# Let's define the cutting cylinders.
cut_r_top = cq.Workplane("XY").moveTo(r_top[0], r_top[1]).circle(batt_diameter/2).extrude(holder_length)
cut_r_bot = cq.Workplane("XY").moveTo(r_bot[0], r_bot[1]).circle(batt_diameter/2).extrude(holder_length)
cut_l_top = cq.Workplane("XY").moveTo(l_top[0], l_top[1]).circle(batt_diameter/2).extrude(holder_length)
cut_l_bot = cq.Workplane("XY").moveTo(l_bot[0], l_bot[1]).circle(batt_diameter/2).extrude(holder_length)

# Cut the battery holes
holder = holder_block.cut(cut_r_top).cut(cut_r_bot).cut(cut_l_top).cut(cut_l_bot)

# C. Create the side openings (to make them snap-fit clips)
# We cut a rectangular slot from the outer edge towards the center.
# The slot width should be slightly smaller than battery diameter to retain it.
slot_width = batt_diameter * 0.85 # Opening size

# Define a cutting shape for the side slots
# We need cuts on the far right and far left.
cut_box_r = (
    cq.Workplane("XY")
    .workplane(offset=0)
    .moveTo(r_bot[0], 0) # Center vertically between the right pair
    .rect(holder_radius * 2, holder_length * 3) # Make it huge
    .extrude(holder_length)
    .translate((holder_radius, 0, 0)) # Move strictly to the right side
)

# To get the specific shape in the image where the slot follows the cylinder curvature until the opening:
# The image actually shows the "Figure 8" shape intersected with a rectangle, rather than full cylinders.
# Let's refine the "outer shells" logic.
# Instead of cutting slots into full cylinders, let's cut a rectangular channel along the outer sides.

slot_cut_right = (
    cq.Workplane("XY")
    .moveTo(r_bot[0], -holder_length) # Start well below
    .rect(holder_radius, holder_length * 4) # A tall strip
    .extrude(holder_length)
    .translate((holder_radius + batt_diameter/2 - 1.5, 0, 0)) # Position on the right edge
    # This placement is approximate to create the "lip"
)

# Actually, the simplest way to get the image look (C-clips):
# Create a rectangular cut on the far right and far left that trims the "cheeks" of the holder.
trim_width = 10
trim_r = (
    cq.Workplane("XY")
    .moveTo(r_top[0] + batt_diameter/2, 0)
    .rect(trim_width, 100) # Tall rectangle
    .extrude(holder_length)
    .translate((trim_width/2 - (batt_diameter - slot_width)/2, 0, 0))
)
trim_l = (
    cq.Workplane("XY")
    .moveTo(l_top[0] - batt_diameter/2, 0)
    .rect(trim_width, 100)
    .extrude(holder_length)
    .translate((-trim_width/2 + (batt_diameter - slot_width)/2, 0, 0))
)

holder = holder.cut(trim_r).cut(trim_l)

# D. Add mounting holes in the central bridge
# The image shows holes drilled through the center bridge (Y-axis direction in local coords, but here X-axis relative to gap).
# The holes are perpendicular to the main extrusion axis.
# Since we extruded in Z, the bridge face is on the XZ plane (side) or YZ plane (front).
# The holes go through the "gap" direction (Y axis in our sketch plane coordinates).
# Wait, based on the image, the bridge is horizontal, the gap is vertical.
# The holes go through the "floor" of the gap.

# Let's orient ourselves to the image:
# Z is cylinder axis.
# X is left-right (across the two pairs).
# Y is up-down (stacking of cylinders).
# The "Gap" is in the middle. The holes go through the Y-thickness of the bridge.

hole_locations = [(0, holder_length * 0.3), (0, holder_length * 0.7)] # Position along length

for loc in hole_locations:
    # Create a cylinder to cut the hole
    hole_cutter = (
        cq.Workplane("XZ") # Plane perpendicular to Y
        .workplane(offset=-10) # Start outside
        .moveTo(loc[1], 0) # X is length (Z in global), Y is width (X in global) -> mapping is tricky
        # Let's use world coordinates for clarity.
        # We need a cylinder oriented along Y axis.
    )
    
    # Using simple cylinder primitive for cutting
    c_hole = (
        cq.Workplane("XY")
        .moveTo(0, 0) # Center X/Y
        .circle(mount_hole_dia/2)
        .extrude(20) # Length of cut
        .rotate((0,0,0), (1,0,0), 90) # Rotate to point along Y
        .translate((0, 0, loc[1])) # Move up along Z (length of holder)
    )
    holder = holder.cut(c_hole)


# E. Add the central slot/groove
# The image shows a rectangular slot cut out of the very center of the bridge.
# This separates the left and right halves slightly more distinctly in the middle.
center_slot = (
    cq.Workplane("XY")
    .rect(2.0, 100) # Width 2, very tall
    .extrude(holder_length)
)
# But wait, the bridge connects them. The image shows a groove, but not a full cut-through?
# Looking closely at the image, there is a slot in the bridge for the mounting holes, 
# and potentially a notch at the end.
# Let's add the small notches at the end of the cylinders (visible on top right of holder).
# These look like retention tabs or polarity indicators.
notch = (
    cq.Workplane("XY")
    .rect(2, 2)
    .extrude(2)
    .translate((r_top[0], r_top[1] + holder_radius, holder_length))
)

# Let's perform the central recess cut (the channel where the holes are)
# The bridge is currently solid. We want a channel.
channel_width = 3.0
channel = (
    cq.Workplane("XY")
    .rect(channel_width, 100) # Narrow width, extends across Y
    .extrude(holder_length)
    .translate((0, 0, 0)) # Center
)
# We only want to cut the "top" and "bottom" of the bridge if we want a separate look,
# but the image shows a solid bridge with holes.
# However, there are rectangular cutouts at the ends of the central spine.
spine_cutout_width = 2.0
spine_cutout_depth = 4.0

spine_cutout = (
    cq.Workplane("XY")
    .rect(spine_cutout_width, 20) # Y-dimension needs to clear the bridge
    .extrude(spine_cutout_depth)
    .translate((0, 0, holder_length - spine_cutout_depth))
)
holder = holder.cut(spine_cutout)


# Final Rotation to match image orientation roughly
# Image has tubes running diagonal.
# We generated tubes along Z.
result = holder.rotate((0,0,0), (1,0,0), -90).translate((0, 20, 0))

# Add the battery back to the result for display
result = result.union(battery)

# Export or Render
if 'show_object' in globals():
    show_object(result)