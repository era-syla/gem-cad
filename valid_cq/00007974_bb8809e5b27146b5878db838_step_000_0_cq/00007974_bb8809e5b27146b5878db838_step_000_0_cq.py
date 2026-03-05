import cadquery as cq

# --- Parameter Definitions ---
# Overall panel dimensions
panel_height = 800.0
panel_width = 600.0
panel_thickness = 40.0

# Top recess/handle dimensions
top_recess_width = 150.0
top_recess_depth = 10.0
top_recess_height = 15.0  # Cut into the top edge

# Bottom access panel/door section dimensions
bottom_panel_height = 300.0
bottom_panel_inset_depth = 2.0  # Slight recess for the whole bottom area

# Inner small access door dimensions
inner_door_width = 150.0
inner_door_height = 150.0
inner_door_x_offset = 0.0  # Centered relative to bottom panel center
inner_door_y_offset = 0.0  # Centered relative to bottom panel center
inner_door_recess_depth = 3.0
inner_door_frame_width = 15.0 # Width of the frame around the handle area

# Small door handle dimensions
handle_width = 10.0
handle_height = 60.0
handle_depth = 5.0
handle_offset_x = -50.0 # Shifted to the left side of the inner door

# --- Geometry Construction ---

# 1. Base Panel
# Create the main rectangular block
result = cq.Workplane("XY").box(panel_width, panel_height, panel_thickness)

# 2. Top Edge Recess (Handle/Latch area)
# Cutting a slot in the center top edge
top_recess = (
    cq.Workplane("XZ")
    .workplane(offset=panel_height/2)  # Move to top face
    .center(0, -panel_thickness/2 + top_recess_depth/2) # Align to front edge
    .rect(top_recess_width, top_recess_depth)
    .extrude(-top_recess_height) # Cut downwards
)
result = result.cut(top_recess)


# 3. Bottom Panel Section (The larger lower recessed area)
# This looks like a separate plate or a stepped region.
# We will model it as a slight cut to create the step line.
bottom_panel_center_y = -panel_height/2 + bottom_panel_height/2
bottom_panel_cut = (
    cq.Workplane("XY")
    .workplane(offset=panel_thickness/2) # Front face
    .center(0, bottom_panel_center_y)
    .rect(panel_width, bottom_panel_height)
    .extrude(-bottom_panel_inset_depth)
)

# However, looking closely at the image, the bottom part actually protrudes slightly 
# or is the "flush" part while the top is recessed? 
# Or simpler: The main body is one thickness, and the bottom plate is added or defined by a cut.
# Let's interpret the image as: The bottom square is flush with the main frame, 
# but there is a seam line. Let's create the geometry by defining the lower region.
# A robust way is to cut the bottom area slightly.

result = result.cut(bottom_panel_cut)


# 4. Inner Small Access Door Frame
# This is a recessed rectangle within the bottom panel
inner_door_center_y = bottom_panel_center_y + inner_door_y_offset

inner_door_cut = (
    cq.Workplane("XY")
    .workplane(offset=panel_thickness/2 - bottom_panel_inset_depth) # Start from the bottom panel face
    .center(inner_door_x_offset, inner_door_center_y)
    .rect(inner_door_width + inner_door_frame_width, inner_door_height + inner_door_frame_width)
    .extrude(-inner_door_recess_depth)
)
result = result.cut(inner_door_cut)

# 5. The Inner Door Plate (Pop it back up slightly or leave as recess)
# The image shows a frame and then a flat area inside.
# Let's add the plate back in the center of the recess, slightly lower than flush.
inner_plate = (
    cq.Workplane("XY")
    .workplane(offset=panel_thickness/2 - bottom_panel_inset_depth - inner_door_recess_depth)
    .center(inner_door_x_offset, inner_door_center_y)
    .rect(inner_door_width, inner_door_height)
    .extrude(inner_door_recess_depth * 0.5) # Halfway back up
)
result = result.union(inner_plate)

# 6. The Handle on the Inner Door
# A simple vertical capsule or rectangular shape
handle = (
    cq.Workplane("XY")
    .workplane(offset=panel_thickness/2 - bottom_panel_inset_depth - inner_door_recess_depth * 0.5)
    .center(inner_door_x_offset + handle_offset_x, inner_door_center_y)
    .rect(handle_width, handle_height)
    .extrude(handle_depth)
    .edges("|Z").fillet(handle_width/2.1) # Round the vertical edges to make a pill shape
)
result = result.union(handle)

# 7. Hinge/Corner details (Top corners)
# There appear to be small hinge pins or screws in the top corners.
pin_dia = 6.0
pin_depth = 5.0

# Left Pin
pin_l = (
    cq.Workplane("XY")
    .workplane(offset=panel_height/2) # Top face
    .center(-panel_width/2 + 15, -panel_thickness/2 + 10)
    .circle(pin_dia/2)
    .extrude(-pin_depth)
)
result = result.cut(pin_l)

# Right Pin
pin_r = (
    cq.Workplane("XY")
    .workplane(offset=panel_height/2) # Top face
    .center(panel_width/2 - 15, -panel_thickness/2 + 10)
    .circle(pin_dia/2)
    .extrude(-pin_depth)
)
result = result.cut(pin_r)

# Optional: Add small fillets to the vertical edges of the main panel for realism
result = result.edges("|Z").fillet(1.0)

# Export or Render
if 'show_object' in globals():
    show_object(result)