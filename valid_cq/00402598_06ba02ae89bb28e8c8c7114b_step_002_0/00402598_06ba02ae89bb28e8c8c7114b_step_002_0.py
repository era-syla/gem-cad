import cadquery as cq

# Dimensions and Parameters
thickness = 3.0
panel_height = 60.0

# 1. Left Panel
# A solid rectangular plate oriented in the YZ plane
# Positioned to the left
left_panel = (
    cq.Workplane("YZ")
    .box(thickness, 80, panel_height)
    .translate((-50, 0, panel_height / 2))
)

# 2. Back Panel with Door and Window
# Oriented in the XZ plane, positioned behind
back_w = 90.0
back_h = panel_height

# Door Parameters
door_width = 25.0
door_radius = door_width / 2.0
door_rect_height = 35.0  # Height of the rectangular part of the door
door_x_pos = -20.0       # X offset from the center of the panel

# Window Parameters
window_size = 18.0
window_x_pos = 25.0
window_z_pos = 10.0      # Z offset from the center of the panel (vertical position)

# Create the base wall
back_panel_base = cq.Workplane("XZ").box(back_w, thickness, back_h)

# Create the Door Cutter Geometry
# Calculating coordinates relative to the panel center (Z=0 at center, so bottom is -back_h/2)
door_bottom_z = -back_h / 2
door_top_rect_z = door_bottom_z + door_rect_height
door_left_x = door_x_pos - door_radius
door_right_x = door_x_pos + door_radius

door_sketch = (
    cq.Workplane("XZ")
    .moveTo(door_left_x, door_bottom_z)
    .lineTo(door_left_x, door_top_rect_z)
    .threePointArc(
        (door_x_pos, door_top_rect_z + door_radius),  # Apex of the arch
        (door_right_x, door_top_rect_z)               # End of the arch
    )
    .lineTo(door_right_x, door_bottom_z)
    .close()
    .extrude(thickness * 3, both=True)  # Extrude enough to cut through
)

# Create the Window Cutter Geometry
window_sketch = (
    cq.Workplane("XZ")
    .moveTo(window_x_pos, window_z_pos)
    .rect(window_size, window_size)
    .extrude(thickness * 3, both=True)
)

# Apply cuts and position the Back Panel
back_panel = (
    back_panel_base
    .cut(door_sketch)
    .cut(window_sketch)
    .translate((10, 40, back_h / 2))
)

# 3. Front Panel
# A smaller solid rectangular plate oriented in the XZ plane
# Positioned in front
front_panel_h = 45.0
front_panel = (
    cq.Workplane("XZ")
    .box(50, thickness, front_panel_h)
    .translate((20, -40, front_panel_h / 2))
)

# Combine all parts into the final result
result = left_panel.union(back_panel).union(front_panel)