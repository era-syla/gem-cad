import cadquery as cq

# --- Parametric Dimensions ---
# Main vertical panel (monitor/screen part)
panel_width = 300.0
panel_height = 200.0
panel_thickness = 15.0

# VESA mounting holes pattern (centered on panel)
vesa_width = 100.0
vesa_height = 100.0
hole_diameter = 5.0

# Horizontal support bar (below the panel)
bar_width = 250.0
bar_height = 20.0
bar_depth = 20.0
bar_offset_z = -10.0  # Offset from the bottom edge of the panel

# Support Post
post_diameter = 15.0
post_length = 150.0

# Base Clamp/Plate
base_width = 80.0
base_depth = 80.0
base_thickness = 15.0
base_pos_z = -100.0 # Position relative to the main panel center

# --- Geometry Construction ---

# 1. Create the Main Vertical Panel
panel = cq.Workplane("XY").box(panel_width, panel_height, panel_thickness)

# 2. Create Mounting Holes (VESA pattern)
# We create points for the holes relative to the center
hole_locations = [
    (-vesa_width/2, vesa_height/2),
    (vesa_width/2, vesa_height/2),
    (-vesa_width/2, -vesa_height/2),
    (vesa_width/2, -vesa_height/2)
]

panel = (panel.faces(">Z").workplane()
         .pushPoints(hole_locations)
         .hole(hole_diameter))

# 3. Create Horizontal Bar
# Positioned at the bottom of the panel
bar_center_y = -panel_height/2 + bar_height/2 - 10 # Slightly offset downwards visually
bar = (cq.Workplane("XY")
       .workplane(offset=-panel_thickness/2) # Align with back or front? Let's align generally
       .center(0, -panel_height/2 - bar_height/2 + 10) # Position below
       .box(bar_width, bar_height, bar_depth))

# Let's adjust the bar position to match the image better. 
# It looks attached to the bottom edge, slightly protruding.
# Re-defining bar logic for better placement relative to panel.
bar = (cq.Workplane("XY")
       .center(0, -panel_height/2 - bar_height/2)
       .box(bar_width, bar_height, bar_depth))

# 4. Create the Vertical Post
# The post goes down from the bar
post_top_z = 0 # Center Z
post_center_y = -panel_height/2 - bar_height/2 
# In the image, the post is behind the bar or attached to it.
# Let's attach it to the bottom of the bar.
post = (cq.Workplane("XY")
        .center(0, post_center_y)
        .circle(post_diameter/2)
        .extrude(-post_length))

# 5. Create the Base Plate
# The base plate is somewhere along the post.
# Looking at the image, there is a square plate partway down the post.
base_plate = (cq.Workplane("XY")
              .workplane(offset=base_pos_z)
              .center(0, post_center_y)
              .box(base_width, base_depth, base_thickness))

# --- Combine All Parts ---
result = panel.union(bar).union(post).union(base_plate)

# If necessary, apply fillets or specific details, but the image is quite blocky.

# Export or visualization
if 'show_object' in globals():
    show_object(result)