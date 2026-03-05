import cadquery as cq

# Parametric dimensions
height = 35.0
width = 14.0
depth = 14.0
wall_thickness = 1.5
fillet_radius = 1.0

# Side feature dimensions
slot_width = 10.0
slot_height = 2.0
slot_z_offset = 6.0  # From center of face upwards

window_width = 10.0
window_height = 9.0
window_z_offset = -5.0  # From center of face downwards

tab_width = 4.0
tab_height = 4.0

# 1. Create the main body block
result = cq.Workplane("XY").box(width, depth, height)

# 2. Apply fillets to vertical edges
result = result.edges("|Z").fillet(fillet_radius)

# 3. Create the internal cavity (hollow tube open at top)
result = (
    result.faces(">Z")
    .workplane()
    .rect(width - 2 * wall_thickness, depth - 2 * wall_thickness)
    .cutBlind(-(height - wall_thickness))
)

# 4. Create features on the side face (Right Face >X)
# We need to cut a slot and a window that leaves a tab at the bottom

# Helper calculations for the "Window with Tab" geometry
# Window geometry relative to the window center
# We calculate the areas to CUT to leave the tab remaining
cut_left_w = (window_width - tab_width) / 2
cut_left_h = window_height
cut_left_center_x = -(tab_width / 2 + cut_left_w / 2)
cut_left_center_y = 0  # Relative to window center

cut_right_w = cut_left_w
cut_right_h = window_height
cut_right_center_x = (tab_width / 2 + cut_right_w / 2)
cut_right_center_y = 0

cut_top_w = tab_width
cut_top_h = window_height - tab_height
cut_top_center_x = 0
# Top cut center Y: Window Top is +H/2. Tab Top is -H/2 + Tab_H.
# Cut Top section is between Tab Top and Window Top.
# Center is (Window_Top + Tab_Top) / 2
# Window Top = window_height / 2
# Tab Top = -window_height / 2 + tab_height
cut_top_center_y = (window_height / 2 + (-window_height / 2 + tab_height)) / 2

# Apply cuts
result = (
    result.faces(">X")
    .workplane()
    
    # Feature A: Horizontal Slot
    .center(0, slot_z_offset)
    .rect(slot_width, slot_height)
    .cutBlind(-wall_thickness * 2)
    
    # Reset origin to face center for next feature
    .center(0, -slot_z_offset)
    
    # Feature B: Lower Window (Constructed as 3 cuts to leave the tab)
    .center(0, window_z_offset)
    
    # 1. Left Vertical Cut
    .center(cut_left_center_x, cut_left_center_y)
    .rect(cut_left_w, cut_left_h)
    .cutBlind(-wall_thickness * 2)
    .center(-cut_left_center_x, -cut_left_center_y) # Reset
    
    # 2. Right Vertical Cut
    .center(cut_right_center_x, cut_right_center_y)
    .rect(cut_right_w, cut_right_h)
    .cutBlind(-wall_thickness * 2)
    .center(-cut_right_center_x, -cut_right_center_y) # Reset
    
    # 3. Top Section Cut (above the tab)
    .center(cut_top_center_x, cut_top_center_y)
    .rect(cut_top_w, cut_top_h)
    .cutBlind(-wall_thickness * 2)
)

# Export or Render
if __name__ == "__main__":
    # show_object(result) # Only for CQ-editor
    pass