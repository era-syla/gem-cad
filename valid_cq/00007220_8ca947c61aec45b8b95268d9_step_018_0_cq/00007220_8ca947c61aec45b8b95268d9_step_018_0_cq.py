import cadquery as cq

# --- Parametric Dimensions ---
# Base dimensions
base_leg_length = 80.0
base_leg_width = 10.0
base_leg_spacing = 50.0  # Gap between legs
base_crossbar_depth = 10.0
base_thickness = 5.0

# Feet dimensions (at the tips of the legs)
foot_height = 5.0
foot_length = 10.0

# Upright dimensions
upright_height = 40.0
upright_thickness = 5.0  # Thickness of the vertical wall

# Top platform dimensions
top_width = base_leg_spacing + 2 * base_leg_width
top_depth = 60.0
top_thickness = 10.0

# Notch dimensions (on the top platform)
notch_width = 20.0
notch_depth = 5.0
notch_thickness = 3.0  # How deep into the material it cuts

# --- Modeling ---

# 1. Create the U-shaped base
# We'll sketch the U-shape on the XY plane.
# The overall width is leg_width + spacing + leg_width
overall_width = 2 * base_leg_width + base_leg_spacing

# Let's center the base on the Y-axis for symmetry
# Left Leg
left_leg = (
    cq.Workplane("XY")
    .rect(base_leg_width, base_leg_length)
    .extrude(base_thickness)
    .translate((-(base_leg_spacing/2 + base_leg_width/2), 0, 0))
)

# Right Leg
right_leg = (
    cq.Workplane("XY")
    .rect(base_leg_width, base_leg_length)
    .extrude(base_thickness)
    .translate(((base_leg_spacing/2 + base_leg_width/2), 0, 0))
)

# Crossbar (connecting the back of the legs)
# Positioned at the back of the legs. 
# Legs are centered at Y=0, so they go from -length/2 to +length/2.
# We want the crossbar at the "back" (let's say -Y direction).
crossbar_y_pos = -base_leg_length/2 + base_crossbar_depth/2
crossbar = (
    cq.Workplane("XY")
    .rect(base_leg_spacing, base_crossbar_depth)
    .extrude(base_thickness)
    .translate((0, crossbar_y_pos, 0))
)

base_structure = left_leg.union(right_leg).union(crossbar)

# 2. Add Feet
# Small blocks at the front tip of each leg, going downwards.
foot_y_pos = base_leg_length/2 - foot_length/2
left_foot = (
    cq.Workplane("XY")
    .rect(base_leg_width, foot_length)
    .extrude(-foot_height) # Extrude downwards
    .translate((-(base_leg_spacing/2 + base_leg_width/2), foot_y_pos, 0))
)
right_foot = (
    cq.Workplane("XY")
    .rect(base_leg_width, foot_length)
    .extrude(-foot_height) # Extrude downwards
    .translate(((base_leg_spacing/2 + base_leg_width/2), foot_y_pos, 0))
)

base_with_feet = base_structure.union(left_foot).union(right_foot)

# 3. Create the Vertical Upright
# This rises from the back crossbar.
# It sits on top of the base geometry.
upright_z_start = base_thickness
upright_y_pos = -base_leg_length/2 + upright_thickness/2 

upright = (
    cq.Workplane("XY")
    .rect(overall_width, upright_thickness)
    .extrude(upright_height)
    .translate((0, upright_y_pos, upright_z_start))
)

# 4. Create the Top Platform
# This extends forward from the top of the upright.
top_z_pos = upright_z_start + upright_height - top_thickness
# The back of the top aligns with the back of the upright
# The upright back is at y = -base_leg_length/2
# So the center of the top needs to be calculated
top_back_y = -base_leg_length/2
top_center_y = top_back_y + top_depth/2

top_platform = (
    cq.Workplane("XY")
    .rect(overall_width, top_depth)
    .extrude(top_thickness)
    .translate((0, top_center_y, top_z_pos))
)

# 5. Add the Notch to the Top Platform
# The notch is located at the front edge of the top platform.
notch_y_center = top_back_y + top_depth - notch_depth/2
notch = (
    cq.Workplane("XY")
    .rect(notch_width, notch_depth)
    .extrude(notch_thickness) # Cut depth
    .translate((0, notch_y_center, top_z_pos + top_thickness - notch_thickness))
)

# Combine everything
# We union the base, upright, and top, then cut the notch
result = (
    base_with_feet
    .union(upright)
    .union(top_platform)
    .cut(notch)
)

# Optional: Center the whole model or adjust position if needed for display
# This moves the assembly so the bottom of the feet is at Z=0? 
# Currently bottom of feet is at Z = -foot_height.
# Let's leave coordinates relative to the main sketch plane for clarity.